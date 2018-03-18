#-*-coding:utf-8-*-
import sqlite3


class SqlLiteDB:
    def __init__(self, dbName):
        if ".db" not in dbName:
            self.db = sqlite3.connect(dbName+".db")
        else:
            self.db = sqlite3.connect(dbName)
        self.cursor = self.db.cursor()

    def createTable(self, tableName, **columnNames):
        columns = ""
        for i in columnNames:
            columns += "%s %s, " %(i, columnNames[i])
        columns = columns[0:len(columns)-2]
        tableName = tableName.replace(" ", "_")
        command = "create table if not exists %s (%s)" %(tableName, columns)
        self.cursor.execute(command)
        self.__commit()

    def deleteTable(self, tableName):
        command = "Drop table if exists %s" %(tableName)
        self.cursor.execute(command)

    def execute(self, command, *values):
        rtn = self.cursor.execute(command, values).fetchall()
        self.__commit()
        return rtn

    def __commit(self):
        self.db.commit()
