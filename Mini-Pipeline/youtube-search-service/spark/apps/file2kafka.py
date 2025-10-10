# This streaming method.
import os
from schema.kafka_schema import youtube_script_schema as schema


TOPIC = "analysis"
# file_dir = "data/test_json"

def file_to_kafka(spark, file_dir):

    print("📂 현재 작업 디렉토리:", os.getcwd())
    if not os.path.exists(file_dir):
        print("file does not exists")
        raise ValueError(file_dir)


    df = spark.readStream \
        .schema(schema) \
        .option("maxFilesPerTrigger", 1) \
        .json(file_dir)
    # maxFilesPerTrigger는 한번에 읽을 파일 수

    # print("This is DATAFRAME!!")
    # df.writeStream \
    #     .format("console") \
    #     .outputMode("append") \
    #     .start() \
    #     .awaitTermination()

    query = df.selectExpr("to_json(struct(*)) AS value") \
                .writeStream \
                .format("kafka") \
                .option("kafka.bootstrap.servers", "Kafka00Service:9092,Kafka01Service:9092,Kafka02Service:9092") \
                .option("topic", TOPIC) \
                .option("checkpointLocation", "/tmp/checkpoint" + TOPIC) \
                .start()
                    # .outputMode("append") \

    print("실행 중:", query.isActive)  # True

    return query
