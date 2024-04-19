from flask import Flask, request, jsonify, url_for, render_template, send_from_directory
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
from urllib.parse import quote
import joblib
import numpy as np
import os
from gensim.models import KeyedVectors

app = Flask(__name__, static_folder='docs')

# Load the precomputed data
data = joblib.load('./inv_index.pkl')  # make sure the path to your inv_index.pkl is correct
vectorizer = data['vectorizer']
tfidf_matrix = data['tfidf_matrix']
file_names = data['file_names']

# Load the Word2Vec model's KeyedVectors
w2v_model = joblib.load('./word2vec_model.pkl')  # make sure the path to your word2vec_model.pkl is correct

def get_vector(text):
    """Generate a vector for the input text using Word2Vec model."""
    words = text.split()  # Basic tokenization, consider using more sophisticated processing.
    words = [word for word in words if word in w2v_model]
    if words:
        return np.mean(w2v_model[words], axis=0)
    else:
        return np.zeros(w2v_model.vector_size)

@app.route('/', methods=['GET'])
def index():
    """Render the search form."""
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    content = request.get_json()
    query = content['query']
    if not query.strip():
        return jsonify({"error": "The query is empty or invalid.", "results": []})

    # Transform query to vectors
    query_vec_tfidf = vectorizer.transform([query]).toarray()
    query_vec_w2v = get_vector(query).reshape(1, -1)

    # Calculate cosine similarities
    similarities_tfidf = cosine_similarity(query_vec_tfidf, tfidf_matrix).flatten()
    doc_vectors_w2v = np.array([get_vector(doc) for doc in file_names])
    similarities_w2v = cosine_similarity(query_vec_w2v, doc_vectors_w2v).flatten()

    # Normalize the similarity scores
    scaler = MinMaxScaler()
    similarities_tfidf_scaled = scaler.fit_transform(similarities_tfidf.reshape(-1, 1)).flatten()
    similarities_w2v_scaled = scaler.fit_transform(similarities_w2v.reshape(-1, 1)).flatten()

    # Filter out results where either TF-IDF or Word2Vec scores are 0
    valid_indices = (similarities_tfidf_scaled > 0) & (similarities_w2v_scaled > 0)

    # Combine normalized similarities for valid indices only
    combined_similarities = np.zeros_like(similarities_tfidf_scaled)
    combined_similarities[valid_indices] = similarities_tfidf_scaled[valid_indices] + similarities_w2v_scaled[valid_indices]

    top_indices = combined_similarities.argsort()[-10:][::-1]

    results = []
    for idx in top_indices:
        if combined_similarities[idx] == 0.0:
            continue
        file_path = file_names[idx]
        file_basename = os.path.splitext(os.path.basename(file_path))[0]
        download_url = url_for('static', filename='docs/' + file_names[idx])  # make sure this path is correct
        wikipedia_url = f"https://en.wikipedia.org/wiki/{quote(file_basename.replace('_', ' '))}"

        results.append({
            "document": file_basename,
            "tfidf": round(similarities_tfidf_scaled[idx], 2),
            "similarity": round(similarities_w2v_scaled[idx], 2),
            "download_url": download_url,
            "view_url": wikipedia_url
        })

    if not results:
        return jsonify({"error": "No relevant documents found for the query.", "results": []})

    return jsonify(results=results)


@app.route('/download/<filename>')
def download_file(filename):
    """Serve a file from the documents directory."""
    return send_from_directory(app.static_folder, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
