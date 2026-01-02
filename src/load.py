from __future__ import annotations
from pathlib import Path
import sqlite3
import pandas as pd
from .util import ensure_dir

def save_csv(df: pd.DataFrame, processed_dir: str | Path, name: str) -> Path:
    pdir = ensure_dir(processed_dir)
    out = pdir / name
    df.to_csv(out, index=False)
    return out

def upsert_sqlite(df: pd.DataFrame, sqlite_path: str | Path, table: str = "market_features") -> None:
    sp = Path(sqlite_path)
    ensure_dir(sp.parent)
    with sqlite3.connect(sp) as con:
        df.to_sql(table, con, if_exists="replace", index=False)
