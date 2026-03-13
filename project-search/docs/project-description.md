# Project search

## Project description

**Project search** is a search-based recommender system designed to help users navigate this portfolio of projects by topic, frameworks, or technologies. It ranks projects based on relevance to user queries using **TF-IDF vectorization** and **cosine similarity**.

The app compiles a corpus of documents such as this one (using the `os` library) to build a pandas dataframe with 1-gram tokenization. The pre-processing includes:
- Removal of common Markdown characters like hastags, asteriscs and similar using the regular expression library `re`.
- 1-gram tokenisation.
- Lower case conversion.
- Removal of stop words using the English stopwords list from `nltk.corpus`.
- Stemming using a Lancaster stemmer algorithm `nltk.stem.LancasterStemmer` to reduce words to their root forms.

The system uses **TF-IDF vectorization** to create a multidimensional vector space representing the repository corpus. **Cosine similatiry** is then used to match user queries against this space, returning the most relevant projects.

The app is hosted on `Streamlit` and can be accessed at: https://portfolio-search.streamlit.app/
