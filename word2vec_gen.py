import os
from bs4 import BeautifulSoup
from gensim.models import Word2Vec
import gensim
import joblib

# Function to clean and preprocess text
def clean_text(text):
    """Remove unwanted characters and extra spaces from text."""
    text = text.replace('\n', ' ').replace('\r', '')
    text = ' '.join(text.split())
    return text

def extract_text_from_html(file_path):
    """Extract and clean text from an HTML file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        contents = file.read()
        soup = BeautifulSoup(contents, 'html.parser')
        text = soup.get_text()
        cleaned_text = clean_text(text)
        return cleaned_text

def process_directory(directory):
    """Process each HTML file in the specified directory and collect cleaned text."""
    documents = []
    for filename in os.listdir(directory):
        if filename.endswith('.html'):
            file_path = os.path.join(directory, filename)
            text = extract_text_from_html(file_path)
            documents.append(text)
    return documents

def preprocess_documents(documents):
    """Preprocess documents for Word2Vec training."""
    return [gensim.utils.simple_preprocess(doc) for doc in documents]

# Specify the directory containing HTML documents
docs_directory = '/[FLASK] main/docs'
documents = process_directory(docs_directory)
processed_docs = preprocess_documents(documents)

# Train a Word2Vec model
model = Word2Vec(processed_docs, vector_size=100, window=5, min_count=2, workers=4)

# Convert model to a format that can be pickled
model_to_save = model.wv
model_to_save.save_word2vec_format('model.bin', binary=True)

# Alternatively, you can use joblib to save the model
joblib.dump(model_to_save, 'word2vec_model2.pkl')

print("Word2Vec model has been trained and saved successfully as a .pkl file.")
