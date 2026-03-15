from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from src.preprocessing import preprocess_text

def search_projects(query: str, projects: pd.DataFrame, vectorizer, tfidf_matrix) -> pd.DataFrame:
    """
    Searches for projects most relevant to a user query using cosine similarity within a TF-IDF vector space.
    """
    query_tokens = preprocess_text(query)

    query_vector = vectorizer.transform([query_tokens])

    similarity_scores = cosine_similarity(query_vector, tfidf_matrix).flatten()

    results = projects.copy()
    results['similarity'] = similarity_scores

    return results.sort_values(by='similarity', ascending=False)
