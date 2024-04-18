from flask import Flask, render_template, request, jsonify, url_for
import joblib
import os
from sklearn.metrics.pairwise import cosine_similarity
from urllib.parse import quote


app = Flask(__name__, static_folder='docs')

# Load the precomputed data
data = joblib.load('./inv_index.pkl')
vectorizer = data['vectorizer']
tfidf_matrix = data['tfidf_matrix']
file_names = data['file_names']

@app.route('/', methods=['GET'])
def index():
    """Render the search form."""
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    """Handle the search query submitted from the form and return results."""
    content = request.get_json()
    query = content['query']
    if not query.strip():
        return jsonify({"error": "The query is empty or invalid.", "results": []})
    
    query_vec = vectorizer.transform([query]).toarray()
    similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
    top_indices = similarities.argsort()[-10:][::-1]

    results = []
    for idx in top_indices:
        file_path = file_names[idx]
        tfidf_score = tfidf_matrix[idx].sum()
        similarity = similarities[idx]
        if similarity == 0.0:
            return jsonify({"error": "No relevant documents found for the query.", "results": []})
        file_basename = os.path.splitext(os.path.basename(file_path))[0]
        download_url = url_for('static', filename= file_names[idx], _external=True)
        wikipedia_url = f"https://en.wikipedia.org/wiki/{quote(file_basename.replace('_', ' '))}"

        results.append({
            "document": file_basename,
            "tfidf": round(tfidf_score, 2),
            "similarity": round(similarity, 2),
            "download_url": download_url,
            "view_url" : wikipedia_url
        })

    return jsonify(results=results)

@app.route('/download/<filename>')
def download_file(filename):
    """Serve a file from the documents directory."""
    return send_from_directory(app.static_folder, filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
