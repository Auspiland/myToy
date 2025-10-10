from fastapi import FastAPI, Request
from schemas import LoadChannel
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import requests


app = FastAPI()


templates = Jinja2Templates(directory="templates")

@app.get("/user", response_class=HTMLResponse)
async def search_page(request: Request):
    return templates.TemplateResponse("user.html", {"request": request})

########################################

@app.post("/spark-submit")
async def submit_to_spark(data: LoadChannel):
    payload = {
        "channel_name": data.channel_name,
        "channel_code": data.channel_code
    }
    print("I'm sending!")
    if payload["channel_code"] == None or payload["channel_code"] == "":
        payload["channel_code"] = "PL9a4x_yPK_86-3n5ggM7jescX0Q4770iU"
    try:
        
        res = requests.post("http://spark-app:8001/submit", json=payload)
        res.raise_for_status()  # HTTP 4xx/5xx 예외 발생
        return JSONResponse(
            status_code=200,
            content={"success": True, "message": "Spark 전송 성공", "result": res.json()}
        )
    except requests.RequestException as e:
        print("ERROR")
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": f"Spark 전송 실패: {str(e)}"}
        )