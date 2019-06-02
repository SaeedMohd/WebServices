import pyodbc
import datetime
from json import dumps
from InspectionAPIs import InspectionAPIs

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
    def getFacilityEmailsFromDB(): #use this after running fillFacilityEmailsData to retrieve the data from DB
        dbConnection = DbConnection('192.168.75.1', '1433', 'CSI', 'devsherif', 'Xirah4Lishe8ahFae9ze')
        connection = dbConnection.connect()
        try:
            cursor = connection.cursor()
            cursor.execute(
                "select a.clubcode,a.facnum,b.FacName, a.emails from AAAFacilityEmails a,AAAFacilities b where a.facnum=b.FacNum and a.clubcode=RIGHT('00'+ CONVERT(VARCHAR,b.clubcode),3) and acnm = 'aaaphone' and active = 1 and a.FacNum>0 order by FacName")
            result = "Facility Name|Facility Number|Club Code|emails"
            for row in cursor.fetchall():
                result += "\n"+row[2]+"|"+str(row[1])+"|"+row[0]+"|"+row[3]
            cursor.close()
            return result
        except Exception as e:
            print("the error retrieved is:" + str(e))
            if "Attempt to use a closed connection" not in str(e) and "Connection not open" not in str(
                    e) and "Communication link failure" not in str(e):
                connection.close()


    @staticmethod
    def getFacNumAndClubs():
        dbConnection = DbConnection('192.168.75.1', '1433', 'CSI', 'devsherif', 'Xirah4Lishe8ahFae9ze')
        connection = dbConnection.connect()
        try:
            cursor = connection.cursor()
            cursor.execute("select distinct FacNum,RIGHT('00'+ CONVERT(VARCHAR,clubcode),3) AS clubcode FROM aaafacilities a where acnm = 'aaaphone' and active = 1 and FacNum>0")
            for row in cursor.fetchall():
                DbConnection.getFacilityEmailsByFacNum(row[0],row[1])
            cursor.close()
            return ''
        except Exception as e:
            print("the error retrieved is:" + str(e))
            if "Attempt to use a closed connection" not in str(e) and "Connection not open" not in str(
                    e) and "Communication link failure" not in str(e):
                connection.close()


    @staticmethod
    def getFacilityEmailsByFacNum(facnum, clubcode):
        inspectionApis = InspectionAPIs()
        result = str(inspectionApis.getFacilityData(facnum, clubcode))
        indexFrom = result.find("<tblFacilityEmail>")
        indexTo = result.rfind("</tblFacilityEmail>")
        result = result[indexFrom:indexTo + 19]
        emails = ""
        while result.find("<email>") > -1:
            indexFrom = result.find("<email>")
            indexTo = result.find("</email>")
            emails += result[indexFrom + 7:indexTo] + " - "
            indexFrom = indexTo + 8
            indexTo = result.rfind("</email>") + 8
            result = result[indexFrom:indexTo]
        DbConnection.updateCsiDB(
            "insert into AAAFacilityEmails values (" + facnum + ",'" + clubcode + "','" + emails[:-3] + "',current_timestamp)")
        return result

    # @staticmethod
    # def queryDbTypeTables(queryString):
    #     dbConnection = DbConnection('localhost', '1401', 'Inspection', 'SA', 'InspectionDoesntHaveAStrongRootPass9211@')
    #     connection = dbConnection.connect()
    #     resultDict = []
    #     result = []
    #     try:
    #         cursor = connection.cursor()
    #         resultDict.append('{\"tblPRGFacilityType\":[')
    #         cursor.execute("Select * from AAAClient.tblPRGFacilityType")
    #         columns = [column[0] for column in cursor.description]
    #         lowerColumns = []
    #         for column in columns:
    #             lowerColumns.append('"'+column.lower()+'"')
    #         for row in cursor.fetchall():
    #             resultDict.append(dict(zip(lowerColumns,row)))
    #         resultDict.append('{\"tblPRGFacilityStatusType\":[')
    #         cursor.execute("Select * from AAAClient.tblPRGFacilityStatusType")
    #         columns = [column[0] for column in cursor.description]
    #         lowerColumns = []
    #         for column in columns:
    #             lowerColumns.append('"' + column.lower() + '"')
    #         for row in cursor.fetchall():
    #             resultDict.append(dict(zip(lowerColumns, row)))
    #         cursor.close()
    #         result = dumps(resultDict, default=DbConnection.myconverter)
    #         return result
    #     except Exception as e:
    #         print("the error retrieved is:" + str(e))
    #         if "Attempt to use a closed connection" not in str(e) and "Connection not open" not in str(
    #                 e) and "Communication link failure" not in str(e):
    #             connection.close()

    @staticmethod
    def queryDbTypeTables(schemaname,clientid):
        dbConnection = DbConnection('localhost', '1401', 'Inspection', 'SA', 'InspectionDoesntHaveAStrongRootPass9211@')
        connection = dbConnection.connect()
        resultDict = []
        # result = []
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT (select * from "+schemaname+".tblPRGFacilityStatusType FOR XML PATH('tblPRGFacilityStatusType'), TYPE) AS 'ttblPRGFacilityStatusType', (select * from "+schemaname+".tblPRGVisitationTypes FOR XML PATH('tblPRGVisitationTypes'), TYPE) AS 'ttblPRGVisitationTypes', (select * from "+schemaname+".tblPRGVisitationStatus FOR XML PATH('tblPRGVisitationStatus'), TYPE) AS 'ttblPRGVisitationStatus', (select * from "+schemaname+".tblPRGVisitationReasons FOR XML PATH('tblPRGVisitationReasons'), TYPE) AS 'ttblPRGVisitationReasons', (select * from "+schemaname+".tblPRGFacilityType FOR XML PATH('tblPRGFacilityType'), TYPE) AS 'ttblPRGFacilityType', (select * from "+schemaname+".tblPRGTimezoneType FOR XML PATH('tblPRGTimezoneType'), TYPE) AS 'ttblPRGTimezoneType', (select * from "+schemaname+".tblPRGServiceAvailabilityType FOR XML PATH('tblPRGServiceAvailabilityType'), TYPE) AS 'ttblPRGServiceAvailabilityType', (select * from "+schemaname+".tblPRGTerminationCodeType FOR XML PATH('tblPRGTerminationCodeType'), TYPE) AS 'ttblPRGTerminationCodeType' ,(select userName,email,userTrackingID,isSpecialist,ReadAccess,WriteAccess from AAAMaster.tblPRGUsers where clientId="+clientid+" FOR XML PATH ('tblPRGUsers'), TYPE) AS 'ttblPRGUsers', (select specialistemail,name,clubcode,facNum,userTrackingID from "+schemaname+".tblPRGSpecialists FOR XML PATH ('tblPRGSpecialists'), TYPE) AS 'ttblPRGSpecialists',(select * from "+schemaname+".tblPRGClubs FOR XML PATH ('tblPRGClubCodes'), TYPE) AS 'ttblPRGClubCodes',(select facid,ClubCode,FACNo,BusinessName from "+schemaname+".tblPRGFacilities FOR XML PATH ('tblPRGFacilities'), TYPE) AS 'ttblPRGFacilities',(select * from "+schemaname+".tblPRGReservedFields where active = 1 FOR XML PATH ('tblPRGReservedFields'), TYPE)     AS 'ttblPRGReservedFields' FOR XML PATH(''), ROOT('root')")
            result = ""
            for row in cursor.fetchall():
                result += row[0]
            cursor.close()
            return result
        except Exception as e:
            print("the error retrieved is:" + str(e))
            if "Attempt to use a closed connection" not in str(e) and "Connection not open" not in str(
                    e) and "Communication link failure" not in str(e):
                connection.close()


    @staticmethod
    def updateDB(updateStatement):
        dbConnection = DbConnection('localhost', '1401', 'Inspection', 'SA', 'InspectionDoesntHaveAStrongRootPass9211@')
        conn = dbConnection.connect()
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
            updateDB(updateStatement)


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
    def sendPassResetMail(receipient,password):
        dbConnection2 = DbConnection('192.168.75.1', '1433', 'CSI', 'devsherif', 'Xirah4Lishe8ahFae9ze')
        conn = dbConnection2.connect()
        body = '<p>Hi,<br> It was requested to reset your password for ACE AAR Inspection App Account.<br>This is you Temp Password: <b>'+password+'</b><br><br>If you didn''t ask to reset your password, you can ignore this email.<br><br>Thanks,<br>ACE AAR Inspection Team</p>'
        conn.execute("exec dbo.sp_SMTPMail_HTML_TXT @SenderAddress = 'NoReply@PacificResearchGroup.com',@RecipientAddress = '"+receipient+"',@Subject1 = 'ACE AAR Inspection: Reset Password',@Body1 = '"+body+"'")
        conn.commit()


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

    @staticmethod
    def getCountFromDB(queryString):
        dbConnection = DbConnection('localhost', '1401', 'Inspection', 'SA', 'InspectionDoesntHaveAStrongRootPass9211@')
        conn = dbConnection.connect()
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
            # connection = dbConnection.connect()
            # counter += 1
            # queryDb(queryString)

