from pydantic import BaseModel
from datetime import date

class SearchQuery(BaseModel):
    query: str


class LoadChannel(BaseModel):
    channel_name: str
    channel_code: str

