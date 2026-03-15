import streamlit as st
import src.utils as utils
from src.preprocessing import preprocess_text
from sklearn.feature_extraction.text import TfidfVectorizer
from src.search_engine import search_projects
from src.db import insert_query
import re
import os


@st.cache_resource
def build_search_engine():
    """
    Builds the project documentation search engine.

    Loads all project documentations and preprocess the texts.
    Constructs a TF-IDF representation of the project descriptions that can 
    be used to compute similarities with user queries.

    Returns
    -------
    projects: pd.DataFrame
        DataFrame containing information from all projects.
    vectorizer: TfidfVectorizer
        Fitted TF-IDF vectorizer.
    tfidf_matrix: scipy.sparse.csr_matrix
        TF-IDF matrix of preprocessed project documentations.
    """
    projects = utils.load_documentation_files()

    vectorizer = TfidfVectorizer(
        tokenizer=lambda x: x,
        token_pattern=None,
        lowercase=False
    )

    tfidf_matrix = vectorizer.fit_transform(
        projects["description"].apply(preprocess_text)
    )

    return projects, vectorizer, tfidf_matrix


def format_result(project_name: str, project_folder: str, introduction: str, snippet: str, similarity: str) -> str:
    """
    Formats a project search result as HTML for display in Streamlit.
    
    Parameters
    ----------
    project_name: str
        Project name.
    project_folder: str
        Project folder (used to generate a hyperlink to GitHub).
    introduction: str
        Project's introduction.
    snippet: str
        Description snippet.
    similarity: str
        Project description's similarity with user's query.

    Returns
    -------
    str
        String of HTML representing the formatted search result.

    """

    html = f"""
    <style>
    .project-container {{
        margin-bottom:20px;
        font-family: sans-serif;
    }}
    .project-header {{
        display:flex;
        justify-content:space-between;
        align-items:center;
        font-size:20px;
        font-weight:bold;
    }}
    .project-name {{
        color:#1a0dab;
    }}
    .project-link,
    .project-link:link,
    .project-link:visited,
    .project-link:hover,
    .project-link:active {{
        color:#6c757d;
        text-decoration:underline;
        font-size:16px;
        font-weight:normal;
    }}
    .project-intro {{
        color:#4d5156;
        font-size:16px;
    }}
    .project-snippet {{
        color:#6c757d;
        font-size:14px;
        font-style:italic;
    }}
    .project-similarity {{
        color:#4169e1;
        font-size:14px;
        text-align:right;
    }}

    /* Dark mode overrides */
    @media (prefers-color-scheme: dark) {{
        .project-name {{ color:#90bbff; }}
        .project-link,
        .project-link:link,
        .project-link:visited,
        .project-link:hover,
        .project-link:active {{
            color:#b0b0b0;
        }}
        .project-intro {{ color:#e0e0e0; }}
        .project-snippet {{ color:#b0b0b0; }}
        .project-similarity {{ color:#aaccff; }}
    }}
    </style>

    <div class="project-container">
        <div class="project-header">
            <span class="project-name">{project_name}</span>
            <a href="https://github.com/dcrespons14/DS-ML-portfolio/tree/main/{project_folder}" 
            class="project-link" target="_blank">
            GitHub Link
            </a>
        </div>
        <div class="project-intro">{introduction}</div>
        <div class="project-snippet">{snippet}</div>
        <div class="project-similarity">{similarity}</div>
    </div>
    """
    return html


def format_introduction(introduction: str, query: str, max_words: int = 80) -> str:
    """
    Formats the project's introduction by highlighting terms that appear in the query
    and limiting the length to a maximum number of words.
    
    Parameters
    ----------
    introduction: str
        Raw project's introduction text.
    query: str
        User's search query; terms in this query will be highlighted.
    max_words: int, optional
        Maximum numbers of words to display (default 70).

    Returns
    -------
    str
        Formatted introduction with highlighted query terms and truncated to maximum number of words to display.
    """
    
    # Highlight query terms
    terms = query.split()
    for term in terms:
        term_esc = re.escape(term)
        introduction = re.sub(f"\\b({term_esc}\\w*)\\b", r"<b>\1</b>", introduction, flags=re.IGNORECASE)

    # Limit words count
    words = re.split(r'(\s+)', introduction)
    truncated = []
    count = 0
    for w in words:
        if not w.isspace():
            count += 1
        if count > max_words:
            break
        truncated.append(w)
    introduction = ''.join(truncated) + ("..." if count > max_words else "")

    return introduction


def description_snippet(description: str, query: str, max_words: int = 60) -> str:
    """
    Extracts a snippet with the highest density of query terms on the project description and highlights them.

    Parameters
    ----------
    description : str
        Full project description text.
    query : str
        User's search query; terms in this query will be highlighted.
    max_words : int, optional
        Maximum number of words in the snippet (default 40).

    Returns
    -------
    str
        Snippet with highlighted query terms.
    """
    words = description.split()
    if not words:
        return ""
    
    query_terms = [t.lower() for t in query.split()]
    
    # Find the best snippet window (with the most matches)
    best_start = 0
    max_count = 0
    for i in range(len(words)):
        window = words[i:i + max_words]
        count = sum(any(w.lower().startswith(term) for term in query_terms) for w in window)
        if count > max_count:
            max_count = count
            best_start = i
    
    # Center the middle match within the best window
    window_words = words[best_start:best_start + max_words]
    match_indices = [i for i, w in enumerate(window_words) if any(w.lower().startswith(term) for term in query_terms)]

    if match_indices:
        middle_idx = match_indices[len(match_indices) // 2]
        center_offset = max_words // 2
        shift = middle_idx - center_offset
        if shift > 0:
            best_start += shift
            window_words = words[best_start:best_start + max_words]

    snippet_text = " ".join(window_words)

    # Highlight query terms
    for term in query_terms:
        term_esc = re.escape(term)
        snippet_text = re.sub(rf'\b({term_esc}\w*)\b', r'<b>\1</b>', snippet_text, flags=re.IGNORECASE)

    # Add ellipsis if snippet is not at start or end of description
    prefix = "..." if best_start > 0 else ""
    suffix = "..." if best_start + len(window_words) < len(words) else ""
    
    return f"{prefix}{snippet_text}{suffix}"


def main():
    """
    Runs the Streamlit application.

    Initializes the user interface, loads the project seaerch engine, 
    processes the user query, and displays the ranked project results.
    """
    st.set_page_config(
        page_title="Project Search",
        page_icon="🔎",
        layout="wide"
    )

    st.title("Project Search")
    st.write("Search across portfolio documentation to find the most relevant projects using keywords (e.g., pandas, SQL, or neural network).")

    projects, vectorizer, tfidf_matrix = build_search_engine()

    query = st.text_input("Search projects")

    if query:      
        results = search_projects(
            query,
            projects,
            vectorizer,
            tfidf_matrix
        )

        relevant_results = (
            results[results["similarity"] > 0.01]
            .sort_values(by="similarity", ascending=False)
            .reset_index(drop=True)
        )

        if not relevant_results.empty:
            for _, row in relevant_results.iterrows():
                st.markdown("---")
                st.markdown(
                    format_result(
                        row["project_name"],
                        row["folder"],
                        format_introduction(row["introduction"], query),
                        description_snippet(row["description"], query),
                        f"Similarity score: {row.similarity * 100:.1f}%"
                    ),
                    unsafe_allow_html=True
                )
        else:
            st.info("Sorry, no projects matched your search. You can try something else.")

        try:
            insert_query(query, os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY"))
        except:
            pass  # Ignore errors if query can't be inserted


if __name__ == "__main__":
    main()
