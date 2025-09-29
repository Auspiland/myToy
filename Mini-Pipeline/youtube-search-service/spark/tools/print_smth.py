import json

def print_dict(data, indent=2, color=True):
    """
    딕셔너리 또는 JSON 형식 데이터를 보기 좋게 출력합니다.
    - indent : 들여쓰기 간격
    - color  : 색상 출력 여부 (기본: True)
    """
    if color:
        try:
            from pygments           import highlight
            from pygments.lexers    import JsonLexer
            from pygments.formatters import TerminalFormatter

            formatted_json = json.dumps(data, indent=indent, ensure_ascii=False)
            colored_output  = highlight(formatted_json, JsonLexer(), TerminalFormatter())
            print(colored_output)
        except ImportError:
            # pygments 미설치 시 fallback
            print(json.dumps(data, indent=indent, ensure_ascii=False))
    else:
        print(json.dumps(data, indent=indent, ensure_ascii=False))
