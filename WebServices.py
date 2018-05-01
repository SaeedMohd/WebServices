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

counter = 0


def getRequestParam(req, param):
    return req.args.get(param)


def queryDb(queryString):
    global connection
    global counter
    if counter > 2:
        counter = 0
        return "[]"
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
        return dumps(resultDict, default=myconverter)
    except Exception as e:
        print("the error retrieved is:" + str(e))
        if "Attempt to use a closed connection" not in str(e) and "Connection not open" not in str(
                e) and "Communication link failure" not in str(e):
            connection.close()
        connection = dbConnection.connect()
        counter += 1
        queryDb(queryString)


@app.route('/getFacilities')
def getFacilities():
    facilityName = str(request.args.get('facilityName')).lower()
    return queryDb("select * from tblFacilities$ where active = 1 and BusinessName like '" + facilityName + "%'")


@app.route('/getFacilityWithId')
def getFacilityWithId():
    facilityId = request.args.get('facilityId')
    return queryDb("select * from tblFacilities$ where active = 1 and facId = " + facilityId)


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


@app.route('/getAllPersonnelsDetails')
def getAllPersonnelDetails():
    return queryDb(
        "select a.FacID, a.PersonnelID,a.PersonnelTypeID,a.FirstName,a.LastName,a.SeniorityDate,a.CertificationNum,a.startDate,a.endDate,a.ContractSigner,a.PrimaryMailRecipient,a.RSP_UserName,a.RSP_Email,a.RSP_Phone,b.Addr1,b.Addr2,b.CITY, case when (b.ST is not null) then (select LongDesc from tblStateMapping where ShortDesc=b.st) else null end as State ,b.ZIP,b.ZIP4,b.Phone,b.email,b.ContractStartDate,b.ContractEndDate from tblPersonnel$ a LEFT OUTER JOIN tblPersonnelSigner$ b on a.PersonnelID=b.PersonnelID")


@app.route('/getPersonnelDetailsWithId')
def getPersonnelDetailsWithId():
    personneId = str(request.args.get('personnelId'))
    return queryDb(
        "select a.FacID, a.PersonnelID,a.PersonnelTypeID,a.FirstName,a.LastName,a.SeniorityDate,a.CertificationNum,a.startDate,a.endDate,a.ContractSigner,a.PrimaryMailRecipient,a.RSP_UserName,a.RSP_Email,a.RSP_Phone,b.Addr1,b.Addr2,b.CITY, case when (b.ST is not null) then (select LongDesc from tblStateMapping where ShortDesc=b.st) else null end as State ,b.ZIP,b.ZIP4,b.Phone,b.email,b.ContractStartDate,b.ContractEndDate from tblPersonnel$ a LEFT OUTER JOIN tblPersonnelSigner$ b on a.PersonnelID=b.PersonnelID where a.personnelId = " + personneId)


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


# @app.route('/getFacilityComplaints')
# def getFacilityComplaints():
#     facilityId = str(request.args.get('facilityId'))
#     return queryDb(
#         "select a.RecordID,a.ComplaintID,a.FirstName,a.LastName,a.ReceivedDate,c.ComplaintReasonName,(select count(1) from tblComplaintFiles$ cf where a.FACID=cf.FACID and cf.ReceivedDate>=current_timestamp-365) as NoOfComplaintsLastYear from tblComplaintFiles$ a,tblComplaintFilesReason$ b, tblComplaintFilesReasonType$ c where a.RecordID=b.ComplaintRecordID and b.ComplaintReasonID=c.ComplaintReasonID and ComplaintNotCounted=0 and FACID = " + facilityId)


@app.route('/getFacilityEmailAndPhone')
def getFacilityEmailaAndPhone():
    facilityId = str(request.args.get('facilityId'))
    return queryDb(
        "select FacID,'EMAIL' as ContactType,emailTypeId as 'TYPE',case (emailTypeId) when 0 then 'Business' else 'Personal' END as 'TypeName',email as 'ContactDetail' from tblFacilityEmail$ a where FacID=" + facilityId + " union All select FacID,'PHONE',PhoneTypeID,case (PhoneTypeID) when 0 then 'Business' when 1 then 'Cell' when 2 then 'Fax' else 'Home' END ,LTRIM(str(PhoneNumber,20)) from tblPhone$ where FacID=" + facilityId)


