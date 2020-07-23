import news_aggregator
import database_manager
import numpy as np
from scipy.sparse.dia import dia_matrix
from sklearn.feature_extraction.text import TfidfVectorizer

class NewsEmbedder:
    def getEmbeddingMatrix(self, articleTexts):
        vectorizer = TfidfVectorizer(min_df=1, stop_words="english")
        tfidf = vectorizer.fit_transform(articleTexts)
        pairwise_similarity = tfidf * tfidf.T 
        return pairwise_similarity.toarray()    



