# backend/app/schemas.py
from pydantic import BaseModel

class QueryRequest(BaseModel):
    question: str

class FAQItem(BaseModel):
    id: int | None
    question: str
    answer: str
