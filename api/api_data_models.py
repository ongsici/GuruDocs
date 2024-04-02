from pydantic import BaseModel
from typing import List

class FilePath(BaseModel):
    file_path: str

class QueryInput(BaseModel):
    model_option: str
    vectorstore_id: str
    user_query: str

class SummaryInput(BaseModel):
    model_option: str
    pages_id: str