from pyspark.sql.types import StructType, StringType, StructField

kafka_table_schema = {}

youtube_script_schema = StructType([
    StructField("id", StringType()),
    StructField("video_id", StringType()),
    
    StructField("title_name", StringType()),
    StructField("published_at", StringType()),
    StructField("script", StringType()),
    StructField("language", StringType()),

    StructField("err_cd", StringType()),
    StructField("err_msg", StringType()),
    StructField("err_detail", StringType()),
    StructField("etc_info", StringType())        # 기타 정보 (JSON 문자열 형태 추천)
])

kafka_table_schema['youtube_script'] = youtube_script_schema

