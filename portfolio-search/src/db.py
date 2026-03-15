from supabase import create_client


def insert_query(query: str, SUPABASE_URL: str, SUPABASE_KEY: str):
    """
    Inserts the user query into the SQL database.

    Parameters
    ----------
    query: str
        User query text.
    SUPABASE_URL: str
        Supabase project URL.
    SUPABASE_KEY: str
        Supabase publishable key.

    Returns
    -------
    list of dict
        A list containing the inserted rows as dictionaries.
        Returns an empty list if the insert failed.
    """
    client = create_client(SUPABASE_URL, SUPABASE_KEY)
    response = client.table("project_search_queries").insert([
        {"query": query}
    ]).execute()
    return response.data
