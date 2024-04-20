# CS429 Project: Document Search Application

## Abstract
The Document Search Application is an innovative tool engineered to enhance the searchability of HTML documents. The application employs TF-IDF (Term Frequency-Inverse Document Frequency) for term importance evaluation and Word2Vec for semantic analysis. This initiative is part of an ongoing effort to augment phrase recognition capabilities and possibly integrate models like Doc2Vec for an improved understanding of document context.

## Overview
Our Flask-based web application offers users the ability to search through a corpus of HTML documents by analyzing the content using state-of-the-art natural language processing techniques. The system harnesses TF-IDF to measure word significance and utilizes Word2Vec to grasp the semantic relationships between words within the corpus. The next phase includes the advancement of phrase recognition and context understanding through potential incorporation of sophisticated models such as Doc2Vec.

## Design
The Document Search Application provides a user-friendly web interface for query submission and results display. The backend leverages TF-IDF to construct a matrix representing term importance and employs Word2Vec to capture semantic word relationships. This dual-model approach aims to deliver precise and contextually relevant search results.

## Architecture
The application's architecture encompasses the following components:
- **Flask Web Server**: Manages user requests and delivers the web interface for the search system.
- **TF-IDF Vectorizer**: Converts documents into a matrix to gauge term significance within the corpus.
- **Word2Vec**: Creates word embeddings to understand semantic similarities.
- **Joblib**: Efficiently saves and loads the machine learning models.

## Operation
### Installation and Setup
To install the required dependencies, run the following commands:
```bash
pip install Flask numpy gensim nltk scikit-learn beautifulsoup4 scrapy
```

### Running the Application
1. Clone the repository to a local directory.
2. Execute `app.py` to start the Flask web server:
```bash
python app.py
```
3. Open a web browser and navigate to `http://localhost:5000` to access the search interface.
4. Enter search queries to retrieve relevant documents based on the content.

## Conclusion
The application has demonstrated the ability to facilitate effective document retrieval based on content similarity. The integration of TF-IDF and Word2Vec has shown to significantly enhance the relevance of the search results. Future work will focus on refining the system's capability to process complex queries through advanced phrase recognition techniques.

## Data Sources
The application conducts searches on a locally hosted corpus of HTML files stored within the `./[FLASK] main/docs` directory.

## Test Cases
The application has undergone rigorous testing with a variety of queries to ensure the accuracy and relevance of the search results. Tests include single-word and multi-word queries, assessing the efficacy of both the TF-IDF and Word2Vec models.

## Source Code
The source code repository includes:
- `app.py`: The main Flask application.
- `requirements.txt`: A list specifying the Python libraries required for the project.

### Dependencies
The application utilizes several open-source libraries, listed as follows:
- **Flask**: A micro web framework for Python.
- **NumPy**: A library for large, multi-dimensional arrays and matrices.
- **Gensim**: An open-source library for unsupervised topic modeling and natural language processing.
- **NLTK (Natural Language Toolkit)**: A suite of libraries and programs for symbolic and statistical natural language processing.
- **Scikit-Learn**: A machine learning library for Python.
- **BeautifulSoup4**: A library that makes it easy to scrape information from web pages.

## Bibliography
Please reference the following sources for more information on the technologies and methodologies used in this project:
1. McKinney, Wes. "Data Structures for Statistical Computing in Python." *Proceedings of the 9th Python in Science Conference.* 445 (2010): 51-56.
2. Bird, Steven, Edward Loper, and Ewan Klein. "Natural Language Processing with Python." O'Reilly Media Inc., 2009.
3. Rehurek, Radim, and Petr Sojka. "Software Framework for Topic Modeling with Large Corpora." *Proceedings of the LREC 2010 Workshop on New Challenges for NLP Frameworks.* (2010).
4. "Flask Documentation." Pallets Projects. [Flask Documentation](https://flask.palletsprojects.com/en/1.1.x/)
5. Pedregosa, F. et al. "Scikit-learn: Machine Learning in Python." *Journal of Machine Learning Research* 12 (2011): 2825-2830.
6. "Scrapy 2.4 Documentation." Scrapy. [Scrapy Documentation](https://docs.scrapy.org/en/latest/)
7. "Beautiful Soup Documentation." Crummy. [Beautiful Soup 4.

9.0 Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

Special thanks to ChatGPT for project assistance and guidance. A nod of gratitude to random YouTube professors for their Flask tutorials which have significantly contributed to the learning process. This project wouldn't be what it is without the collective wisdom shared by the open-source community.

