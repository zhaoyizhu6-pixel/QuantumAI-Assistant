import os, json
from pathlib import Path
from typing import List, Dict
import jieba
from rank_bm25 import BM25Okapi
import numpy as np

ROOT = Path(__file__).resolve().parent
DATA = ROOT / 'data'
MODEL_DIR = ROOT / 'model' / 'paraphrase-multilingual-MiniLM-L12-v2'

def load_jsonl(path: Path):
    items=[]
    if path.exists():
        for line in path.open('r',encoding='utf-8'):
            line=line.strip()
            if not line: continue
            try: items.append(json.loads(line))
            except: pass
    return items

def read_stopwords(path: Path):
    if not path.exists(): return set()
    return {w.strip() for w in path.read_text(encoding='utf-8').splitlines() if w.strip()}

class HybridIndex:
    def __init__(self, kb_items: List[Dict], stopwords_path: Path):
        self.items = kb_items
        self.stop = read_stopwords(stopwords_path)
        corpus = [[t for t in jieba.cut(it.get('question','')+' '+it.get('answer','')) if t.strip() and t not in self.stop] for it in kb_items]
        self.bm25 = BM25Okapi(corpus)
        self.vec_model=None; self.vec_matrix=None
        try:
            from sentence_transformers import SentenceTransformer
            model_path = str(MODEL_DIR) if MODEL_DIR.exists() else 'paraphrase-multilingual-MiniLM-L12-v2'
            self.vec_model = SentenceTransformer(model_path)
            texts=[(it.get('question','')+' '+it.get('answer','')).strip() for it in self.items]
            if texts:
                self.vec_matrix=self.vec_model.encode(texts, convert_to_numpy=True, show_progress_bar=False, normalize_embeddings=True)
        except Exception:
            pass
    def search(self, query: str, mode: str='hybrid', topk: int=5, alpha: float=0.6, beta: float=0.4):
        q_tokens=[t for t in jieba.cut(query) if t.strip() and t not in self.stop]
        bm25_scores=np.array(self.bm25.get_scores(q_tokens),dtype=float)
        if self.vec_model is not None and self.vec_matrix is not None and mode in ('vector','hybrid'):
            qv=self.vec_model.encode([query], convert_to_numpy=True, normalize_embeddings=True, show_progress_bar=False)[0]
            vec_scores=self.vec_matrix @ qv
        else:
            vec_scores=np.zeros_like(bm25_scores)
        final=bm25_scores if mode=='bm25' else vec_scores if mode=='vector' else alpha*bm25_scores+beta*vec_scores
        idx=np.argsort(-final)[:topk]
        return [(int(i), float(final[i]), float(bm25_scores[i]), float(vec_scores[i])) for i in idx]
    def get_item(self, i:int)->Dict:
        return self.items[i]
