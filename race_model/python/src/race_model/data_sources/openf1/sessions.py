import pandas as pd
from . import handle_requests
import warnings


SCHEMA = {
    "session_key": "Int64",
    "session_type": "string",
    "session_name": "string",
    "date_start": "datetime",
    "date_end": "datetime",
    "meeting_key": "Int64",
    "circuit_key": "Int64",
    "circuit_short_name": "string",
    "country_key": "Int64",
    "country_code": "string",
    "country_name": "string",
    "location": "string",
    "gmt_offset": "timedelta",
    "year": "Int64"
}


def fetch(
        years: list = [None],
        circuit_names: list = [None],
        session_names: list = ["Race"],
        base_url: str = "https://api.openf1.org/v1",
        schema: dict = SCHEMA
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
    base_url : str, optional
        Base OpenF1 URL.
    schema : dict, optional
        Dictionary that defines dtypes by column.

    Returns
    -------
    pd.DataFrame
        DataFrame containing session data. Returns empty DataFrame if no results are found.
    """

    params_set = handle_requests.build_params_set(filters={'year': years, 'circuit_short_name': circuit_names, 'session_name': session_names})
    session_list = handle_requests.fetch_all_requests(params_set=params_set, base_url=base_url, endpoint="sessions")

    if not session_list:
        warnings.warn("No sessions found for given inputs", UserWarning)
        return pd.DataFrame()
    return handle_requests.apply_schema(pd.DataFrame(session_list), schema).sort_values(by='date_start').reset_index(drop=True)
