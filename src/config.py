from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import yaml

@dataclass
class Paths:
    raw_dir: str
    processed_dir: str
    sqlite_path: str

@dataclass
class Features:
    ma_windows: list[int]
    vol_windows: list[int]

@dataclass
class Viz:
    asset: str
    out_png: str

@dataclass
class AppConfig:
    provider: str
    vs_currency: str
    days: int
    interval: str
    assets: list[str]
    paths: Paths
    features: Features
    viz: Viz

def load_config(path: str | Path) -> AppConfig:
    with open(path, "r", encoding="utf-8") as f:
        c = yaml.safe_load(f)
    return AppConfig(
        provider=c["provider"],
        vs_currency=c["vs_currency"],
        days=int(c["days"]),
        interval=c["interval"],
        assets=list(c["assets"]),
        paths=Paths(**c["paths"]),
        features=Features(**c["features"]),
        viz=Viz(**c.get("viz", {"asset": c["assets"][0], "out_png": "results/figures/price_ma.png"})),
    )
