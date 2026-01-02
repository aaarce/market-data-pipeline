from src.util import stable_cache_key

def test_stable_cache_key_is_deterministic():
    url = "https://example.com"
    params = {"a": 1, "b": 2}
    assert stable_cache_key(url, params) == stable_cache_key(url, params)
