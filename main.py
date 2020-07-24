import news_aggregator
import news_embedder
import news_recommender
import database_manager
import time

import numpy as np

sources = ["http://cnn.com","http://www.nytimes.com","https://www.foxnews.com/"]


databaseManager = database_manager.DatabaseManager("articles.db")
newsRecommender = news_recommender.NewsRecommender(databaseManager)
newsManager = news_aggregator.NewsAggregator(databaseManager)
newsEmbedder = news_embedder.NewsEmbedder(databaseManager)

# Update 
#newsManager.updateDatabase(sources, 20,databaseManager)
#newsEmbedder.updateEmbeddingMatrix(databaseManager)

articles=newsRecommender.similarArticles("http://www.nytimes.com/2020/07/23/nyregion/coronavirus-testing-nyc.html",0.17)
titles=[article[1] for article in articles]
print(titles)