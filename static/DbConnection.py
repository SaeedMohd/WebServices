import pyodbc
import datetime
from json import dumps


class DbConnection:
    connection = ''

    def __init__(self, host, port, dbName, username, pwd):
        self.host = host
        self.port = port
        self.username = username
        self.pwd = pwd
        self.dbName = dbName

    def myconverter(o):
        if isinstance(o, datetime.datetime):
            return o.__str__()

    def connect(self):
        self.connection = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL "
                                         "Server};Server=" + self.host + "," + self.port + ";Database=" + self.dbName + ";uid=" + self.username + ";pwd=" + self.pwd)
        return self.connection

    def disconnect(self):
        self.connection.close()

    @staticmethod
    def queryDb(queryString):
        dbConnection = DbConnection('localhost', '1401', 'Inspection', 'SA', 'InspectionDoesntHaveAStrongRootPass9211@')
        connection = dbConnection.connect()

        try:
            cursor = connection.cursor()
            cursor.execute(queryString)
            resultDict = []
            columns = [column[0] for column in cursor.description]
            lowerColumns = []
            for column in columns:
                lowerColumns.append(column.lower())
            for row in cursor.fetchall():
                resultDict.append(dict(zip(lowerColumns, row)))
            cursor.close()
            counter = 0
            return dumps(resultDict, default=DbConnection.myconverter)
        except Exception as e:
            print("the error retrieved is:" + str(e))
            if "Attempt to use a closed connection" not in str(e) and "Connection not open" not in str(
                    e) and "Communication link failure" not in str(e):
                connection.close()
            connection = DbConnection.connect()
            counter += 1
            DbConnection.queryDb(queryString)

    @staticmethod
    def queryCsiDB(queryString):
        dbConnection2 = DbConnection('192.168.75.1', '1433', 'CSI', 'devsherif', 'Xirah4Lishe8ahFae9ze')
        conn = dbConnection2.connect()
        try:
            cursor = conn.cursor()
            cursor.execute(queryString)
            resultDict = []
            columns = [column[0] for column in cursor.description]
            lowerColumns = []
            for column in columns:
                lowerColumns.append(column.lower())
            for row in cursor.fetchall():
                resultDict.append(dict(zip(lowerColumns, row)))
            cursor.close()
            counter = 0
            return dumps(resultDict, default=DbConnection.myconverter)
        except Exception as e:
            print("the error retrieved is:" + str(e))
            return str(e)
            if "Attempt to use a closed connection" not in str(e) and "Connection not open" not in str(
                    e) and "Communication link failure" not in str(e):
                conn.close()
            connection = dbConnection.connect()
            counter += 1
            queryDb(queryString)

    @staticmethod
    def updateCsiDB(updateStatement):
        dbConnection2 = DbConnection('192.168.75.1', '1433', 'CSI', 'devsherif', 'Xirah4Lishe8ahFae9ze')
        conn = dbConnection2.connect()
        try:
            cursor = conn.cursor()
            cursor.execute(updateStatement)
            cursor.close()
            conn.commit()
            return 'Success'
        except Exception as e:
            print("the error retrieved is:" + str(e))
            return str(e)
            if "Attempt to use a closed connection" not in str(e) and "Connection not open" not in str(
                    e) and "Communication link failure" not in str(e):
                conn.close()
            connection = dbConnection.connect()
            counter += 1
            updateCsiDB(updateStatement)

    @staticmethod
    def getCountFromCsiDB(queryString):
        dbConnection2 = DbConnection('192.168.75.1', '1433', 'CSI', 'devsherif', 'Xirah4Lishe8ahFae9ze')
        conn = dbConnection2.connect()
        try:
            cursor = conn.cursor()
            cursor.execute(queryString)
            result = cursor.fetchone()[0]
            cursor.close()
            return result
        except Exception as e:
            print("the error retrieved is:" + str(e))
            return str(e)
            if "Attempt to use a closed connection" not in str(e) and "Connection not open" not in str(
                    e) and "Communication link failure" not in str(e):
                conn.close()
            connection = dbConnection.connect()
            counter += 1
            queryDb(queryString)

    @staticmethod
    def getCountFromCsiDB(queryString):
        dbConnection2 = DbConnection('192.168.75.1', '1433', 'CSI', 'devsherif', 'Xirah4Lishe8ahFae9ze')
        conn = dbConnection2.connect()
        try:
            cursor = conn.cursor()
            cursor.execute(queryString)
            result = cursor.fetchone()[0]
            cursor.close()
            return result
        except Exception as e:
            print("the error retrieved is:" + str(e))
            return str(e)
            if "Attempt to use a closed connection" not in str(e) and "Connection not open" not in str(
                    e) and "Communication link failure" not in str(e):
                conn.close()
            connection = dbConnection.connect()
            counter += 1
            queryDb(queryString)
