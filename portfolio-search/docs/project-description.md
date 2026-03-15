# Portfolio search

## Project description

**Portfolio search** is a search-based recommender system designed to help users navigate this portfolio of projects by topic, frameworks, or technologies. It ranks projects based on relevance to user queries using **TF-IDF vectorization** and **cosine similarity**.

The app compiles a corpus of documents such as this one (using the `os` library) to build a pandas dataframe with 1-gram tokenization. The pre-processing includes:
- Removal of common Markdown characters like hastags, asteriscs and similar using the regular expression library `re`.
- 1-gram tokenisation.
- Lower case conversion.
- Removal of stop words using the English stopwords list from `nltk.corpus`.
- Stemming using a Lancaster stemmer algorithm `nltk.stem.LancasterStemmer` to reduce words to their root forms.

The system uses **TF-IDF vectorization** to create a multidimensional vector space representing the repository corpus. **Cosine similatiry** is then used to match user queries against this space, returning the most relevant projects.

User queries are logged into an SQL database (PostgreSQL hosted on Supabase) as a means of gathering feedback. Several layers of security, including RLS and the use of environment variables, are applied to guarantee confidentiality at all times.
See `docs/db.md` for further information on the database setup.

The app is hosted on `Render` and can be accessed at: https://portfolio-search.onrender.com
