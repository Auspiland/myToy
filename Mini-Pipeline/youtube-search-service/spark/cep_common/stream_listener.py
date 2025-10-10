def print_batch(df, epoch_id):
    GREEN = "\033[92m"
    RESET = "\033[0m"
    if epoch_id == 0:
        print(f"[🟢 READY] {GREEN}Spark Streaming 초기화 완료!{RESET} 데이터 수신 대기 중...")
    else:
        print(f"📦 Batch {epoch_id} 진행 중")

    df.show(truncate=False)