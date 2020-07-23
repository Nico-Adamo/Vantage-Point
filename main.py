import news_aggregator
import news_embedder
import database_manager
import time

import numpy as np

sources = ["http://cnn.com","http://www.nytimes.com","https://www.foxnews.com/"]

newsManager = news_aggregator.NewsAggregator()
newsEmbedder = news_embedder.NewsEmbedder()
databaseManager = database_manager.DatabaseManager()


newsManager.updateDatabase(sources, 10, "articles.db")
articleTest=databaseManager.getArticleByIndex("articles.db",10)
print(articleTest[0],articleTest[1])

# articleData = newsManager.getArticleData(sources,10)
# articleTexts = [articleDatum[2] for articleDatum in articleData]

#articleEmbeddings = newsEmbedder.getEmbeddingMatrix(articleTexts)

#np.fill_diagonal(articleEmbeddings, np.nan) # We don't want an article similarity with itself

#print(articleEmbeddings)
#databaseManager.writeSimilarityMatrix("articles.db",articleEmbeddings)
#data=databaseManager.getSimilarityMatrix("articles.db")

#print(articleData[14][1])
#result_idx = np.nanargmax(articleEmbeddings[14])
#print(result_idx, articleData[result_idx][1])