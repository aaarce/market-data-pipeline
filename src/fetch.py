from __future__ import annotations
import json, logging
from pathlib import Path
from typing import Any
import requests
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from .util import ensure_dir, stable_cache_key

log = logging.getLogger(__name__)

class ApiError(RuntimeError):
    pass

@retry(
    reraise=True,
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=1, max=20),
    retry=retry_if_exception_type((requests.RequestException, ApiError)),
)
def _get_json(url: str, params: dict[str, Any], timeout: int = 30) -> dict[str, Any]:
    r = requests.get(url, params=params, timeout=timeout)
    if r.status_code == 429:
        raise ApiError("Rate limited (429)")
    r.raise_for_status()
    return r.json()

def fetch_coingecko_market_chart(
    coin_id: str,
    vs_currency: str,
    days: int,
    interval: str,
    raw_dir: str | Path,
    use_cache: bool = True,
) -> dict[str, Any]:
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {"vs_currency": vs_currency, "days": days, "interval": interval}

    raw_path = ensure_dir(raw_dir)
    key = stable_cache_key(url, params)
    cache_file = raw_path / f"{coin_id}_{key}.json"

    if use_cache and cache_file.exists():
        log.info("cache_hit coin=%s file=%s", coin_id, cache_file.name)
        return json.loads(cache_file.read_text(encoding="utf-8"))

    log.info("api_fetch coin=%s days=%s interval=%s", coin_id, days, interval)
    data = _get_json(url, params=params)
    cache_file.write_text(json.dumps(data), encoding="utf-8")
    log.info("cache_write coin=%s file=%s", coin_id, cache_file.name)
    return data
