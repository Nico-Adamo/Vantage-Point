import news_aggregator
import news_embedder

import numpy as np

sources = ["http://cnn.com","http://www.nytimes.com","https://www.foxnews.com/"]

newsManager = news_aggregator.NewsAggregator()
newsEmbedder = news_embedder.NewsEmbedder()

articleData = newsManager.getArticleData(sources,10)
articleTexts = [articleDatum[2] for articleDatum in articleData]

articleEmbeddings = newsEmbedder.getEmbeddingMatrix(articleTexts)
np.fill_diagonal(articleEmbeddings, np.nan) # We don't want an article similarity with itself

print(articleData[5][1])

result_idx = np.nanargmax(articleEmbeddings[5])

print(result_idx, articleData[result_idx][1])