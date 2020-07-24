import news_aggregator
import news_embedder
import news_recommender
import database_manager
import time

import numpy as np

import flask
from flask import request, jsonify

from apscheduler.schedulers.background import BackgroundScheduler
import atexit

sources = ["http://cnn.com","http://www.nytimes.com","https://www.foxnews.com/"]


databaseManager = database_manager.DatabaseManager("articles.db")
newsRecommender = news_recommender.NewsRecommender(databaseManager)
newsManager = news_aggregator.NewsAggregator(databaseManager)
newsEmbedder = news_embedder.NewsEmbedder(databaseManager)


app = flask.Flask(__name__)

def updateDatabase():
    newsManager.updateDatabase(sources, 20,databaseManager)
    newsEmbedder.updateEmbeddingMatrix(databaseManager)

@app.route('/', methods=['GET'])
def home():
    return "<h1>Vantage Point API</h1><p>This site is a prototype API for finding news articles on the same topic.</p>"

@app.route('/api/v1/articleSimilarity', methods=['GET'])
def api_url():
    # Check if an URL was provided as part of the URL Args.
    # If URL is provided, assign it to a variable.
    # If no URL is provided, display an error in the browser.
    if 'url' in request.args:
        url = request.args['url']
    else:
        return "Error: No url field provided. Please specify an url."
    
    if 'cutoff' in request.args:
        cutoff = int(request.args['cutoff'])
    else:
        cutoff = 0.17

    articles = newsRecommender.similarArticles(url,cutoff)
    articleURLText = [article[:2] for article in articles]
    return jsonify(articleURLText)


scheduler = BackgroundScheduler()
scheduler.add_job(func=updateDatabase, trigger="interval", hours=1)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

app.run()


#articles=newsRecommender.similarArticles("http://www.nytimes.com/2020/07/23/nyregion/coronavirus-testing-nyc.html",0.17)
#titles=[article[1] for article in articles]
#print(titles) 