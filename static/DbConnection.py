import pyodbc


class DbConnection:
    connection = ''

    def __init__(self, host, dbName, username, pwd):
        self.host = host
        self.username = username
        self.pwd = pwd
        self.dbName = dbName

    def connect(self):
        self.connection = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL "
                                         "Server};Server=localhost,1401;Database=Inspection;uid=SA;pwd=InspectionDoesntHaveAStrongRootPass9211@")
        return self.connection

    def disconnect(self):
        self.connection.close()
