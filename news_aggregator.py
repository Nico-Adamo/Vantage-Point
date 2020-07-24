import newspaper
import time
import database_manager

sources = ["http://cnn.com","http://www.nytimes.com","https://www.foxnews.com/"]

class SingleSource(newspaper.Source):
    def __init__(self, articleURL):
        super(SingleSource, self).__init__("http://localhost")
        self.articles = [newspaper.Article(url=articleURL)]

class NewsAggregator:
    def __init__(self,databaseManager):
        self.databaseManager = databaseManager

    def getArticleData(self, sourceUrls, articlesPerSource): #Returns recent article data in the form [URL, Title, Text] 
        sourcesBuilt = [newspaper.build(source) for source in sourceUrls] #Build with memoize_articles=False if trying to build initial database
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

    def updateDatabase(self, sourceUrls, articlesPerSource):
        updatedArticles = self.getArticleData(sourceUrls,articlesPerSource)
        for article in updatedArticles:
            self.databaseManager.addArticle(article)