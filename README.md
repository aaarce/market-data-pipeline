# Market Data Pipeline (API → Features → CSV/SQLite)

A small, **config-driven** data pipeline that fetches market prices from the **CoinGecko API**, caches raw responses, engineers time-series features (returns, moving averages, volatility, drawdown), and persists outputs to **CSV** and **SQLite**. Includes a simple visualization script that saves a plot image.

## Quickstart
```bash
pip install -r requirements.txt
python -m src.cli --config config.yaml
python -m src.viz --config config.yaml
```

## Outputs
- CSV: `data/processed/market_features.csv`
- SQLite: `db/market.db` (table: `market_features`)
- Figure: `results/figures/price_ma.png`
