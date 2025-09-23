from pathlib import Path
from typing import Dict, Tuple
import cv2
import numpy as np

def _preprocess(img: np.ndarray, size: Tuple[int, int] = (96, 96)) -> np.ndarray:
    if img is None:
        raise ValueError("Received None image for preprocessing.")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
    resized = cv2.resize(gray, size, interpolation=cv2.INTER_AREA)
    norm = cv2.normalize(resized, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
    return norm

def load_templates(dataset_dir: str) -> Dict[str, np.ndarray]:
    p = Path(dataset_dir)
    if not p.exists():
        raise FileNotFoundError(f"Dataset dir not found: {dataset_dir}")
    paths = sorted([*p.glob("*.png"), *p.glob("*.jpg"), *p.glob("*.jpeg")])
    if not paths:
        raise FileNotFoundError(f"No images found in {dataset_dir}")
    bank = {}
    for fp in paths:
        img = cv2.imread(str(fp), cv2.IMREAD_COLOR)
        tmpl = _preprocess(img)
        label = fp.stem.replace("_", " ").strip()
        bank[label] = tmpl
    return bank

def classify(frame_bgr: np.ndarray, bank: Dict[str, np.ndarray]) -> Tuple[str, float]:
    if not bank:
        raise ValueError("Template bank is empty.")
    query = _preprocess(frame_bgr)
    best_label, best_score = None, -1.0
    for label, tmpl in bank.items():
        if tmpl.shape != query.shape:
            tmpl_r = cv2.resize(tmpl, (query.shape[1], query.shape[0]), interpolation=cv2.INTER_AREA)
        else:
            tmpl_r = tmpl
        res = cv2.matchTemplate(query, tmpl_r, cv2.TM_CCOEFF_NORMED)
        score = float(res.max())
        if score > best_score:
            best_label, best_score = label, score
    best_score = max(0.0, min(1.0, best_score))
    return best_label, best_score
