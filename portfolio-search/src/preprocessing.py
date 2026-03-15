import nltk
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer

nltk.download('stopwords')

stemmer = LancasterStemmer()
stop_words = set(stopwords.words('english'))

def preprocess_text(text: str) -> str:
    """
    Converts text to lowercase, removes stop words, and applies Lancaster stemming.

    Parameters
    ----------
    text: str
        Raw text (from loading step).

    Returns
    -------
    tokens: list
        List of tokens from the input text.
    """
    text = text.lower()
    tokens = text.split()
    tokens = [stemmer.stem(t) for t in tokens if t not in stop_words]
    return tokens
