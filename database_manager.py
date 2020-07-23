import sqlite3
import numpy as np
import io

class DatabaseManager:
    def __init__(self):
        sqlite3.register_adapter(np.ndarray, self.convertNumpyToSqlite)
        sqlite3.register_converter("array", self.convertSqliteToNumpy)

    def convertNumpyToSqlite(self,arr):
        """
        https://stackoverflow.com/a/55799782/5215410 (gavin)
        """
        return arr.tobytes()

    def convertSqliteToNumpy(self,text):
        return np.frombuffer(text)

 
    def connectDatabase(self,db_file):
        return sqlite3.connect(db_file,detect_types=sqlite3.PARSE_DECLTYPES)
    
    def getSimilarityMatrix(self,db_file):
        conn = self.connectDatabase(db_file)
        cur = conn.cursor()
        cur.execute("select simMatrix from matrix")
        simMatrix = cur.fetchone()[0]
        conn.close()
        return simMatrix

    def writeSimilarityMatrix(self,db_file,array):
        conn = self.connectDatabase(db_file)
        cur = conn.cursor()
        cur.execute("create table if not exists matrix (simMatrix array)")
        cur.execute("insert or replace into matrix (simMatrix) values (?)", (array, ))
        conn.commit()
        conn.close()
    
    def addArticle(self,db_file,articleData,index):
        conn = self.connectDatabase(db_file)
        cur = conn.cursor()
        cur.execute("create table if not exists articles (id INTEGER, url TEXT, title TEXT, text TEXT)")
        cur.execute("insert into articles (id,url,title,text) values (?,?,?,?)", tuple([index] + articleData))
        conn.commit()
        conn.close()

    def getArticleByIndex(self,db_file,index):
        conn = self.connectDatabase(db_file)
        cur = conn.cursor()
        cur.execute("select * from articles where id=?",(index,))
        article = cur.fetchone()
        conn.close()
        return article

    def getArticleByURL(self,db_file,url):
        conn = self.connectDatabase(db_file)
        cur = conn.cursor()
        cur.execute("select * from articles where url=?",(url,))
        article = cur.fetchone()
        conn.close()
        return article