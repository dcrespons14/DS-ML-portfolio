# Literature Review: Search Engines

Indexing is the process of transforming raw project content into a structured format that allows fast retrieval. The most common structure is an inverted index, where each term maps to a list of files or documents in which it appears (Ruthven et al., 2011).

The indexing process starts with data collection, where project files, source code, and documentation are gathered from the repository. These documents are then converted into machine-readable text through text extraction. The text is subsequently tokenised into individual words, normalised by converting to lowercase and removing punctuation, and filtered through stop word removal to eliminate common but uninteresting words such as “the” or “and”. Stemming is then applied, often using the Porter stemming algorithm, to reduce words to their root forms. Finally, the processed terms are stored in the index along with references to the files in which they occur.

Forming this index presents several challenges. Project files may exist in heterogeneous formats such as `.txt`, `.md`, or source code files, complicating text extraction. Linguistic challenges such as synonyms and polysemy also present a challenge, and the presence of technical terms specific to the project adds complexity. Efficient storage is another concern, as the index must allow fast access while remaining lightweight.

When a user performs a search, the query undergoes a similar processing pipeline to that used during indexing. The query is tokenised, normalised, stripped of stop words, and stemmed to ensure consistency. It is then transformed into a TF-IDF vector representation. The search engine retrieves the postings lists for the query terms from the inverted index and compares the query vector with document vectors using cosine similarity, which ensures that longer files do not receive artificially higher scores simply due to their size.

Finally, understanding user interactions can help improve the system. By examining search logs and clicked results, it is possible to identify patterns in how users navigate the repository. Over time, this behavioural data can be used to refine ranking methods and improve search relevance (Brusilovsky et al., 2007).

In conclusion, a small repository search engine relies on efficient indexing and effective ranking techniques. The combination of TF-IDF weighting and cosine similarity enables accurate relevance estimation, while careful handling of diverse file types ensures a responsive and useful search experience.

## References
Brusilovsky, P., Kobsa, A., and Wlfgang, N., 2007. *The Adaptive Web: Methods and Strategies of Web Personalization.* Berlin: Springer Berlin Heidelberg.  
Ruthven, I., and Kelly, D., 2011. *Interactive information seeking, behaviour and retrieval.* London: Facet Publishing.
