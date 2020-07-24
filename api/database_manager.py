import sqlite3
import numpy as np
import io

class DatabaseManager:
    def __init__(self,db_file):
        self.db_file = db_file
        sqlite3.register_adapter(np.ndarray, self.convertNumpyToSqlite)
        sqlite3.register_converter("array", self.convertSqliteToNumpy)

    def convertNumpyToSqlite(self,arr):
        """
        https://stackoverflow.com/a/55799782/5215410 (gavin)
        """
        out = io.BytesIO()
        np.save(out, arr)
        out.seek(0)
        return sqlite3.Binary(out.read())

    def convertSqliteToNumpy(self,text):
        out = io.BytesIO(text)
        out.seek(0)
        return np.load(out)

 
    def connectDatabase(self):
        return sqlite3.connect(self.db_file,detect_types=sqlite3.PARSE_DECLTYPES)
    
    def getSimilarityMatrix(self):
        conn = self.connectDatabase()
        cur = conn.cursor()
        cur.execute("select simMatrix from matrix")
        simMatrix = cur.fetchone()[0]
        conn.close()
        return simMatrix

    def writeSimilarityMatrix(self,array):
        conn = self.connectDatabase()
        cur = conn.cursor()
        cur.execute("create table if not exists matrix (simMatrix array)")
        cur.execute("delete from matrix")
        cur.execute("insert into matrix (simMatrix) values (?)", (array, ))
        conn.commit()
        conn.close()
    
    def addArticle(self,articleData):
        conn = self.connectDatabase()
        cur = conn.cursor()
        cur.execute("create table if not exists articles (url TEXT, title TEXT, text TEXT)")
        cur.execute("insert into articles (url,title,text) values (?,?,?)", tuple(articleData))
        conn.commit()
        conn.close()

    def getArticleByIndex(self,index):
        conn = self.connectDatabase()
        cur = conn.cursor()
        cur.execute("select * from articles where rowid=?",(index+1,))
        article = cur.fetchone()
        conn.close()
        return article

    def getArticleByURL(self,url):
        conn = self.connectDatabase()
        cur = conn.cursor()
        cur.execute("select * from articles where url=?",(url,))
        article = cur.fetchone()
        conn.close()
        return article
    
    def getArticlePropList(self,prop):
        conn = self.connectDatabase()
        cur = conn.cursor()
        cur.execute("select " + prop + " from articles")
        articles = cur.fetchall()
        conn.close()
        return articles
    
    def getIndexByURL(self,url):
        conn = self.connectDatabase()
        cur = conn.cursor()
        cur.execute("select rowid from articles where url=?",(url,))
        try: 
            id = cur.fetchone()[0]-1
        except TypeError:
            id = None            
        conn.close()
        return id