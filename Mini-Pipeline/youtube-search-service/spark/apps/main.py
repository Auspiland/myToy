from schema.opensearch_schema import LoadChannel
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import time, sys

import cep_common.spark_utils as su
from conf.local.properties import QUERYTIMEOUT
# from cep_common.stream_listener import print_batch

from load_script import load_script
from read_kafka import read_kafka
from tokafka import write_kafka_streaming
from toopensearch import write_opensearch
from transfer import transfer
from file2kafka import file_to_kafka


print("spark main.py was just started!")

app = FastAPI()


# FastAPI에서 Spark 컨테이너로 POST 요청

@app.post("/submit")
async def handle_submit(data: LoadChannel):
    if not data.channel_code.strip():
        return JSONResponse(content={"error": "빈 문자열입니다."}, status_code=400)

    print("🚀 SparkSession 시작합니다. 🚀")
    spark = su.create_spark_session(appName="channel_submit")

    ##############
    ## Pipeline ##
    ##############
    query1 = file_to_kafka(spark, "data/test_json")
    # print("What is going on??")
    # query.awaitTermination(timeout=100)

    print("📡📡📡📡📡Now tranferring started!📡📡📡📡📡")

    df_1 = read_kafka(spark,"analysis")
    
    df_2 = transfer(df_1)

    query3 = write_kafka_streaming(df_2)

    query4 = write_opensearch(df_2)

    GREEN = "\033[32m"
    RESET = "\033[0m"
    print(f"[🟢 READY] {GREEN}Spark Streaming 초기화 완료!{RESET} 데이터 수신 대기 중...")

    query5 = df_2.writeStream \
        .format("console") \
        .outputMode("append") \
        .option("truncate", False) \
        .start()
    
    # query5 = df_2.writeStream \
    #     .outputMode("append") \
    #     .foreachBatch(print_batch) \
    #     .start()



    queries = [query1, query3, query4, query5]
    start_time = time.time()

    while True:
        if time.time() - start_time > QUERYTIMEOUT:
            print("⏱️ Timeout reached. Stopping all queries.")
            for q in queries:
                if q.isActive:
                    q.stop()
            break
        time.sleep(0.5)




    print("🛑 Streaming query terminated.")

    row_count = df_2.count()

    result = JSONResponse(content={
        "status": "처리 완료",
        "channel": data.channel_name,
        "processed_rows": row_count
    })
    spark.stop()
   
    return result