@app.route('/getVisitationRecords')
def getVisitationRecords():
    facilityName = str(request.args.get('facilityName'))
    inspectionType = str(request.args.get('inspectionType'))
    if inspectionType == '0':
        return queryDb(
            "select a.facID, a.visitationID, a.performedBy, a.DatePerformed, a.DatePlanned, c.businessName as name, case when(DatePlanned is not null) then 'Planned Visitation' else 'New Visitation' end as InspectionStatus from tblVisitationRecords a, tblInspectiontypes b, tblFacilities$ c where a.facID = c.FacID and  a.InspectionType = b.id and (BusinessName like '%" + facilityName + "%' or EntityName like '%" + facilityName + "%')")
    else:
        return queryDb(
            "select a.facID, a.visitationID, a.performedBy, a.DatePerformed, a.DatePlanned, c.businessName as name, case when(DatePlanned is not null) then 'Planned Visitation' else 'New Visitation' end as InspectionStatus from tblVisitationRecords a, tblInspectiontypes b, tblFacilities$ c where a.facID = c.FacID and  a.InspectionType = b.id and (BusinessName like '%" + facilityName + "%' or EntityName like '%" + facilityName + "%') and a.InspectionType = " + inspectionType)


@app.route('/getContractSignerDetails')
def getContractSignerDetails():
    personnelId = str(request.args.get('personnelId'))
    return queryDb(
        "select PersonnelID,Addr1,Addr2,CITY,ST,ZIP,ZIP4,Phone,email,ContractStartDate,ContractEndDate from tblPersonnelSigner$ where PersonnelID=" + personnelId)


@app.route('/getAnnualVisitations')
def getAnnualVisitations():
    clubCode = getRequestParam(request, 'clubCode')
    facilityNumber = getRequestParam(request, 'facilityNumber')
    facilityName = getRequestParam(request, 'facilityName')
    year = getRequestParam(request, 'year')
    month = getRequestParam(request, 'month')
    specialistName = getRequestParam(request, 'specialistName')
    isAnnualVisitation = getRequestParam(request, 'isAnnualVisitation')
    isOtherVisitation = getRequestParam(request, 'isOtherVisitation')
    isAdHocVisitation = getRequestParam(request, 'isAdHocVisitation')
    isDeficiency = getRequestParam(request, 'isDeficiency')
    isPending = getRequestParam(request, 'isPending')
    isCompleted = getRequestParam(request, 'isCompleted')

    queryString = 'select * from tblAnnualVisitationInspectionFormData a , tblFacilities$ b where a.facilityId = b.FacID'

    if clubCode is not None:
        queryString += " and clubCode = " + clubCode

    if facilityName is not None:
        queryString += " and (b.EntityName like '%" + facilityName + "%' or b.BusinessName like '%" + facilityName + "%')"

    if facilityNumber is not None:
        queryString += " and facno = " + facilityNumber

    if year is not None:
        queryString += " and year(dateOfInspection) = " + year

    if month is not None:
        queryString += " and month(dateOfInspection) = " + month

    if specialistName is not None:
        queryString += " and automotivespecialistname = '" + specialistName+"'"

    if isAnnualVisitation is not None:
        if isAnnualVisitation:
            queryString += " and inspectionType = 3"
        else:
            queryString += " and inspectionType != 3"

    if isOtherVisitation is not None:
        queryString += " and inspectionType != 3"

    # if isAdHocVisitation:
    #     queryString += " and inspectionType in (1, 4, 5)"

    if isDeficiency is not None:
        queryString += " and inspectionType in (1, 4, 5)"

    if isPending is not None:
        queryString += " and dateOfInspection > getdate()"

    # if isCompleted:
    #     quereyString += " "

    print(queryString)

    return queryDb(queryString)


@app.route('/getLastAnnualVisitationInspectionForFacility')
def getLastAnnualVisitationInspectionForFacility():
    facilityId = str(request.args.get('facilityId'))
    return queryDb(
        "select * from tblAnnualVisitationInspectionFormData where facilityId=" + facilityId)


@app.route('/getPhoneNumberWithFacilityAndId')
def getPhoneNumberWithFacilityAndId():
    facilityId = str(request.args.get('facilityId'))
    phoneId = str(request.args.get('phoneId'))
    return queryDb(
        "select * from tblPhone$ a where FacID = " + facilityId + " and phoneId = " + phoneId + " and active = 1")


@app.route('/getEmailFromFacilityAndId')
def getEmailFromFacilityAndId():
    facilityId = str(request.args.get('facilityId'))
    emailId = str(request.args.get('emailId'))
    return queryDb(
        "select * from tblFacilityEmail$ where facId = " + facilityId + " and emailId = " + emailId + "")


@app.route('/getVehicleServices')
def getVehicleServices():
    return queryDb(
        "select * from tblScopeofServiceType$ where active = 1 order by scopeservicename")


