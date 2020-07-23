import news_aggregator 
from sklearn.feature_extraction.text import TfidfVectorizer

class NewsEmbedder:
    def getEmbeddingMatrix(self, articleTexts):
        vectorizer = TfidfVectorizer(min_df=1, stop_words="english")
        tfidf = vectorizer.fit_transform(articleTexts)
        pairwise_similarity = tfidf * tfidf.T 
        return pairwise_similarity.toarray()

