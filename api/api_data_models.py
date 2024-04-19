from pydantic import BaseModel
from typing import List

class FormDataInput(BaseModel):
    model: str
    files: List[str]

class QueryInput(BaseModel):
    model_option: str
    vectorstore_id: str
    user_query: str

class newQueryInput(BaseModel):
    model_option: str
    vectorstore_id: str
    user_query: str
    # session_id: str

class SummaryInput(BaseModel):
    model_option: str
    pages_id: List[str]