# Portfolio search

## Function reference

### src/utils.py
- `load_documentation_files(repository_path=None)`
    Loads all `project_documentation.md` files from the repository. Cleans Markdown and returns a pandas DataFrame with `project_name` and `description`.

- `clean_md(text)`
    Cleans Markdown formatting (`#`, `*`, `-`, backticks, line breaks) from text.

- `find_repository_path()`
    Automatically finds the repository root path starting from the current file and moving up the folder structure.

### src/preprocessing.py
- `preprocess_text`
    Converts text to lowercase, removes stop words and applies Lancaster stemming.

### src/search_engine.py
- `search_projects`
    Searches for projects most relevant to a user query using cosine similarity within a TF-IDF vector space.

### src/db.py
- `insert_query`
    Inserts the user query on the SQL database.

### app.py
- `build_search_engine`
    Loads all project documentations and preprocesses the texts to construct a TF-IDF representation of the project descriptions that can be used to compute similarities with user queries.

- `format_result`
    Formats a project search result as HTML for display in Streamlit.

- `format_introduction`
    Formats the project's introduction by highlighting terms that appear in the user query and limiting the length to a maximum number of words.

- `description_snippet`
    Extracts a snippet of text with the highest density of query terms on the project description and highlights them.

- `main`
    Runs the `Streamlit` application.
