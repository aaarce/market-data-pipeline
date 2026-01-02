from __future__ import annotations
import pandas as pd

def market_chart_to_df(market_chart: dict, coin_id: str) -> pd.DataFrame:
    df = pd.DataFrame(market_chart["prices"], columns=["ts_ms", "price"])
    df["date"] = pd.to_datetime(df["ts_ms"], unit="ms", utc=True).dt.date
    df = df.drop(columns=["ts_ms"]).drop_duplicates(subset=["date"])
    df["asset"] = coin_id
    df = df.sort_values(["asset", "date"]).reset_index(drop=True)
    return df[["asset", "date", "price"]]

def add_features(df: pd.DataFrame, ma_windows: list[int], vol_windows: list[int]) -> pd.DataFrame:
    out = df.copy()
    out["return_1d"] = out.groupby("asset")["price"].pct_change()

    for w in ma_windows:
        out[f"ma_{w}"] = out.groupby("asset")["price"].transform(lambda s: s.rolling(w).mean())

    for w in vol_windows:
        out[f"vol_{w}"] = out.groupby("asset")["return_1d"].transform(lambda s: s.rolling(w).std())

    out["cum_max"] = out.groupby("asset")["price"].cummax()
    out["drawdown"] = (out["price"] / out["cum_max"]) - 1.0
    out = out.drop(columns=["cum_max"])
    return out
