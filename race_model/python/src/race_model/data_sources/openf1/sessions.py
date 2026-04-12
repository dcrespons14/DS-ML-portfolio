import requests
import time
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
import warnings



SESSIONS_SCHEMA = {
    "session_key": "int",
    "session_type": "string",
    "session_name": "string",
    "date_start": "datetime",
    "date_end": "datetime",
    "meeting_key": "int",
    "circuit_key": "int",
    "circuit_short_name": "string",
    "country_key": "int",
    "country_code": "string",
    "country_name": "string",
    "location": "string",
    "gmt_offset": "timedelta",
    "year": "int"
}



def fetch(
        years: list = [None],
        circuit_names: list = [None],
        session_names: list = ["Race"],
        url: str = "https://api.openf1.org/v1/sessions",
        schema: dict = SESSIONS_SCHEMA
) -> pd.DataFrame:
    """
    Fetch dataframe of sessions from OpenF1 API based on user filters.

    Parameters
    ----------
    years : list, optional
        List of years to filter session (e.g., [2023, 2024]).
        Use [None] to include all years.
    circuit_names : list, optional
        List of circuit short names (e.g., ["Monza", "Melbourne"]).
        Use [None] to include all circuits.
    session_names : list, optional
        List of session types (e.g., ["Qualifying", "Race"]).
        Defaults to ["Race"].
    url : str, optional
        OpenF1 sessions endopoint URL.

    Returns
    -------
    pd.DataFrame
        DataFrame containing session data. Returns empty DataFrame if no results are found.
    """

    params_set = _build_params_set(years, circuit_names, session_names)

    session_list = _fetch_all_requests(params_set, url)

    if not session_list:
        warnings.warn("No sessions found for given inputs", UserWarning)
        return pd.DataFrame()
    return _apply_schema(pd.DataFrame(session_list), schema).sort_values(by='date_start').reset_index(drop=True)


def _build_params_set(years, circuit_names, session_names) -> list:
    """
    Build a list of parameter dictionaries for API requests.
    """

    params_set = []
    
    for y in years:
        for c in circuit_names:
            for s in session_names:
                params = {}

                if y is not None: params["year"] = y
                if c is not None: params["circuit_short_name"] = c
                if s is not None: params["session_name"] = s

                params_set.append(params)

    return params_set


def _fetch_single_request(params, url, retries=5):
    """
    Fetch a single OpenF1 API request with retry and rate-limit handling.
    """

    for i in range(retries):
        r = requests.get(url, params=params, timeout=30)

        if r.status_code == 404:  # Session does not exist
            return []

        if r.status_code == 429:  # Too many requests, sleep and try again
            time.sleep(0.1 * i)
            continue

        r.raise_for_status()
        return r.json()
    return []


def _fetch_all_requests(param_set, url) -> list:
    """
    Execute multiple OpenF1 API requests in parallel and aggregate results.
    """
    session_list = []
    
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(_fetch_single_request, p, url) for p in param_set]

        for f in as_completed(futures):
            data = f.result()
            if data:
                session_list.extend(data)

    return session_list


def _apply_schema(df: pd.DataFrame, schema: dict) -> pd.DataFrame:
    """
    Apply the datatime defualt schema to ensure consistency.
    """
    for col, dtype in schema.items():
        if dtype == "datetime":
            df[col] = pd.to_datetime(df[col], errors="coerce")
        elif dtype == "timedelta":
            df[col] = pd.to_timedelta(df[col], errors="coerce")
        else:
            df[col] = df[col].astype(dtype)

    return df
