# CS429 Project

## Abstract
The Document Search Application is designed to provide a robust text search capability for HTML documents stored within a specific directory. The project utilizes advanced text processing techniques, including TF-IDF for term importance evaluation. The next steps involve enhancing phrase recognition with Gensim and potentially integrating more sophisticated models like Doc2Vec for improved contextual understanding.

## Overview
This solution involves a Flask web application that allows users to search for HTML documents based on their content. It leverages TF-IDF to evaluate the importance of terms within documents. The proposed system aims to improve search accuracy by recognizing phrases and contextual relationships between terms.

## Design
The system is designed to allow users to interact through a web interface where they can enter search queries and receive relevant documents. It integrates TF-IDF vectorization to handle term frequency and semantic analysis, providing a robust search capability.

## Architecture
The software architecture includes several key components:
- **Flask Web Server**: Handles HTTP requests and serves the search interface.
- **TF-IDF Vectorizer**: Processes documents to create a term frequency-inverse document frequency matrix.
- **Joblib**: Used for saving and loading precomputed models.

## Operation
To operate the software, execute the `app.py` script which starts the Flask server. Once the server is running, open a web browser and navigate to `http://localhost:5000` to access the search interface. Users can input queries into the provided form to search for documents.

### Installation
```bash
pip install flask numpy gensim nltk sklearn beautifulsoup4
python app.py
```

## Conclusion
The application successfully allows users to search for and retrieve documents based on content similarity. Initial tests indicate that the inclusion of TF-IDF and Word2Vec enhances the relevance of search results significantly. However, further tuning and integration of phrase recognition may be necessary to handle complex queries more effectively.

## Data Sources
- **Local HTML Files**: The application searches within HTML files stored under `/[FLASK] main/docs`.

## Test Cases
The testing framework involves using a variety of predefined queries to evaluate the accuracy and relevance of search results. Coverage includes testing single-word and multi-word queries to assess both TF-IDF and Word2Vec implementations.

## Source Code
The source code includes:
- `app.py`: The Flask application script.
- `requirements.txt`: Lists all Python library dependencies.

### Dependencies
- Flask
- NumPy
- Gensim
- NLTK
- Scikit-Learn
- BeautifulSoup4

## Bibliography
1. "Scrapy 2.4 documentation." Scrapy, 2021. [Scrapy Documentation](https://docs.scrapy.org/en/latest/)
2. Bird, Steven, Edward Loper, and Ewan Klein, "Natural Language Processing with Python." O'Reilly Media, 2009.
3. Pedregosa et al., "Scikit-learn: Machine Learning in Python." JMLR 12, pp. 2825-2830, 2011.
4. Rehurek, Radim and Petr Sojka. "Software Framework for Topic Modelling with Large Corpora." In Proceedings of the LREC 2010 Workshop on New Challenges for NLP Frameworks. 2010.
5. "Flask Documentation." Flask, 2021. [Flask Documentation](https://flask.palletsprojects.com/en/1.1.x/)

