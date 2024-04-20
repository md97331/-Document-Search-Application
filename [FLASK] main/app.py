from flask import Flask, request, jsonify, url_for, render_template, send_from_directory
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
from urllib.parse import quote
import joblib
import numpy as np
import os
from gensim.models import KeyedVectors

# Initialize the Flask application
app = Flask(__name__, static_folder='docs')

# Load precomputed indices and models for search functionality
data = joblib.load('./inv_index.pkl')  # Load the TF-IDF matrix and other associated data
vectorizer = data['vectorizer']  # The vectorizer used to convert queries into TF-IDF vectors
tfidf_matrix = data['tfidf_matrix']  # The TF-IDF matrix for the documents
file_names = data['file_names']  # List of filenames corresponding to the documents in the TF-IDF matrix

# Load the Word2Vec model's KeyedVectors for semantic analysis
w2v_model = joblib.load('./word2vec_model.pkl')  # This model provides word embeddings

def get_vector(text):
    """
    Generates a semantic vector for the given text by averaging the vectors of the words 
    contained in the text. This vector represents the combined meaning of the words in a 
    multi-dimensional space and is used to determine the document's relevance to a query.
    """
    words = text.split()  # Tokenize the text into words
    valid_words = [word for word in words if word in w2v_model]  # Filter words present in the model
    if valid_words:
        return np.mean(w2v_model[valid_words], axis=0)  # Average the vectors of valid words
    else:
        return np.zeros(w2v_model.vector_size)  # Return a zero vector if no valid words are found

@app.route('/', methods=['GET'])
def index():
    """
    Route to render the main search page where users can input their search queries.
    """
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    """
    Endpoint to handle search queries submitted from the search page. It calculates 
    similarity scores for the query against all documents using both TF-IDF and Word2Vec 
    vectors and returns the most relevant documents.
    """
    content = request.get_json()
    query = content['query'].strip()

    if not query:
        return jsonify({"error": "The query is empty or invalid.", "results": []})

    # Convert the query into TF-IDF and Word2Vec vectors
    query_vec_tfidf = vectorizer.transform([query]).toarray()
    query_vec_w2v = get_vector(query).reshape(1, -1)

    # Compute the cosine similarity for both TF-IDF and Word2Vec vectors
    similarities_tfidf = cosine_similarity(query_vec_tfidf, tfidf_matrix).flatten()
    doc_vectors_w2v = np.array([get_vector(doc) for doc in file_names])
    similarities_w2v = cosine_similarity(query_vec_w2v, doc_vectors_w2v).flatten()

    # Normalize the similarity scores to allow fair combination
    scaler = MinMaxScaler()
    similarities_tfidf_scaled = scaler.fit_transform(similarities_tfidf.reshape(-1, 1)).flatten()
    similarities_w2v_scaled = scaler.fit_transform(similarities_w2v.reshape(-1, 1)).flatten()

    # Combine the normalized scores, ignoring documents with a score of zero in either model
    valid_indices = (similarities_tfidf_scaled > 0) & (similarities_w2v_scaled > 0)
    combined_similarities = np.zeros_like(similarities_tfidf_scaled)
    combined_similarities[valid_indices] = similarities_tfidf_scaled[valid_indices] + similarities_w2v_scaled[valid_indices]

    if not any(valid_indices):
        print("message query not")
        return jsonify({"message": "The query did not retrieve any results."})


    # Sort the documents based on the combined similarity scores
    top_indices = combined_similarities.argsort()[-10:][::-1]

    # Construct the results to return, including metadata and URLs for download and viewing
    results = []
    for idx in top_indices:
        if combined_similarities[idx] == 0.0:
            continue  # Skip documents with a combined score of zero
        file_basename = os.path.splitext(os.path.basename(file_names[idx]))[0]
        download_url = url_for('static', filename='docs/' + file_names[idx])
        wikipedia_url = f"https://en.wikipedia.org/wiki/{quote(file_basename.replace('_', ' '))}"

        # Add document details to the results list
        results.append({
            "document": file_basename,
            "tfidf": round(similarities_tfidf_scaled[idx], 2),
            "similarity": round(similarities_w2v_scaled[idx], 2),
            "download_url": download_url,
            "view_url": wikipedia_url
        })

    # Return a JSON response with the search results
    return jsonify(results=results)

@app.route('/download/<filename>')
def download_file(filename):
    """
    Route to serve files from the document directory, allowing users to download documents 
    directly from the search results.
    """
    return send_from_directory(app.static_folder, filename, as_attachment=True)

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
