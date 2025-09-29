import findspark
findspark.init()

import os, datetime, sys, importlib, time, uuid 
from pyspark import SparkConf
from pyspark.sql import SparkSession
#from pyspark.sql.conf import RuntimeConfig
from pyspark.sql.types import *
import pyspark.sql.functions as F

from cep_common import config as con
from schema.kafka_schema import kafka_table_schema


class SparkPipeline:
    def __init__(
        self, session, SRC_TYPE , DEST_TYPE, SRC_PATH=None, KAFKA_TOPIC=None,
        SAVE_PATH=None, ES_MAPPING_ID=None, ES_INDEX_NAME=None,
        CHECK_POINT_PATH=None, TRANSFORM_MODULE_PATH=None, TRANSFORM_MODULE=None, 
        ES_MAPPING_ID_FOR_LOG=None, ES_INDEX_NAME_FOR_LOG=None, 
	    SRC_KAFKA_TOPIC=None, DEST_KAFKA_TOPIC=None, CREATE_TASK_ID=None, CREATE_ID=None, **kwargs
    ):
        self._session = session
        self._src_type = SRC_TYPE
        # delta
        self._src_path = SRC_PATH
        # kafka
        self._kafka_topic = KAFKA_TOPIC
        self._src_kafka_topic = SRC_KAFKA_TOPIC
        self._dest_kafka_topic = DEST_KAFKA_TOPIC

        # read_schema 가 나을까? write 는 스키마 불필요함
        # 유사한 kafka_schema 추출
        self._kafka_schema = None
        if self._kafka_topic or self._src_kafka_topic:
            # input_topic 값 추출
            input_topic = self._src_kafka_topic
            if self._src_kafka_topic == None:
                input_topic = self._kafka_topic
            # best effort 유사 스키마 추출
            schema_name = None
            try:
                self._kafka_schema = kafka_table_schema[input_topic]
                schema_name = input_topic
            except Exception as e:
                for key in kafka_table_schema.keys():
                    # in 기반 유사 스키마명 찾기
                    if input_topic in key or key in input_topic:
                        self._kafka_schema = kafka_table_schema[key]
                        schema_name = key
                        break # re_ 필터용?
                # 기본 스키마(int_topic) 적용
                if not self._kafka_schema:
                    self._kafka_schema = kafka_table_schema["int_topic"]
                    schema_name = "default(int_topic)"
            print(f"--loading kafka_schema: '{schema_name}' as SRC--")


        self._dest_type = DEST_TYPE
        # delta, delta-upsert
        self._save_path = SAVE_PATH
        # es
        self._es_mapping_id = ES_MAPPING_ID
        self._index_name = ES_INDEX_NAME
        self._check_point_path = CHECK_POINT_PATH
        # es 기반 로깅 설정
        self._index_nm_abr = ""
        if self._index_name:
            if "sentence" in self._index_name:
                self._index_nm_abr = "sen"
            elif "doc" in self._index_name:
                self._index_nm_abr = "biz"
            else:
                self._index_nm_abr = "file"

        #common
        self._tranform_module_path = TRANSFORM_MODULE_PATH
        self._transform_module = TRANSFORM_MODULE

        #log
        self._es_mapping_id_for_log = ES_MAPPING_ID_FOR_LOG
        self._index_name_for_log = ES_INDEX_NAME_FOR_LOG
        self._create_task_id = CREATE_TASK_ID
        self._create_id = CREATE_ID

        ## 여기 UDF & es_conf 등 설정
        # 로깅용 함수
        self._uuid_udf = F.udf(lambda z: uuid.uuid5(uuid.NAMESPACE_OID, z).hex, StringType())
        # proc_system 산출용
        self._CEP_ENV = os.environ.get("CEP_ENV", "")
        # app_name 기반 코드: 이거 위치 바꾸고 싶은데..
        self._app_name = self._session.sparkContext.appName
        self._stage_no = int(self._app_name.split("-")[0][0:][-1]) # Step 'N'
        # 로깅용 ES 설정
        self._log_conf = {
            "es.nodes": con.ES_NODES,
            "es.mapping.id": self._es_mapping_id_for_log,
            "es.write.operation":"upsert" 
        }
        # write 용 ES 설정
        self._es_conf = {
            "es.nodes": con.ES_NODES,
            "es.mapping.id": self._es_mapping_id,
            "es.write.operation":"upsert"
        }


    def set_vars(
        self, SRC_TYPE=None, DEST_TYPE=None, SRC_PATH=None, KAFKA_TOPIC=None,
        SAVE_PATH=None, ES_MAPPING_ID=None, ES_INDEX_NAME=None,
        CHECK_POINT_PATH=None, TRANSFORM_MODULE_PATH=None, TRANSFORM_MODULE=None,
        ES_MAPPING_ID_FOR_LOG=None, ES_INDEX_NAME_FOR_LOG=None, 
        SRC_KAFKA_TOPIC=None, DEST_KAFKA_TOPIC=None, CREATE_TASK_ID=None, CREATE_ID=None
        ):
        # input, output source
        if SRC_TYPE is not None:
            self._src_type = SRC_TYPE
        if DEST_TYPE is not None:
            self._dest_type = DEST_TYPE
        # delta
        if SRC_PATH is not None:
            self._src_path = SRC_PATH
        # kafka
        if KAFKA_TOPIC is not None:
            self._kafka_topic = KAFKA_TOPIC
        if SRC_KAFKA_TOPIC is not None:
            self._src_kafka_topic = SRC_KAFKA_TOPIC
        if DEST_KAFKA_TOPIC is not None:
            self._dest_kafka_topic = DEST_KAFKA_TOPIC

	# delta, delta-upsert
        if SAVE_PATH is not None:
            self._save_path = SAVE_PATH
        # es
        if ES_MAPPING_ID is not None:
            self._es_mapping_id = ES_MAPPING_ID
        if ES_INDEX_NAME is not None:
            self._index_name = ES_INDEX_NAME
        if CHECK_POINT_PATH is not None:
            self._check_point_path = CHECK_POINT_PATH
        #common
        if TRANSFORM_MODULE_PATH is not None:
            self._tranform_module_path = TRANSFORM_MODULE_PATH
        if TRANSFORM_MODULE is not None:
            self._transform_module = TRANSFORM_MODULE

        #log
        if ES_MAPPING_ID_FOR_LOG is not None:
            self._es_mapping_id_for_log = ES_MAPPING_ID_FOR_LOG
        if ES_INDEX_NAME_FOR_LOG is not None:
            self._index_name_for_log = ES_INDEX_NAME_FOR_LOG
        if CREATE_TASK_ID is not None:
            self._create_task_id = CREATE_TASK_ID
        if CREATE_ID is not None:
            self._create_id = CREATE_ID

    def read_stream(self, maxFilesPerTrigger=None, maxBytesPerTrigger=None, startingTimestamp=None, maxOffsetsPerTrigger=None):
        """
        create readstream

        Parameters
        ----------
        session : Session
            spark session

        Returns
        -------
        df : Dataframe
            spark df.readStream
        """
        
        #uuid_udf = F.udf(lambda z: uuid.uuid5(uuid.NAMESPACE_OID, z).hex, StringType())

        if self._src_type == "delta":
            if type(self._src_path) is not str:
                raise TypeError("Wrong type {} value passed in SRC_PATH. list type expected or value='all'".format(type(self._src_path)))
       # elif self._src_type == "kafka":
       #     if type(self._kafka_topic) is not str:
       #         raise TypeError("Wrong type {} value passed in KAFKA_TOPIC. list type expected or value='all'".format(type(self._kafka_topic)))
       # else:
       #     raise ValueError("Readstream: SRC_PATH {} received. Must be either 'delta' or 'kafka'.".format(self._src_type))

        if self._src_type == "delta":
            # failOnDataLoss 를 비활성화 시
            #   Delta VACUUM 동작 시 에러 발생 가능함
            df = self._session \
                .readStream \
                .format("delta") \
                .option("inferSchema", "true") \
                .option("failOnDataLoss", "false") 

            if maxFilesPerTrigger != None:
                df = df.option("maxFilesPerTrigger", maxFilesPerTrigger)
            if maxBytesPerTrigger != None:
                df = df.option("maxBytesPerTrigger", maxBytesPerTrigger)
            if startingTimestamp != None:
                df = df.option("startingTimestamp", startingTimestamp)

            df = df.load(self._src_path)

        elif self._src_type == "kafka":
            current_kafka_topic = self._src_kafka_topic
            if self._src_kafka_topic == None:
                current_kafka_topic = self._kafka_topic
            # startingOffsets: 'earliest' OR 'latest'
            # read raw message from kafka topic
            df = self._session\
                .readStream \
                .format("kafka") \
                .option("kafka.bootstrap.servers", con.KAFKA_NODES) \
                .option("subscribe", current_kafka_topic) \
                .option("startingOffsets", "earliest") \
                .option("failOnDataLoss", "false") 
            
            if maxOffsetsPerTrigger != None:
                df = df.option("maxOffsetsPerTrigger", maxOffsetsPerTrigger)
            # kafka startingTimestamp, need more testing
            # epoch(ms) required: 1705480796000
            if startingTimestamp != None:
                df = df.option("startingTimestamp", startingTimestamp)
            
            df = df.load()
            # check original Kafka DataType
            #print("---RAW KAFKA DATATYPE:")
            #df.printSchema()
            # BYTE -> STRING 타입변환
            df = df.selectExpr("CAST(value AS STRING)")
            # self._kafka_schema: SRC kafka 토픽에 적용할 스키마(별도 정의)
            # STRING인 value 필드에 JSON 양식 기반으로 신규 df 생성
            df = df.select(F.from_json(df.value, self._kafka_schema).alias("data")).select("data.*")
            # kafka topic 메세지가 깨졌을 경우 필터
            if self._create_id != "True":
                df = df.filter('id is not null')
        
        # yaml 파일 "CREATE_ID" 값이 "TRUE" 일 경우
        if self._create_id == "True":
            df = df.withColumn("id", F.expr("uuid()"))
            
        # yaml 파일 "CREATE_TASK_ID" 값이 "TRUE" 일 경우
        if self._create_task_id == "True":
            df = df.withColumn("task_id", F.expr("uuid()"))
            df = df.withColumn("task_type", 
                    F.when(F.col("task_type").isNull() | 
                        F.col("task_type").isin([""]), F.lit("real_time"))
                            .otherwise(F.col("task_type")))        

        # returns Spark Structured Streaming df
        return df

    def write_stream(self, df, processing_time='1 seconds', upsert_match_col=None, upsert_update_cols=None, upsert_insert_cols=None):
        """
        create writestream

        Parameters
        ----------
        df : Dataframe
            spark dataframe

        Returns
        -------
        query : spark query (writestream)
            spark df.writeStream
        """
        # output vars
        if self._dest_type == "delta" or self._dest_type == "delta-upsert" or self._dest_type == "delta-fbatch":
            if type(self._save_path) is not str:
                raise TypeError("Wrong type {} value passed in SAVE_PATH. list type expected or value='all'".format(type(self._save_path)))
        elif self._dest_type == "es":
            if type(self._index_name) is not str or \
            type(self._es_mapping_id) is not str or type(self._check_point_path) is not str:
                raise TypeError("Wrong type value passed in es options(ES_INDEX_NAME, ES_MAPPING_ID, CHECK_POINT_PATH). string type expected")
        elif self._dest_type == "kafka":
            if type(self._dest_kafka_topic) is not str:
                raise TypeError("Wrong type {} value passed in DEST_KAFKA_TOPIC. list type expected or value='all'".format(type(self._dest_kafka_topic)))
        else:
            raise ValueError("Writestream: DEST_TYPE {} received. Must be either 'delta', 'delta-upsert' or 'es' or 'kafka'.".format(self._src_type))

        if self._dest_type == "delta-upsert":
            if type(upsert_match_col) is not str:
                raise TypeError("Wrong type {} value passed in upsert_match_col. string type expected".format(type(upsert_match_col)))
            if upsert_update_cols != 'all':
                if type(upsert_update_cols) is not list:
                    raise TypeError("Wrong type {} value passed in upsert_update_cols. list type expected or value='all'".format(type(upsert_update_cols)))
            if upsert_insert_cols != 'all':
                if type(upsert_insert_cols) is not list:
                    raise TypeError("Wrong type {} value passed in upsert_insert_cols. list type expected or value='all'".format(type(upsert_insert_cols)))

        # global col_dt fix
        df = df.withColumn("col_dt", F.current_timestamp())

        if self._dest_type == "delta":
    
            df = df.withColumn("date", F.col('col_dt').cast(DateType()))

            query = df.writeStream \
                .format("delta") \
                .outputMode("append") \
                .trigger(processingTime=processing_time) \
                .option("checkpointLocation", "{}/{}".format(self._check_point_path, "check_points")) \
                .option("path", self._save_path)
        # 2023.02.09 엣지 kafka sink 추가
        elif self._dest_type == "kafka":      
            # BYTE 타입 변환 불필요
            #df = df.selectExpr("CAST(value AS BINARY)")
            # create df w/ col. "value" containing all df.columns as json 
            #df = df.select(F.to_json(F.struct(df.columns)).alias("value"))
            query = df.selectExpr("to_json(struct(*)) AS value") \
                .writeStream \
                .format("kafka") \
                .outputMode("append") \
                .option("kafka.bootstrap.servers", con.KAFKA_NODES) \
                .option("failOnDataLoss", "false") \
                .option("topic", self._dest_kafka_topic) \
                .option("checkpointLocation", "{}/{}".format(self._check_point_path, "check_points"))

        elif self._dest_type == "delta-fbatch":
            mod = self._load_module()

            query = df.writeStream \
                .format("delta") \
                .foreachBatch(lambda batch_df, batch_id: 
                    mod.batch_write(
                        batch_df, batch_id, 
                        save_path=self._save_path, 
                        spark=self._session)) \
                .outputMode("append") \
                .trigger(processingTime=processing_time) \
                .option("checkpointLocation", "{}/{}".format(self._check_point_path, "check_points"))

        # 이거 사용 케이스 있나?
        elif self._dest_type  == "delta-upsert":
            from delta.tables import DeltaTable
            update_vals, insert_vals = {}, {}

            # create delta table if it doesn't exist
            init_df = self._session.createDataFrame(self._session.sparkContext.emptyRDD(), df.schema)
            init_df.write.format("delta").mode("ignore").save(self._save_path)

            def upsert_data(df, batch_id):
                dt1 = DeltaTable.forPath(self._session, self._save_path)
                dt1 = dt1.alias("oldData") \
                    .merge( \
                        df.alias("newData"), \
                    "oldData.{0} = newData.{0}".format(upsert_match_col))

                if upsert_update_cols=='all':
                    dt1 = dt1.whenMatchedUpdateAll()
                else:
                    for x in upsert_update_cols:
                        update_vals[x] = "newData.{}".format(x)
                    dt1 = dt1.whenMatchedUpdate(set=update_vals)

                if upsert_insert_cols=='all':
                    dt1 = dt1.whenNotMatchedInsertAll()
                else:
                    for x in upsert_insert_cols:
                        insert_vals[x] = "newData.{}".format(x)
                    dt1 = dt1.whenNotMatchedInsert(value=insert_vals)

                dt1.execute()

            query = df.writeStream \
                .format("delta") \
                .foreachBatch(upsert_data) \
                .outputMode("update") \
                .trigger(processingTime=processing_time) \
                .option("checkpointLocation", "{}/{}".format(self._check_point_path, "check_points"))

        elif self._dest_type  == "es":
            try:
                query = df.writeStream \
                    .format("es") \
                    .options(**self._es_conf) \
                    .outputMode("append") \
                    .trigger(processingTime=processing_time) \
                    .option("checkpointLocation", "{}/{}".format(self._check_point_path, "check_points")) \
                    .option("es.resource", "{}/{}".format(self._index_name +"_basic"))
            except Exception as e:
                print("spark_app.ERROR>>>>", e)
                query = None
    
        elif self._dest_type  == "api":
            query = None
        # query = None 일 경우 다음 read_stream() 으로 진행
        return query


    #############################################################
    ##  23.04.03 foreachBatch 방식 로깅함수
    #############################################################
    def pre_log(self, df, statusString, process_date, errString = None, st="", bi=""):
        # 요 에러핸들링 필요한가??
        if type(self._es_mapping_id_for_log) is not str or type(self._index_name_for_log) is not str:
            raise TypeError("Wrong type value passed in es options(ES_INDEX_NAME, ES_MAPPING_ID, CHECK_POINT_PATH). string type expected")
        
        

        # 재처리 파이프라인의 경우 'task_id' 로 'id' 대체
        log_df = addColumn("id", df.columns, df, sub="task_id")
             
        # 'file_id' 필드 생성: 대체로 'id' 컬럼이 file_id 임
        log_df = addColumn("id", df.columns, df, alias="file_id")

        # TODO 에러로깅 & 핸들링 전체적인 개선안
        if errString is None:
            # API 에러 등 발생 시: err_cd & err_msg 접수
            if "err_cd" in df.columns and "err_msg" in df.columns:
                log_df = log_df.withColumn("err_msg", F.col("err_msg"))
                log_df = log_df.withColumn("err_cd", F.col("err_cd"))
            else:    
                log_df = log_df.withColumn("err_msg", F.lit(""))
                log_df = log_df.withColumn("err_cd", F.lit("0"))
        else:
            # Pipeline 에러 발생 시
            log_df = log_df.withColumn("err_msg", F.lit(errString))
            log_df = log_df.withColumn("err_cd", F.lit("400"))

        # 'doc_id' 필드가 없거나 Null 인 경우 'id' 필드로 대체
        log_df = addColumn("doc_id", df.columns, log_df, alias="biz_id", sub="id")
        log_df = addColumn("task_id", df.columns, log_df)
        log_df = addColumn("task_type", df.columns, log_df)
        log_df = addColumn("file_name", df.columns, log_df)
        log_df = addColumn("title", df.columns, log_df)
        log_df = addColumn("biz_l_cd", df.columns, log_df)
        log_df = addColumn("biz_m_cd", df.columns, log_df)
        log_df = addColumn("biz_s_cd", df.columns, log_df)
        log_df = addColumn("data_src_l_cd", df.columns, log_df)
        log_df = addColumn("data_src_m_cd", df.columns, log_df)
        log_df = addColumn("data_src_s_cd", df.columns, log_df)
        log_df = addColumn("data_type_l_cd", df.columns, log_df)
        log_df = addColumn("data_type_m_cd", df.columns, log_df)
        #log_df = addColumn("data_type_s_cd", df.columns, log_df)
        log_df = addColumn("event_date", df.columns, log_df)
        log_df = addColumn("biz_title", df.columns, log_df, sub="title")
        ## self._app_name & _stage.no        
        # uuid("appName_startingTime_batchId_monIncId")
        log_df = log_df.withColumn("pair_id", self._uuid_udf(F.concat( 
                F.lit(self._app_name), F.lit("_"), F.lit(st), F.lit("_"), F.lit(bi), 
                F.lit("_"), F.monotonically_increasing_id())))
        log_df = log_df.withColumn("app_name", F.lit(self._app_name))
        log_df = log_df.withColumn("stage", F.lit(self._stage_no))
        log_df = log_df.withColumn("status", F.lit(statusString))
        log_df = log_df.withColumn("process_date", F.lit(process_date)) 

        # 2023.06.21 색인 인덱스명 표기 필드
        log_df = log_df.withColumn("index_nm", F.lit(self._index_nm_abr))

        # 출처 시스템 필드
        log_df = log_df.withColumn("proc_system", F.lit(self._CEP_ENV))

        # Spark SQL 내장 uuid() 함수로 대체: 중복만 아니면 됨
        log_df = log_df.withColumn("log_id", F.expr("uuid()"))

        # cols 리스트 만들까?
        log_df = log_df.select("file_id","biz_id","task_id","status","task_type",
            "process_date","event_date","stage", "app_name", 
            "biz_s_cd","data_src_s_cd","data_type_m_cd",
            "title","file_name", "index_nm",
            "err_cd","err_msg", "biz_title", "proc_system",
            "log_id","pair_id") 

        return log_df

    # REFACTOR: log_conf 한번만 선언
    def send_log(self, df, log_conf):
        # 인덱스 YYMM 형식으로 색인
        ts = datetime.datetime.now()
        now = ts.strftime("%Y%m")

        df.write.format("es") \
            .options(**log_conf) \
            .mode("append") \
            .option("es.resource", f"{self._index_name_for_log}_{now}") \
            .save()


    def fbatch_log(self, df, batch_id):
        """
        :param df: dataframe from data src 
        :type df: pyspark.sql.dataframe.DataFrame (static pyspark df)
        :param batch_id: unique integer value for micro-batch
        :type batch_id: int
        """
        # 에러 발생 시 로그 남겨야 함
        try:
            #print("--START Micro-Batch")
            # start_time
            start_time = int(time.time()*1000) 
            end_df = None #df.unpersist()용     

            # TODO 개선 OR 제거.. 성능엔 도움?
            cnt = df.count()
            if cnt == 0:
                return
            
            # start log 준비 
            start_log_df = self.pre_log(
                df, "start", start_time, st=start_time, bi=batch_id)
            self.send_log(start_log_df, self._log_conf) 

            # 데이터 메타화 (변환모듈 호출)
            # .cache() 없으면 변환모듈 두번씩 호출됨
            trans_df = self.run_transform(df, spark=self._session)

            # col_dt 처리 필수             
            end_df = trans_df.withColumn("col_dt", F.current_timestamp()).cache()

            # TODO 에러 메세지 추출 방안 변경안 검토
            ## 23.05.08 err_cd & err_msg 추출
            # df.first() 리턴값은 Non-deterministic
            # .cache() 직후 호출
            first = end_df.first()

            # TODO write 함수 일원화
            ### Write 모음              
            # delta
            if self._dest_type == "delta" or self._dest_type == "delta-fbatch":
                # 파티셔닝 목적 "date" 컬럼 생성
                write_df = end_df.withColumn("date", F.col('col_dt').cast(DateType()))
                write_df.write \
                    .format("delta") \
                    .mode("append") \
                    .save(self._save_path)
            # es
            elif self._dest_type == "es":
                # write to E/S index
                end_df.write.format("es") \
                    .mode("append") \
                    .options(**self._es_conf) \
                    .option("es.resource", f"{self._index_name}_basic") \
                    .save()
            # kafka
            elif self._dest_type == "kafka":
                write_df = end_df.selectExpr("to_json(struct(*)) AS value") \

                write_df.write \
                    .format("kafka") \
                    .option("kafka.bootstrap.servers", con.KAFKA_NODES) \
                    .option("topic", self._dest_kafka_topic) \
                    .save()
            # skip writing result df to sink
            else:
                pass
            
            # end_df.count() == 0 일 때 first == None
            # TODO err_cd 점검 & 핸들링 개선 필요
            if first:
                err_cd = "0"
                err_msg = ""
                # AND 문 때문에 코드 & 메세지 추출이 안된 것 같음
                if "err_cd" in first:
                    err_cd = first["err_cd"]
                if "err_msg" in first:
                    err_msg = first["err_msg"]
                    
                start_log_df = start_log_df.withColumn("err_cd", F.lit(err_cd))
                start_log_df = start_log_df.withColumn("err_msg", F.lit(err_msg))

            # 역기서 end_time & proc_time 처리
            end_time = int(time.time()*1000)
            # start_log_df vs df.count()
            
            proc_time = 0
            # cnt 폐기하고 proc_time 처리할 방안?
            # 그냥 proc_time 에 micro_batch 처리시간을 넣는다..
            # PMS 에서 쓰는지 확인하고 변경
            if cnt > 0: # divided by 0 회피
                # proc_time: 소숫점 두자리, 초(sec) 단위
                proc_time = round(int((end_time - start_time)/cnt)/1000,2)
            # end_log 준비
            # 'err_cd' 가 "0" 일때만 'status' == "end"
            end_log_df = start_log_df.withColumn("status", F.when(
                    F.col("err_cd").like("0"), F.lit("end"))
                        .otherwise(F.lit("error")))\
                .withColumn("process_date", F.lit(end_time))\
                .withColumn("proc_time", F.lit(proc_time)) \
                .withColumn("log_id", F.expr("uuid()"))

            # end_log 작성
            self.send_log(end_log_df, self._log_conf)
            #print("--END Micro-Batch")
            

        # Pipeline error log
        except Exception as e:
            print("Pipeline Error Occured. Writing error log. ")
            err_time = int(time.time()*1000)
            # TODO 문자열 길이 점검
            errString = str(e)[:1024]
            # 에러로그 준비
            error_log_df = self.pre_log(
                df, "error", err_time, errString=errString,
                st=start_time, bi=batch_id)
            self.send_log(error_log_df, self._log_conf)   

            # 이걸 빼고 무중단으로 운영하도록?
            raise RuntimeError(e) 

        ## end_df 캐쉬 삭제 *중요함
        finally:
            if end_df:
                end_df.unpersist()
            
    #############################################################
    ## 23.04.03 : 신규 foreachBatch 로깅 함수 끝
    #############################################################

    def run_transform(self, df, **args):
        """
        runs custom transform from module
        """
        mod = self._load_module()
        df = mod.run_transform(df, **args)

        return df

    def _load_module(self):
        if type(self._tranform_module_path) is not str:
            raise TypeError("Wrong type {} value passed in TRANSFORM_MODULE_PATH. \
                list type expected or value='all'".format(type(self._tranform_module_path)))
        if type(self._transform_module) is not str:
            raise TypeError("Wrong type {} value passed in TRANSFORM_MODULE. \
                list type expected or value='all'".format(type(self._transform_module)))

        sys.path.append(self._tranform_module_path)
        mod = importlib.import_module("{}.{}".format(self._tranform_module_path.split("/")[-1], self._transform_module))

        return mod


