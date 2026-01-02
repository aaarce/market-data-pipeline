from __future__ import annotations
import hashlib, json
from pathlib import Path
from typing import Any

def ensure_dir(p: str | Path) -> Path:
    p = Path(p)
    p.mkdir(parents=True, exist_ok=True)
    return p

def stable_cache_key(url: str, params: dict[str, Any]) -> str:
    payload = {"url": url, "params": params}
    blob = json.dumps(payload, sort_keys=True).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()[:16]