@app.route('/getFacilityPrograms')
def getFacilityPrograms():
    facilityId = str(request.args.get('facilityId'))
    return queryDb(
        "select ProgramID,ProgramTypeName,effDate,expDate,Comments from tblPrograms$ a, tblProgramsType$ b where a.ProgramTypeID=b.ProgramTypeID and a.active=1 and FACID=" + facilityId)


@app.route('/getVehicles')
def getVehicles():
    return queryDb(
        "select * from tblVehicleMakesType$ where active = 1 order by 2")


@app.route('/getAffiliationTypes')
def getAffiliationTypes():
    return queryDb(
        "select a.typeID,typeName,typeDetailID,typeDetailName from tblAffiliationType a left OUTER JOIN tblAffiliationTypeDetail b on a.typeID=b.typeID")


@app.route('/getFacilityAffiliations')
def getFacilityAffiliations():
    facilityId = str(request.args.get('facilityId'))
    return queryDb(
        "select a.AffiliationID,b.typeName,(select typeDetailName from tblAffiliationTypeDetail where typeDetailID=AffiliationTypeDetailID) as typeDetailName ,effDate,expDate,comment from tblAffiliations$ a, tblAffiliationType b where a.AffiliationTypeID=b.typeID and a.active=1 and FACID=" + facilityId)


@app.route('/getFacilityComplaints')
def getFacilityComplaints():
    facilityId = str(request.args.get('facilityId'))
    all = str(request.args.get('all'))
    if all == 'true':
        return queryDb(
            "select a.RecordID,a.ComplaintID,a.FirstName,a.LastName,a.ReceivedDate,c.ComplaintReasonName,f.ComplaintResolutionName,(select count(1) from tblComplaintFiles$ cf where a.FACID=cf.FACID and cf.ReceivedDate<=current_timestamp) as NoOfComplaintsLastYear, (select count(1) from tblComplaintFiles$ cf,tblComplaintFilesResolution$ cfr, tblComplaintFilesResolutionType$ cfrt where a.FACID=cf.FACID and cfr.ComplaintRecordID=cf.RecordID and cfr.ComplaintResolutionID=cfrt.ComplaintResolutionID and cf.ReceivedDate<=current_timestamp and lower(ComplaintResolutionName) ='justified') as NoOfJustifiedLastYear, (FacilityRepairOrderCount*12) as TotalOrders, '' as comments from tblComplaintFiles$ a,tblComplaintFilesReason$ b, tblComplaintFilesReasonType$ c,tblFacilities$ d, tblComplaintFilesResolution$ e, tblComplaintFilesResolutionType$ f where a.RecordID=b.ComplaintRecordID and b.ComplaintReasonID=c.ComplaintReasonID and a.RecordID=e.ComplaintRecordID and e.ComplaintResolutionID=f.ComplaintResolutionID and ComplaintNotCounted=0 and a.FACID=d.FacID and ReceivedDate<=current_timestamp and a.FACID=" + facilityId)
    else:
        return queryDb(
            "select a.RecordID,a.ComplaintID,a.FirstName,a.LastName,a.ReceivedDate,c.ComplaintReasonName,f.ComplaintResolutionName,(select count(1) from tblComplaintFiles$ cf where a.FACID=cf.FACID and cf.ReceivedDate>=current_timestamp-365) as NoOfComplaintsLastYear, (select count(1) from tblComplaintFiles$ cf,tblComplaintFilesResolution$ cfr, tblComplaintFilesResolutionType$ cfrt where a.FACID=cf.FACID and cfr.ComplaintRecordID=cf.RecordID and cfr.ComplaintResolutionID=cfrt.ComplaintResolutionID and cf.ReceivedDate>=current_timestamp-365 and lower(ComplaintResolutionName) ='justified') as NoOfJustifiedLastYear, (FacilityRepairOrderCount*12) as TotalOrders, '' as comments from tblComplaintFiles$ a,tblComplaintFilesReason$ b, tblComplaintFilesReasonType$ c,tblFacilities$ d, tblComplaintFilesResolution$ e, tblComplaintFilesResolutionType$ f where a.RecordID=b.ComplaintRecordID and b.ComplaintReasonID=c.ComplaintReasonID and a.RecordID=e.ComplaintRecordID and e.ComplaintResolutionID=f.ComplaintResolutionID and ComplaintNotCounted=0 and a.FACID=d.FacID and ReceivedDate>=current_timestamp-365 and a.FACID=" + facilityId)


@app.route('/<path:path>')
def catch_all(path):
    return '[]'


if __name__ == '__main__':
    app.run()
