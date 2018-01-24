import pypyodbc


class DbConnection:
    connection = ''

    def __init__(self, host, dbName, username, pwd):
        self.host = host
        self.username = username
        self.pwd = pwd
        self.dbName = dbName

    def connect(self):
        self.connection = pypyodbc.connect(
            'Driver={SQL Server};Server=' + self.host + ';Database=' + self.dbName + ';uid=' + self.username + ';pwd=' + self.pwd)
        return self.connection

    def disconnect(self):
        self.connection.close()

