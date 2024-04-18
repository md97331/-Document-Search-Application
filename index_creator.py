import re
import os
import numpy as np
import joblib
from bs4 import BeautifulSoup
from sklearn.preprocessing import normalize
from sklearn.feature_extraction.text import TfidfVectorizer

# Base directories containing your HTML files
base_dirs = ['/PROJ/[FLASK] main/docs']
#base_dirs = ['/PROJ/[DATA] testing']

def extract_text_from_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        
        text = soup.get_text()
    return text


def normalize_matrix(matrix):
    """ Normalize the rows of a sparse matrix. """
    return normalize(matrix, norm='l2', axis=1)


data_file = '/PROJ/inv_index.pkl'

if not os.path.exists(data_file):
    documents = []
    file_names = []

    for base_dir in base_dirs:
        for dirpath, dirnames, filenames in os.walk(base_dir):
            for filename in filenames:
                if filename.endswith('.html'):
                    file_path = os.path.join(dirpath, filename)
                    text = extract_text_from_html(file_path)
                    documents.append(text)
                    file_names.append(filename)

    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(documents)
    normalized_tfidf_matrix = normalize_matrix(tfidf_matrix)

    # Save all necessary objects to a single file using joblib
    data = {
        'vectorizer': vectorizer,
        'tfidf_matrix': normalized_tfidf_matrix,
        'file_names': file_names
    }
    joblib.dump(data, data_file)
    print("Index built and data saved.")
else:
    print("Data file already exists. Loading skipped.")
