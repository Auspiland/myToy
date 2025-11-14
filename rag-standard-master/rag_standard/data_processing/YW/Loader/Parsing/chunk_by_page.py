def page_chunk(file_name, only_text_content, text_table_content):
    """
    페이지별로 추출된 내용 중 누락되는 경우를 보완하기 위한 함수
    - 실제로 페이지별로 내용을 추출하는 것은 Data Load 단계에서 이미 문서를 처리하면서 같이 진행됨
        >> 참고: 전체 문서를 한 청크로 가져오는 경우도 있음 - DOCX, HWP

    Args:
        file_name (str): 파일명
        only_text_content (dict): 텍스트만 추출한 페이지별 딕셔너리
        text_table_content (dict): 텍스트에 테이블까지 추출한 페이지별 딕셔너리

    Returns:
        fname (str): 정제된 파일명
        chunks (dict): text_table_content를 기준으로 혹시나 누락되는 정보가 있다면 only_text_content로 보완해서 저장된 페이지별 딕셔너리

    only_text_content, text_table_content, chunks의 딕셔너리 형식:
        {
            '페이지 번호': 페이지 내용,
            '페이지 번호': 페이지 내용,
             ...
        }
    """
    # 파일명 정제 (파일 경로 구분자 '/'가 포함되어 있다면 마지막 부분만 사용)
    fname = file_name.split('/')[-1] if '/' in file_name else file_name
    
    # 각 청크별 텍스트 생성: 내용이 충분하면 text_table_content의 내용을, 짧으면 only_text_content의 내용을 사용
    # 페이지별로 청크 구분해서 혹 text_table_content가 짧을 경우(10글자 미만), only_text_content로 누락되는 정보 보완
    chunks = {
        chunk: (content.lower() if len(content) >= 10 else only_text.lower())
        for chunk, content, only_text in zip(text_table_content.keys(), text_table_content.values(), only_text_content.values())
    }

    return fname, chunks