import re
import os
import numpy as np
import joblib
from bs4 import BeautifulSoup
from sklearn.preprocessing import normalize
from sklearn.feature_extraction.text import TfidfVectorizer

# Define base directories that contain the HTML files for indexing
base_dirs = ['./[FLASK] main/docs']
# For testing purposes, you can switch to a different directory
#base_dirs = ['./[DATA] testing']

def clean_text(text):
    """
    Cleans the given text by removing HTML entities, extra whitespace, and
    non-alphanumeric characters. This step is important to ensure that the
    text is clean and ready for further processing such as vectorization.
    """
    # Remove HTML entities like '&nbsp;' and replace them with a space
    text = re.sub(r'&[a-z]+;', ' ', text)
    # Replace newline, carriage returns, and tabs with a space
    text = re.sub(r'[\t\n\r]+', ' ', text)
    # Remove all characters that aren't alphanumeric or spaces/periods
    text = re.sub(r'[^a-zA-Z0-9\s.]+', '', text)
    # Collapse multiple consecutive spaces into one
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def extract_text_from_html(file_path):
    """
    Opens an HTML file, parses it, and extracts all the text. The extracted
    text is then cleaned using the clean_text function. This is an essential
    step in preparing the data for indexing and searching, as it strips away
    HTML markup and leaves only the relevant content.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        # Create a BeautifulSoup object to parse the HTML
        soup = BeautifulSoup(file, 'html.parser')
        # Extract the text content from the parsed HTML
        text = soup.get_text()
    # Return the cleaned text
    return clean_text(text)

def normalize_matrix(matrix):
    """
    Normalizes the rows of a given matrix. Normalization is a key step when
    preparing text for machine learning, as it ensures that the magnitude
    of the vector does not affect the algorithm's ability to learn from the
    data.
    """
    # Normalize using L2 norm, so each output vector has a unit norm
    return normalize(matrix, norm='l2', axis=1)

# Name of the data file to store the index
data_file = 'inv_index.pkl'

# Check if the index has already been built and saved to avoid redundant work
if not os.path.exists(data_file):
    # Initialize empty lists to store documents and filenames
    documents = []
    file_names = []

    # Iterate over the base directories
    for base_dir in base_dirs:
        # Walk through the directory structure
        for dirpath, dirnames, filenames in os.walk(base_dir):
            # Process each HTML file
            for filename in filenames:
                if filename.endswith('.html'):
                    # Create a full file path to open
                    file_path = os.path.join(dirpath, filename)
                    # Extract and clean text from the HTML file
                    text = extract_text_from_html(file_path)
                    # Add the cleaned text to the list of documents
                    documents.append(text)
                    # Also, keep track of the file names
                    file_names.append(filename)

    # Initialize a TF-IDF vectorizer, excluding common English stop words
    vectorizer = TfidfVectorizer(stop_words='english')
    # Transform the documents into a sparse matrix of TF-IDF features
    tfidf_matrix = vectorizer.fit_transform(documents)
    # Normalize the TF-IDF matrix
    normalized_tfidf_matrix = normalize_matrix(tfidf_matrix)

    # Save all necessary objects (vectorizer, matrix, filenames) for searching
    data = {
        'vectorizer': vectorizer,
        'tfidf_matrix': normalized_tfidf_matrix,
        'file_names': file_names
    }
    # Use joblib for efficient serialization of large NumPy arrays
    joblib.dump(data, data_file)
    print("Index built and data saved.")
else:
    # If the data has already been processed and saved, no need to redo it
    print("Data file already exists. Loading skipped.")
