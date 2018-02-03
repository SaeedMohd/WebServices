from flask import Flask
from flask import request
from json import dumps
import datetime
import jsonify

from static.DbConnection import DbConnection


def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


app = Flask(__name__)

dbConnection = DbConnection('192.168.75.2', 'AARMaster', 'devsherif', 'f656dd76aed7d46914DF')
connection = dbConnection.connect()


def queryDb(queryString):
    cursor = connection.cursor()
    cursor.execute(queryString)
    resultDict = []
    columns = [column[0] for column in cursor.description]
    for row in cursor.fetchall():
        resultDict.append(dict(zip(columns, row)))
    return dumps(resultDict, default=myconverter)


@app.route('/getFacilities')
def getFacilities():
    facilityName = str(request.args.get('facilityName')).lower()
    return queryDb("select * from tblFacilities$ where active = 1 and BusinessName like '" + facilityName + "%'")


@app.route('/getFacilityHours')
def getFacilityHours():
    facilityId = str(request.args.get('facilityId'))
    return queryDb("select * from tblHours$ where facid = " + facilityId)


@app.route('/getPersonnelTypes')
def getPersonnelTeypes():
    facilityId = str(request.args.get('facilityId'))
    return queryDb(
        "select distinct(personnelTypeName), a.PersonnelTypeID  from tblPersonnelType$ a, tblPersonnel$ b where a.PersonnelTypeID = b.PersonnelTypeID and FacID = " + facilityId)


@app.route('/getPersonnelsDetails')
def getPersonnelDetails():
    facilityId = str(request.args.get('facilityId'))
    personnelTypeId = str(request.args.get('personnelTypeId'))
    return queryDb(
        "select a.FacID, a.PersonnelID,a.PersonnelTypeID,a.FirstName,a.LastName,a.SeniorityDate,a.CertificationNum,a.startDate,a.endDate,a.ContractSigner,a.PrimaryMailRecipient,a.RSP_UserName,a.RSP_Email,a.RSP_Phone,b.Addr1,b.Addr2,b.CITY, case when (b.ST is not null) then (select LongDesc from tblStateMapping where ShortDesc=b.st) else null end as State ,b.ZIP,b.ZIP4,b.Phone,b.email,b.ContractStartDate,b.ContractEndDate from tblPersonnel$ a LEFT OUTER JOIN tblPersonnelSigner$ b on a.PersonnelID=b.PersonnelID where facid = " + facilityId + " and personnelTypeId = " + personnelTypeId)


@app.route('/getScopeOfServicDetails')
def getScopeOfService():
    facilityId = str(request.args.get('facilityId'))
    return queryDb("select * from tblScopeofService$ where FACID = " + facilityId)


@app.route('/getVehicleServicesForFacility')
def getVehicleServicesForFaacility():
    facilityId = str(request.args.get('facilityId'))
    return queryDb(
        "select * from tblScopeofServiceType$ a, tblVehicleServices$ b where a.ScopeServiceID = b.ScopeServiceID and a.active = 1 and FACID = " + facilityId)


@app.route('/getPaymentMethods')
def getPaymentMethods():
    return queryDb("select * from tblPaymentMethodsType$ where active = 1")


@app.route('/getFacilityAddresses')
def getFacilityAddresses():
    facilityId = str(request.args.get('facilityId'))
    return queryDb(
        "select a.*, b.LocTypeName from tblAddress$ a, tblLocationType$ b where a.LocationTypeID = b.LocTypeID and facid = " + facilityId + " and a.active = 1 and b.active = 1")


@app.route('/getProgramTypes')
def getProgramTypes():
    return queryDb("SELECT programtypeid,programtypename from tblProgramsType$ where active=1")


@app.route('/getFacilityComplaints')
def getFacilityComplaints():
    facilityId = str(request.args.get('facilityId'))
    return queryDb(
        "select a.RecordID,a.ComplaintID,a.FirstName,a.LastName,a.ReceivedDate,c.ComplaintReasonName,(select count(1) from tblComplaintFiles$ cf where a.FACID=cf.FACID and cf.ReceivedDate>=current_timestamp-365) as NoOfComplaintsLastYear from tblComplaintFiles$ a,tblComplaintFilesReason$ b, tblComplaintFilesReasonType$ c where a.RecordID=b.ComplaintRecordID and b.ComplaintReasonID=c.ComplaintReasonID and ComplaintNotCounted=0 and FACID = " + facilityId)


@app.route('/getFacilityEmailAndPhone')
def getFacilityEmailAndPhone():
    facilityId = str(request.args.get('facilityId'))
    return queryDb(
        "select FacID,'EMAIL' as ContactType,emailTypeId as 'TYPE',case (emailTypeId) when 0 then 'Business' else 'Personal' END as 'TypeName',email as 'ContactDetail' from tblFacilityEmail$ a where FacID=" + facilityId + " union All select FacID,'PHONE',PhoneTypeID,case (PhoneTypeID) when 0 then 'Business' when 1 then 'Cell' when 2 then 'Fax' else 'Home' END ,LTRIM(str(PhoneNumber,20)) from tblPhone$ where FacID=" + facilityId)


@app.route('/getContractSignerDetails')
def getContractSignerDetails():
    personnelId = str(request.args.get('personnelId'))
    return queryDb(
        "select PersonnelID,Addr1,Addr2,CITY,ST,ZIP,ZIP4,Phone,email,ContractStartDate,ContractEndDate from tblPersonnelSigner$ where PersonnelID=" + personnelId)


@app.route('/<path:path>')
def catch_all(path):
    return '[]'


if __name__ == '__main__':
    app.run()
