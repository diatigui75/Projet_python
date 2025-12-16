import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity

class SearchEngine:
    def __init__(self, corpus):
        self.corpus = corpus
        self.vocab = self.corpus.build_vocab()
        self.mat_TF = self.corpus.build_tf_matrix(self.vocab)
        self.mat_TFxIDF = self.corpus.build_tfidf_matrix(self.mat_TF, self.vocab)

    def search(self, query, k=5):
        query_vector = self.corpus.query_to_vector(query, self.vocab, self.mat_TFxIDF)
        similarities = cosine_similarity(query_vector.reshape(1, -1), self.mat_TFxIDF)
        top_k_indices = np.argsort(similarities[0])[-k:][::-1]
        results = []
        for idx in top_k_indices:
            doc = list(self.corpus.id2doc.values())[idx]
            results.append({
                "titre": doc.titre,
                "auteur": doc.auteur,
                "score": similarities[0][idx]
            })
        return pd.DataFrame(results)
