from __future__ import annotations
import argparse, logging
import pandas as pd

from .config import load_config
from .fetch import fetch_coingecko_market_chart
from .transform import market_chart_to_df, add_features
from .load import save_csv, upsert_sqlite

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Market data pipeline (API -> features -> CSV/SQLite)")
    p.add_argument("--config", default="config.yaml", help="Path to config.yaml")
    p.add_argument("--no-cache", action="store_true", help="Disable API response caching")
    p.add_argument("--log-level", default="INFO", help="DEBUG/INFO/WARNING/ERROR")
    return p

def main() -> None:
    args = build_parser().parse_args()
    logging.basicConfig(
        level=getattr(logging, args.log_level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s - %(message)s"
    )
    cfg = load_config(args.config)

    frames: list[pd.DataFrame] = []
    for coin in cfg.assets:
        raw = fetch_coingecko_market_chart(
            coin_id=coin,
            vs_currency=cfg.vs_currency,
            days=cfg.days,
            interval=cfg.interval,
            raw_dir=cfg.paths.raw_dir,
            use_cache=not args.no_cache,
        )
        frames.append(market_chart_to_df(raw, coin))

    base = pd.concat(frames, ignore_index=True)
    feat = add_features(base, cfg.features.ma_windows, cfg.features.vol_windows)

    csv_path = save_csv(feat, cfg.paths.processed_dir, "market_features.csv")
    upsert_sqlite(feat, cfg.paths.sqlite_path)

    logging.getLogger(__name__).info("wrote_csv=%s rows=%d", csv_path, len(feat))
    logging.getLogger(__name__).info("wrote_sqlite=%s table=market_features", cfg.paths.sqlite_path)

if __name__ == "__main__":
    main()
