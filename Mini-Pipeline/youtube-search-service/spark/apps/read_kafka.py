from pyspark.sql.types import *
import pyspark.sql.functions as F
from schema.kafka_schema import youtube_script_schema as schema
from conf.local.properties import QUERYTIMEOUT


KAFKA_NODES = "broker00:9092"
TOPIC = "analysis"

def read_kafka(spark, topic = TOPIC):
    if not topic:
        topic = TOPIC
    
    print(f"🔥 Kafka Streaming from topic: {topic}")

    # load to df
    df = spark \
            .readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", KAFKA_NODES) \
            .option("subscribe", topic) \
            .option("startingOffsets", "latest") \
            .option("failOnDataLoss", "false") \
            .load()
    
    df = df.selectExpr("CAST(value AS STRING) as value")

    df = df.select(F.from_json(df.value, schema).alias("data")).select("data.*") 
    
    print("✅ Streaming query started.")

    return df
