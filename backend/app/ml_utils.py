# backend/app/ml_utils.py
import joblib
from pathlib import Path
from typing import Optional

VEC_PATH = Path(__file__).parent / "vectorizer.joblib"
CLF_PATH = Path(__file__).parent / "classifier.joblib"

vec = None
clf = None

def load_models():
    global vec, clf
    if vec is None or clf is None:
        vec = joblib.load(VEC_PATH)
        clf = joblib.load(CLF_PATH)

def predict_answer(question: str) -> Optional[str]:
    load_models()
    qv = vec.transform([question])
    pred = clf.predict(qv)
    return pred[0] if len(pred) else None
