# backend/app/ml_utils.py
import joblib
from pathlib import Path

BASE = Path(__file__).resolve().parent
VEC_PATH = BASE / "vectorizer.joblib"
CLF_PATH = BASE / "classifier.joblib"

vec = None
clf = None

def load_models():
    global vec, clf
    if vec is None:
        vec = joblib.load(VEC_PATH)
    if clf is None:
        clf = joblib.load(CLF_PATH)

def predict_answer(question: str):
    load_models()
    qv = vec.transform([question])
    pred = clf.predict(qv)
    return pred[0]

