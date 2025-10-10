from pyspark.sql import DataFrame
from pyspark.sql.types import *
from conf.local.properties import QUERYTIMEOUT
import json
import os

KAFKA_NODES = "broker00:9092"
OUTPUT_TOPIC = "analysis_output"

def load_dummy():
    with open("data/dummy_kafka_data.json", 'r', encoding="utf-8-sig") as f:
        text = json.load(f)
    print("load_dummy : ", f"{type(text)} //  {text}")
    return text


def run(spark, input_df = None, dummy = False):
    if dummy and not input_df:
        raw_data = load_dummy()
        if not isinstance(raw_data, dict):
            raise ValueError(f"raw_data is not a dict : {raw_data}")
        df = spark.createDataFrame([raw_data])
    elif not dummy and input_df:
        if isinstance(input_df, DataFrame):
            df = input_df
        elif isinstance(input_df, dict):
            df = spark.createDataFrame([input_df])
        elif isinstance(input_df, list) and all(isinstance(item, dict) for item in input_df):
            df = spark.createDataFrame(input_df)
        else:
            raise ValueError("Module <tokafka>'s input is unvalid. : ", input_df)
    else:
        raise ValueError("Module <tokafka>'s input is unvalid. : ", input_df)

    # df = spark.createDataFrame(data=data, schema=cols)
    print("><><><><><><>df is : ",df)
    df.show()

    KAFKA_NODES = "docker:9092"
    TOPIC = "analysis"

    # write to KAFKA
    df.selectExpr("to_json(struct(*)) AS value") \
        .write \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_NODES) \
        .option("topic", TOPIC) \
        .save() 
        
    print(' --WRITE KAFKA END!--')
    return None
        
def write_kafka(spark, input_df = None, dummy = False):
    print("Writing kafka started.")

    query = write_kafka_streaming(input_df, topic="analysis_output")
    query.awaitTermination(timeout=QUERYTIMEOUT)

    print("Writing kafka successed!!")


def write_kafka_streaming(df, topic=OUTPUT_TOPIC, checkpoint_path=None):
    # value 컬럼 생성
    df_for_kafka = df.selectExpr("to_json(struct(*)) AS value")

    # 체크포인트 경로 없으면 자동 생성
    if not checkpoint_path:
        checkpoint_path = f"/tmp/checkpoint_{topic}"
        os.makedirs(checkpoint_path, exist_ok=True)

    query = df_for_kafka.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_NODES) \
        .option("topic", topic) \
        .option("checkpointLocation", checkpoint_path) \
        .outputMode("append") \
        .start()

    print(f"✅ Kafka writeStream started to topic: {topic}")
    return query