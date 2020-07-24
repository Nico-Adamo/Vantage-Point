

class NewsRecommender:
    def __init__(self,databaseManager):
        self.databaseManager = databaseManager
    
    def similarArticles(self,url,cutoff):
        articleIndex = self.databaseManager.getIndexByURL(url)
        if articleIndex is None:
            return None
        similarityMatrix = self.databaseManager.getSimilarityMatrix()
        relevantArticleIndices = [i for i, x in enumerate(similarityMatrix[articleIndex]) if x>=cutoff]
        relevantArticles = [self.databaseManager.getArticleByIndex(index) for index in relevantArticleIndices]
        return relevantArticles