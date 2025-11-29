# backend/app/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .database import get_db_connection
from .schemas import QueryRequest, FAQItem
from .ml_utils import predict_answer
import sqlite3

app = FastAPI(title="Student FAQ Bot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # на проді — задайте конкретний домен
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/faqs")
def list_faqs():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, question, answer FROM faqs")
    rows = cur.fetchall()
    conn.close()
    return [{"id": r["id"], "question": r["question"], "answer": r["answer"]} for r in rows]

@app.post("/api/query")
def query_bot(req: QueryRequest):
    q = req.question.strip()
    if not q:
        raise HTTPException(status_code=400, detail="Empty question")
    answer = predict_answer(q)
    if answer:
        return {"answer": answer, "source":"ml"}
    # Якщо модель не впевнена — робимо Fallback: найпростіший пошук по схожості (LIKE)
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT answer FROM faqs WHERE question LIKE ? LIMIT 1", ('%'+q+'%',))
    row = cur.fetchone()
    conn.close()
    if row:
        return {"answer": row["answer"], "source":"db_like"}
    return {"answer": "Вибачте, я не знаю відповіді на це питання. Ви можете звернутися до деканату.", "source":"none"}

@app.post("/api/faqs")
def add_faq(item: FAQItem):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO faqs (question, answer) VALUES (?, ?)", (item.question, item.answer))
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return {"id": new_id, "question": item.question, "answer": item.answer}

@app.delete("/api/faqs/{faq_id}")
def delete_faq(faq_id: int):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM faqs WHERE id = ?", (faq_id,))
    conn.commit()
    conn.close()
    return {"deleted_id": faq_id}