## 23.07.31 Null 값을 가진 경우 "" 로 처리 로직 추가
## 로그 필수 컬럼 생성 함수
def addColumn(new_column, cols, df, alias=None, sub=None):
    # 생성될 컬럼명 지정
    col_name = new_column
    if alias: 
        col_name = alias
    # 'new_column' 필드 있고 sub 없을 떄
    if new_column in cols and not sub:
        return_df = df.withColumn(col_name,
            F.when(F.col(new_column).isNull(), F.lit(""))
            .otherwise(F.col(new_column))
        )
    # 'new_column' 필드 있고 sub 있을 떄:
    #    kafka 에서 doc_id Null 일떄.. id 로 대체
    elif new_column in cols and sub and sub in cols:
        return_df = df.withColumn(col_name,
            F.when(F.col(new_column).isNull(), F.col(sub))
            .otherwise(F.col(new_column))
        )
    # 'new_column' 필드 없고: 대체 필드 'sub' 지정 시
    elif new_column not in cols and sub and sub in cols:        
        return_df = df.withColumn(col_name, 
            F.when(F.col(sub).isNull(), F.lit(""))
            .otherwise(F.col(sub))
        )
    # 아무 것도 없으면 "" 리턴
    else:
        return_df = df.withColumn(col_name, F.lit(""))
    # 신규 컬럼 추가된 spark df 리턴
    return return_df

