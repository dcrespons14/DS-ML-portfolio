from itertools import product
import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd


def build_params_set(filters: dict) -> list:
    """
    Build API parameter sets from a dictionary of lists.

    Parameters
    ----------
    filters : dict
        Dictionary of lists containing filders.
        Example:
            {
                "year": [2024, 2025],
                "circuit_name": ["Melbourne", "Monza"]
            }
    """

    keys = list(filters.keys())
    values = [filters[k] for k in keys]

    params_set = []

    for combo in product(*values):
        params = {
            k: v for k, v in zip(keys, combo)
            if v is not None
        }
        params_set.append(params)

    return params_set


def fetch_single_request(params, base_url, endpoint, retries=5):
    """
    Fetch a single OpenF1 API request with retry and rate-limit handling.
    """

    url = f"{base_url}/{endpoint}"

    for i in range(retries):
        r = requests.get(url, params=params, timeout=30)

        if r.status_code == 404:  # Requested item does not exist
            return []

        if r.status_code == 429:  # Too many requests, sleep and try again
            time.sleep(0.1 * i)
            continue

        r.raise_for_status()
        return r.json()
    return []


def fetch_all_requests(params_set, base_url, endpoint) -> list:
    """
    Execute multiple OpenF1 API requests in parallel and aggregate results.
    """
    results = []
    
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(fetch_single_request, p, base_url, endpoint) for p in params_set]

        for f in as_completed(futures):
            data = f.result()
            if data:
                results.extend(data)

    return results


def apply_schema(df: pd.DataFrame, schema: dict) -> pd.DataFrame:
    """
    Apply a dtype schema to a dataframe.
    """
    for col, dtype in schema.items():
        if dtype == "datetime":
            df[col] = pd.to_datetime(df[col], errors="coerce")
        elif dtype == "timedelta":
            df[col] = pd.to_timedelta(df[col], errors="coerce")
        else:
            df[col] = df[col].astype(dtype)

    return df
