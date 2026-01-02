from __future__ import annotations
import argparse
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

from .config import load_config
from .util import ensure_dir

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Create a simple price + moving averages plot from pipeline output")
    p.add_argument("--config", default="config.yaml", help="Path to config.yaml")
    return p

def main() -> None:
    args = build_parser().parse_args()
    cfg = load_config(args.config)

    csv_path = Path(cfg.paths.processed_dir) / "market_features.csv"
    if not csv_path.exists():
        raise FileNotFoundError(f"Missing {csv_path}. Run: python -m src.cli --config {args.config}")

    df = pd.read_csv(csv_path)
    df = df[df["asset"] == cfg.viz.asset].copy()
    if df.empty:
        raise ValueError(f"No rows for asset='{cfg.viz.asset}'. Check config.yaml assets/viz.asset.")

    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    out_png = Path(cfg.viz.out_png)
    ensure_dir(out_png.parent)

    plt.figure(figsize=(8,4))
    plt.plot(df["date"], df["price"], label="price")
    for w in cfg.features.ma_windows:
        col = f"ma_{w}"
        if col in df.columns:
            plt.plot(df["date"], df[col], label=col)
    plt.title(f"{cfg.viz.asset} — Price and Moving Averages")
    plt.xlabel("date")
    plt.ylabel(f"price ({cfg.vs_currency})")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_png, dpi=150)
    print(f"Saved: {out_png}")
    
        # --- Drawdown plot ---
    out_dd = Path(cfg.viz.out_drawdown_png)
    ensure_dir(out_dd.parent)

    plt.figure(figsize=(8,4))
    plt.plot(df["date"], df["drawdown"], label="drawdown")
    plt.title(f"{cfg.viz.asset} — Drawdown")
    plt.xlabel("date")
    plt.ylabel("drawdown")
    plt.axhline(0, linewidth=1)
    plt.tight_layout()
    plt.savefig(out_dd, dpi=150)
    print(f"Saved: {out_dd}")

if __name__ == "__main__":
    main()
