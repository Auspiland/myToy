import json, os, sys, logging
from common_utils import response_GPT

log = logging.getLogger(__name__)


def analysing_error(problem, code, error_msg, special_prompt=""):
    sys_prompt = (
        "당신은 코드 리뷰 전문가입니다. 에러로그를 보고 원인을 철저히 분석하세요"
    )
    special_prompt = "---\n입력데이터가 다음 조건에 맞는지 검수하세요 :\n" + special_prompt if special_prompt else ""
    user_prompt = f"""
다음 에러로그 혹은 틀린 결과값을 보고 오류 혹은 틀린 원인을 분석하세요.
원인은 두가지 경우가 있습니다. 1.유저 코드의 오류 2.테스트 데이터의 부정합
error or status :
{error_msg}
---
User code :
{code}
---
Probelm :
{problem}

{special_prompt}
"""

    log.info("Analysing Error")
    response = response_GPT(
        messages=[{"role":"system","content":sys_prompt},
                  {"role":"user","content":user_prompt}]
    )
    return response
