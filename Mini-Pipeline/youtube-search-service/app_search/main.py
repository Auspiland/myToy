from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from search_osh import search_by_title
from schemas import SearchQuery

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# from fastapi.middleware.cors import CORSMiddleware

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # 개발용, 배포 시 도메인 지정
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


@app.get("/search", response_class=HTMLResponse)
async def search_form(request: Request):
    return templates.TemplateResponse("search.html", {"request": request})

@app.post("/search/find")
async def search_api(data: SearchQuery):
    results = search_by_title(index="script_index", query=data.query)
    return JSONResponse(content={"results": results})
