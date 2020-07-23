import newspaper
import time
import database_manager

sources = ["http://cnn.com","http://www.nytimes.com","https://www.foxnews.com/"]

class SingleSource(newspaper.Source):
    def __init__(self, articleURL):
        super(SingleSource, self).__init__("http://localhost")
        self.articles = [newspaper.Article(url=articleURL)]

class NewsAggregator:
    def getArticleData(self, sourceUrls, articlesPerSource): #Returns recent article data in the form [URL, Title, Text] 
        sourcesBuilt = [newspaper.build(source, memoize_articles=False) for source in sourceUrls]
        sourceArticles = [source.articles[:articlesPerSource] for source in sourcesBuilt]
        urls = [item.url for sublist in sourceArticles for item in sublist]
        sourcesIndiv = [SingleSource(articleURL=u) for u in urls]

        newspaper.news_pool.set(sourcesIndiv)
        newspaper.news_pool.join()
     
        articleData=[]
        for source in sourcesIndiv:
            if source.articles:
                article = source.articles[0]
                article.parse()
                articleData.append([article.url,article.title,article.text])
        return articleData

    def updateDatabase(self, sourceUrls, articlesPerSource, db_file):
        updatedArticles = self.getArticleData(sourceUrls,articlesPerSource)
        databaseManager = database_manager.DatabaseManager()
        for i in range(len(updatedArticles)):
            databaseManager.addArticle(db_file,updatedArticles[i],i)