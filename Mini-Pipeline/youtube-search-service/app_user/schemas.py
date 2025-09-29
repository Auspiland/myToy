from pydantic import BaseModel
from datetime import date

class LoadChannel(BaseModel):
    channel_name: str
    channel_code: str
