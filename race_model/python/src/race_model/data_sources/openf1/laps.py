from . import handle_requests
import warnings
import pandas as pd


SCHEMA = {
    "meeting_key": "Int64",
    "session_key": "Int64",
    "driver_number": "Int64",
    "lap_number": "Int64",
    "date_start": "datetime",
    "duration_sector_1": "Float64",
    "duration_sector_2": "Float64",
    "duration_sector_3": "Float64",
    "i1_speed": "Float64",
    "i2_speed": "Float64",
    "is_pit_out_lap": "boolean",
    "lap_duration": "Float64",
    "segments_sector_1": "object",
    "segments_sector_2": "object",
    "segments_sector_3": "object",
    "st_speed": "Float64"
}


def fetch(session_keys, base_url: str = "https://api.openf1.org/v1", schema: dict = SCHEMA) -> pd.DataFrame:
    """
    Fetch all laps from OpenF1 API for given sessions.

    Parameters
    ----------
    session_keys : list or pd.Series
        List of session keys to fetch laps from.
    base_url : str, optional
        Base OpenF1 URL.
    schema : dict, optional
        Dictionary that defines dtypes by column.

    Returns
    -------
    pd.DataFrame
        DataFrame containing laps data. Returns empty DataFrame if no results are found.
    """
    if isinstance(session_keys, pd.Series): session_keys = session_keys.to_list()

    params_set = handle_requests.build_params_set(filters={'session_key': session_keys})
    lap_list = handle_requests.fetch_all_requests(params_set=params_set, base_url=base_url, endpoint="laps")

    if not lap_list:
        warnings.warn("No laps found for given session keys", UserWarning)
        return pd.DataFrame()
    return (
        handle_requests.apply_schema(pd.DataFrame(lap_list), schema)
            .sort_values(by=['session_key', 'driver_number', 'lap_number'])
            .reset_index(drop=True)
    )