def create_spark_session(appName):
    # ==================================================================================
    # Create SparkSession
    # ==================================================================================

    sparkConf = SparkConf()
    #sparkConf.set("spark.ui.port","11111") 
    print(f"Spark Config Type : {type(sparkConf)}")


 
    # 로컬 VSCode -> 원격 접속용 JAR 경로 설정
    print(os.path.exists("commons-pool2-2.6.2.jar"))
    print(os.path.exists("opensearch-spark-30_2.12-1.0.1.jar"))
    print(os.path.exists("kafka-clients-2.6.0.jar"))
    print(os.path.exists("spark-sql-kafka-0-10_2.12-3.1.2.jar"))
    print(os.path.exists("spark-token-provider-kafka-0-10_2.12-3.1.2.jar"))

    sparkConf.set("spark.jars", 
        f"commons-pool2-2.6.2.jar,\
        opensearch-spark-30_2.12-1.0.1.jar,\
        kafka-clients-2.6.0.jar,\
        spark-sql-kafka-0-10_2.12-3.1.2.jar,\
        spark-token-provider-kafka-0-10_2.12-3.1.2.jar")
    
    # move builder up
    builder = SparkSession.builder.appName(appName).config("spark.submit.pyFiles", "/app/apps/transfer.py")

    # moved enableHiveSupport() 
    spark = builder.config(conf=sparkConf).getOrCreate()


    spark.sparkContext.setLogLevel("ERROR")
    log4jLogger = spark.sparkContext._jvm.org.apache.log4j
    log = log4jLogger.LogManager.getLogger(__name__) # ?
    #log.warn("Hello World!")

    # Use Default Database
    if con.DEFAULT_DATABASE:
        spark.sql("use {}".format(con.DEFAULT_DATABASE))

    # print SparkConf
    #print("sparkConf:")
    #print(spark.sparkContext.getConf().get("spark.sql.catalogImplementation"))

    print(">> Spark Session was builded <<")


    return spark
