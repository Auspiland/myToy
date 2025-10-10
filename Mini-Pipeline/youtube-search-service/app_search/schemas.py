from pydantic import BaseModel
from datetime import date

class SearchQuery(BaseModel):
    query: str