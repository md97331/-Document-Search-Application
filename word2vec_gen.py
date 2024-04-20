import os
from bs4 import BeautifulSoup
from gensim.models import Word2Vec
import gensim
import joblib

# Function to remove unnecessary characters and whitespace
def clean_text(text):
    """
    Cleans text by replacing newlines and carriage returns with spaces and 
    collapsing multiple spaces into single spaces. This ensures consistency in the text 
    and improves the quality of the data fed into the Word2Vec model.
    """
    text = text.replace('\n', ' ').replace('\r', '')
    text = ' '.join(text.split())
    return text

def extract_text_from_html(file_path):
    """
    Extracts text from an HTML file using BeautifulSoup to parse the file, which is then 
    cleaned using the clean_text function. This helps in removing the HTML markup and 
    retrieving just the content.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        contents = file.read()
        soup = BeautifulSoup(contents, 'html.parser')
        text = soup.get_text()
        cleaned_text = clean_text(text)
        return cleaned_text

def process_directory(directory):
    """
    Processes each HTML file in the specified directory, extracts and cleans the text, and 
    compiles a list of documents. This bulk processing prepares the data for the Word2Vec model.
    """
    documents = []
    for filename in os.listdir(directory):
        if filename.endswith('.html'):
            file_path = os.path.join(directory, filename)
            text = extract_text_from_html(file_path)
            documents.append(text)
    return documents

def preprocess_documents(documents):
    """
    Tokenizes and preprocesses documents using Gensim's simple_preprocess function. This 
    standardizes the text by making it lowercase and splitting it into tokens, which is 
    essential for consistent Word2Vec training.
    """
    return [gensim.utils.simple_preprocess(doc) for doc in documents]

# Path to the directory containing HTML documents for Word2Vec training
docs_directory = './[FLASK] main/docs'  # Update the path to your documents directory
documents = process_directory(docs_directory)
processed_docs = preprocess_documents(documents)

# Train a Word2Vec model on the preprocessed documents
model = Word2Vec(processed_docs, vector_size=100, window=5, min_count=2, workers=4)

# Convert the trained model to a format suitable for pickling
model_to_save = model.wv
# Save the model in binary format for efficiency
model_to_save.save_word2vec_format('model.bin', binary=True)

# Additionally, save the model using joblib for potential compatibility with other Python code
joblib.dump(model_to_save, 'word2vec_model.pkl')

print("Word2Vec model has been trained and saved successfully!!")
