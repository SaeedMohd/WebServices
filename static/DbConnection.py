import pyodbc


class DbConnection:
    connection = ''

    def __init__(self, host, port, dbName, username, pwd):
        self.host = host
        self.port = port
        self.username = username
        self.pwd = pwd
        self.dbName = dbName

    def connect(self):
        self.connection = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL "
                                         "Server};Server="+self.host+","+self.port+";Database="+self.dbName+";uid="+self.username+";pwd="+self.pwd)
        return self.connection

    def disconnect(self):
        self.connection.close()
