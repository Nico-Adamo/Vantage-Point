import news_aggregator
import database_manager
import numpy as np
from scipy.sparse.dia import dia_matrix
from sklearn.feature_extraction.text import TfidfVectorizer

class NewsEmbedder:
    def __init__(self,databaseManager):
        self.databaseManager=databaseManager

    def getEmbeddingMatrixFromTexts(self, articleTexts):
        vectorizer = TfidfVectorizer(min_df=1, stop_words="english")
        tfidf = vectorizer.fit_transform(articleTexts)
        pairwise_similarity = tfidf * tfidf.T 
        returnArray = pairwise_similarity.toarray()
        np.fill_diagonal(returnArray,np.nan)
        return returnArray
    
    def updateEmbeddingMatrix(self):
        """
        Get articles, compute similarity matrix, update in database
        """
        articleText = [articleTuple[0] for articleTuple in self.databaseManager.getArticlePropList("text")]
        computedMatrix = self.getEmbeddingMatrixFromTexts(articleText)
        self.databaseManager.writeSimilarityMatrix(computedMatrix)