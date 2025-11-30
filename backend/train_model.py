import sqlite3
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib
import os

DB_PATH = "app/faqs.db"
VEC_PATH = "app/vectorizer.joblib"
CLF_PATH = "app/classifier.joblib"
CSV_PATH = "faqs_seed.csv"

def create_db_and_seed(csv_path=CSV_PATH):
    df = pd.read_csv(csv_path)
    # Створюємо БД і таблицю
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS faqs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        answer TEXT NOT NULL
    )
    """)
    conn.commit()
    # Очистимо і вставимо
    cur.execute("DELETE FROM faqs")
    for _, row in df.iterrows():
        cur.execute("INSERT INTO faqs (question, answer) VALUES (?, ?)", (row['question'], row['answer']))
    conn.commit()
    conn.close()
    print("DB created and seeded.")

def train_model():
    # Завантажимо питання як X, відповідь як y (клас — індекс відповіді)
    df = pd.read_csv(CSV_PATH)
    X = df['question'].astype(str).tolist()
    # Класифікація: кожна унікальна відповідь — окремий клас
    labels = df['answer'].astype(str).tolist()
    # Векторизатор
    vec = TfidfVectorizer(ngram_range=(1,2), max_features=5000)
    Xv = vec.fit_transform(X)
    clf = LogisticRegression(max_iter=1000)
    clf.fit(Xv, labels)

    os.makedirs(os.path.dirname(VEC_PATH), exist_ok=True)
    joblib.dump(vec, VEC_PATH)
    joblib.dump(clf, CLF_PATH)
    print("Model and vectorizer saved.")

if __name__ == "__main__":
    create_db_and_seed()
    train_model()