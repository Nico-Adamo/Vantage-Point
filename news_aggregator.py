import newspaper
import time

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
     
        articleTitles=[]
        for source in sourcesIndiv:
            if source.articles:
                article = source.articles[0]
                article.parse()
                articleTitles.append([article.url,article.title,article.text])
        return articleTitles

    