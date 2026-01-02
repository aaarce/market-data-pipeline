import pandas as pd
from src.transform import add_features

def test_add_features_creates_columns():
    df = pd.DataFrame({
        "asset": ["btc"] * 5,
        "date": pd.date_range("2025-01-01", periods=5).date,
        "price": [1, 2, 3, 4, 5],
    })
    out = add_features(df, ma_windows=[2], vol_windows=[2])
    assert "return_1d" in out.columns
    assert "ma_2" in out.columns
    assert "vol_2" in out.columns
    assert "drawdown" in out.columns
