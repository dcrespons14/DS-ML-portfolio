from . import handle_requests
import warnings
import pandas as pd


SCHEMA = {
    "meeting_key": "Int64",
    "session_key": "Int64",
    "stint_number": "Int64",
    "driver_number": "Int64",
    "lap_start": "Int64",
    "lap_end": "Int64",
    "compound": "string",
    "tyre_age_at_start": "Int64"
}


def fetch(session_keys, base_url: str = "https://api.openf1.org/v1", schema: dict = SCHEMA) -> pd.DataFrame:
    """
    Fetch all stints from OpenF1 API for given sessions.

    Parameters
    ----------
    session_keys : list or pd.Series
        List of session keys to fetch stints from.
    base_url : str, optional
        Base OpenF1 URL.
    schema : dict, optional
        Dictionary that defines dtypes by column.

    Returns
    -------
    pd.DataFrame
        DataFrame containing stint data. Returns empty DataFrame if no results are found.
    """
    if isinstance(session_keys, pd.Series): session_keys = session_keys.to_list()

    params_set = handle_requests.build_params_set(filters={'session_key': session_keys})
    stint_list = handle_requests.fetch_all_requests(params_set=params_set, base_url=base_url, endpoint="stints")

    if not stint_list:
        warnings.warn("No stints found for given session keys", UserWarning)
        return pd.DataFrame()
    return (
        handle_requests.apply_schema(pd.DataFrame(stint_list), schema)
            .sort_values(by=['session_key', 'driver_number', 'stint_number'])
            .reset_index(drop=True)
    )
