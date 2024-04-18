import joblib
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

data_file = 'project/datatest.pkl'
data = joblib.load(data_file)
tfidf_matrix = data['tfidf_matrix']

# Reduce to 2 dimensions for visualization
pca = PCA(n_components=2)
reduced_data = pca.fit_transform(tfidf_matrix.toarray()) 

# Simple plot
plt.scatter(reduced_data[:, 0], reduced_data[:, 1])
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.title("2D Visualization of Documents")
plt.show()
