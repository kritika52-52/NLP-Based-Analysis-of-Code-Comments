"""NLP pipeline: extract -> clean -> normalize -> tokenize -> stopwords -> stem -> classify."""
import re
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from dataset import DATA

STOP = set("a an the is are was were be been to of in on at for and or it this that with as by from so we then".split())
STEM = PorterStemmer()
_TOKEN = re.compile(
    r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*.*?\*/', re.S)


# ---------- 1. Comment extraction from Java source ----------
def extract_comments(java_src: str):
    out = []
    for m in _TOKEN.finditer(java_src):
        t = m.group(0)
        if t.startswith("//"): kind = "line"
        elif t.startswith("/**"): kind = "javadoc"
        elif t.startswith("/*"): kind = "block"
        else: continue  # string / char literal
        line = java_src.count("\n", 0, m.start()) + 1
        out.append({"line": line, "type": kind, "raw": t, "text": clean(t)})
    return [c for c in out if c["text"]]


def clean(raw: str) -> str:
    lines = [re.sub(r"^\s*(/\*+|\*/|\*+|//+)\s?", "", l).replace("*/", "").strip() for l in raw.splitlines()]
    return " ".join(l for l in lines if l).strip()


# ---------- 2. Normalization / tokenization / stemming ----------
def normalize(text: str) -> str:
    t = re.sub(r"([a-z])([A-Z])", r"\1 \2", text)          # camelCase -> camel Case
    t = re.sub(r"@(\w+)", r" at_\1 ", t)                    # keep Javadoc tags as features
    t = re.sub(r"#\d+|\b\d+\b", " num ", t)                 # numbers / issue refs
    sym = len(re.findall(r"[;{}()=<>\[\]]", t))             # code-like symbols
    t = t.lower() + (" codesym" * min(sym, 3))
    return t


def tokenize(text: str):
    return re.findall(r"[a-z][a-z_]*", text)


def preprocess(text: str, detail=False):
    norm = normalize(text)
    toks = tokenize(norm)
    nostop = [w for w in toks if w not in STOP]
    stems = [STEM.stem(w) for w in nostop]
    if detail:
        return {"normalized": norm, "tokens": toks, "no_stopwords": nostop, "stems": stems}
    return " ".join(stems)


# ---------- 3. Classifier ----------
class CommentClassifier:
    def __init__(self):
        X, y = [], []
        for label, texts in DATA.items():
            for t in texts:
                X.append(preprocess(t)); y.append(label)
        Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)
        self.model = make_pipeline(
            TfidfVectorizer(tokenizer=str.split, token_pattern=None, lowercase=False, ngram_range=(1, 2)),
            LogisticRegression(max_iter=2000, C=10))
        self.model.fit(Xtr, ytr)
        self.report = classification_report(yte, self.model.predict(Xte), output_dict=True, zero_division=0)
        self.model.fit(X, y)  # final model on all data

    def predict(self, text: str):
        p = self.model.predict_proba([preprocess(text)])[0]
        probs = dict(zip(self.model.classes_, p))
        best = max(probs, key=probs.get)
        return best, probs
