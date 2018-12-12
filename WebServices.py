from flask import Flask
from flask import request
from json import dumps
from InspectionAPIs import InspectionAPIs
import datetime

from static.DbConnection import DbConnection


def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


app = Flask(__name__)

dbConnection = DbConnection('localhost', '1401', 'Inspection', 'SA', 'InspectionDoesntHaveAStrongRootPass9211@')
connection = dbConnection.connect()

counter = 0

inspectionApis = InspectionAPIs()


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
        return dumps(resultDict, default=myconverter)
    except Exception as e:
        print("the error retrieved is:" + str(e))
        return str(e)
        if "Attempt to use a closed connection" not in str(e) and "Connection not open" not in str(
                e) and "Communication link failure" not in str(e):
            conn.close()
        connection = dbConnection.connect()
        counter += 1
        queryDb(queryString)


@app.route('/getAllFacilities')
def getAllFacilities():
    return queryCsiDB(
        "select clubcode, facnum, facname from csi.dbo.AAAFacilities where acnm = 'aaaphone' and active = 1")


@app.route('/getAllSpecialists')
def getAllSpecialists():
    # return queryCsiDB("select id, AccSpecID, specialistName from csi.dbo.aaaspecialist where acnm = 'aaaphone'")
    return queryCsiDB("exec csi.dbo.ACE_Specialists")


@app.route('/getClubCodes')
def getClubCodes():
    clubCodeQuery = str(request.args.get('clubCode'))
    queryString = "SELECT distinct(RIGHT('00'+ CONVERT(VARCHAR,clubcode),3)) AS clubcode FROM aaafacilities a where acnm = 'aaaphone' and active = 1"
    if clubCodeQuery is not None:
        queryString += " and RIGHT('00'+ CONVERT(VARCHAR,clubcode),3) like '" + clubCodeQuery + "%'"
    queryString += " order by 1"
    return queryCsiDB(queryString)


@app.route('/getSpecialistNameFromEmail')
def getSpecialistNameFromEmail():
    specialistEmail = request.args.get('specialistEmail')
    return queryCsiDB(
        "select clubcode, specialistName from csi.dbo.aaaspecialist where acnm = 'aaaphone' and lower(specialistemail) = lower('" + specialistEmail + "')")


@app.route('/getVisitationPlanningList')
def getVisitationPlanningList():
    facilityName = request.args.get('facilityName')
    month = request.args.get('month')
    year = request.args.get('year')
    if facilityName is not None and len(facilityName) > 0:
        return queryCsiDB(
            "select FacNum, facname, joindate from csi.dbo.aaafacilities where facname = '" + facilityName + "' and month(JoinDate) = " + month + " and year(JoinDate) < " + year)
    else:
        return queryCsiDB(
            "select FacNum, facname, joindate from csi.dbo.aaafacilities where month(JoinDate) = " + month + " and year(JoinDate) < " + year)


@app.route('/getFacilities')
def getFacilities():
    facilityName = str(request.args.get('facilityName')).lower()
    return queryDb("select * from tblFacilities$ where active = 1 and BusinessName like '" + facilityName + "%'")


@app.route('/getFacilityWithId')
def getFacilityWithId():
    facilityId = request.args.get('facilityId')
    return queryDb("select * from tblFacilities$ where active = 1 and facId = " + facilityId)


@app.route('/getFacilitiesWithFilters')
def getFacilitiesWithFilters():
    facilityNumber = request.args.get('facilityNumber')
    clubCode = request.args.get('clubCode')
    dba = request.args.get('dba')
    assignedSpecialist = request.args.get('assignedSpecialist')
    contractStatus = request.args.get('contractStatus')
    queryString = "select RIGHT('00'+ CONVERT(VARCHAR,clubcode),3) as clubcode, facName, facNum from csi.dbo.aaafacilities where acnm = 'aaaphone' and RIGHT('00'+ CONVERT(VARCHAR,clubcode),3) like '%" + clubCode + "%' and facName like '%" + dba + "%'"

    if len(contractStatus) > 0:
        queryString += str(" and active = " + contractStatus)
    if len(facilityNumber) > 0:
        queryString += str(" and facNum like '%" + facilityNumber + "%'")
    if len(assignedSpecialist) > 0:
        queryString += str(
            " and specialistid = (select id from csi.dbo.aaaspecialist where accspecid = '" + assignedSpecialist + "')")
    return queryCsiDB(queryString)


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
        queryString += " and automotivespecialistname = '" + specialistName + "'"

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


@app.route('/updatePaymentMethodsData')
def updatePaymentMethodsData():
    facNum = str(request.args.get('facNum'))
    clubCode = str(request.args.get('clubCode'))
    paymentMethodID = str(request.args.get('paymentMethodID'))
    insertBy = str(request.args.get('insertBy'))
    insertDate = str(request.args.get('insertDate'))
    return str(inspectionApis.updatePaymentMethodsData(facNum, clubCode, paymentMethodID, insertBy, insertDate))


@app.route('/getTableTypes')
def getTableTypes():
    return str(inspectionApis.getTableTypes())


@app.route('/getVisitations')
def getVisitations():
    facNum = str(request.args.get('facNum'))
    clubCode = str(request.args.get('clubCode'))
    specialist = str(request.args.get('specialist'))
    dba = str(request.args.get('dba'))
    inspectionMonth = str(request.args.get('inspectionMonth'))
    inspectionYear = str(request.args.get('inspectionYear'))
    annualVisitations = str(request.args.get('annualVisitations'))
    quarterlyVisitations = str(request.args.get('quarterlyVisitations'))
    pendingVisitations = str(request.args.get('pendingVisitations'))
    completedVisitations = str(request.args.get('completedVisitations'))
    deficiencies = str(request.args.get('deficiencies'))
    return str(inspectionApis.getVisitations(clubCode, facNum, specialist, dba, inspectionMonth, inspectionYear,
                                             annualVisitations, quarterlyVisitations, pendingVisitations,
                                             completedVisitations, deficiencies))


@app.route('/updateFacilityData')
def updateFacilityData():
    facNum = str(request.args.get('facNum'))
    clubCode = str(request.args.get('clubCode'))
    businessName = str(request.args.get('businessName'))
    busTypeId = str(request.args.get('busTypeId'))
    entityName = str(request.args.get('entityName'))
    assignToId = str(request.args.get('assignToId'))
    officeId = str(request.args.get('officeId'))
    taxIdNumber = str(request.args.get('taxIdNumber'))
    facilityRepairOrderCount = str(request.args.get('facilityRepairOrderCount'))
    facilityAnnualInspectionMonth = str(request.args.get('facilityAnnualInspectionMonth'))
    inspectionCycle = str(request.args.get('inspectionCycle'))
    timeZoneId = str(request.args.get('timeZoneId'))
    svcAvailability = str(request.args.get('svcAvailability'))
    facilityTypeId = str(request.args.get('facilityTypeId'))
    automotiveRepairNumber = str(request.args.get('automotiveRepairNumber'))
    automotiveRepairExpDate = str(request.args.get('automotiveRepairExpDate'))
    contractCurrentDate = str(request.args.get('contractCurrentDate'))
    contractInitialDate = str(request.args.get('contractInitialDate'))
    billingMonth = str(request.args.get('billingMonth'))
    billingAmount = str(request.args.get('billingAmount'))
    internetAccess = str(request.args.get('internetAccess'))
    webSite = str(request.args.get('webSite'))
    terminationDate = str(request.args.get('terminationDate'))
    terminationId = str(request.args.get('terminationId'))
    terminationComments = str(request.args.get('terminationComments'))
    insertBy = str(request.args.get('insertBy'))
    insertDate = str(request.args.get('insertDate'))
    updateBy = str(request.args.get('updateBy'))
    updateDate = str(request.args.get('updateDate'))
    active = str(request.args.get('active'))
    achParticipant = str(request.args.get('achParticipant'))
    insuranceExpDate = str(request.args.get('insuranceExpDate'))
    contractTypeId = str(request.args.get('contractTypeId'))
    return str(
        inspectionApis.updateFacilityData(facNum, clubCode, businessName, busTypeId, entityName, assignToId, officeId
                                          , taxIdNumber, facilityRepairOrderCount, facilityAnnualInspectionMonth,
                                          inspectionCycle,
                                          timeZoneId, svcAvailability
                                          , facilityTypeId, automotiveRepairNumber, automotiveRepairExpDate,
                                          contractCurrentDate,
                                          contractInitialDate, billingMonth, billingAmount
                                          , internetAccess, webSite, terminationDate, terminationId,
                                          terminationComments, insertBy,
                                          insertDate, updateBy, updateDate
                                          , active, achParticipant, insuranceExpDate, contractTypeId))


@app.route('/updateFacilityAddressData')
def updateFacilityAddressData():
    facnum = str(request.args.get('facnum'))
    clubcode = str(request.args.get('clubcode'))
    locationTypeID = str(request.args.get('locationTypeID'))
    FAC_Addr1 = str(request.args.get('FAC_Addr1'))
    FAC_Addr2 = str(request.args.get('FAC_Addr2'))
    CITY = str(request.args.get('CITY'))
    ST = str(request.args.get('ST'))
    ZIP = str(request.args.get('ZIP'))
    Country = str(request.args.get('Country'))
    BranchName = str(request.args.get('BranchName'))
    BranchNumber = str(request.args.get('BranchNumber'))
    LATITUDE = str(request.args.get('LATITUDE'))
    LONGITUDE = str(request.args.get('LONGITUDE'))
    insertBy = str(request.args.get('insertBy'))
    insertDate = str(request.args.get('insertDate'))
    updateBy = str(request.args.get('updateBy'))
    updateDate = str(request.args.get('updateDate'))
    active = str(request.args.get('active'))

    return str(
        inspectionApis.updateFacilityAddressData(facnum, clubcode, locationTypeID, FAC_Addr1, FAC_Addr2, CITY, ST, ZIP,
                                                 Country, BranchName, BranchNumber, LATITUDE, LONGITUDE, insertBy,
                                                 insertDate, updateBy, updateDate, active))


@app.route('/updateFacilityEmailData')
def updateFacilityEmailData():
    facNum = str(request.args.get('facNum'))
    clubCode = str(request.args.get('clubCode'))
    emailId = str(request.args.get('emailId'))
    emailTypeId = str(request.args.get('emailTypeId'))
    email = str(request.args.get('email'))
    insertBy = str(request.args.get('insertBy'))
    insertDate = str(request.args.get('insertDate'))
    updateBy = str(request.args.get('updateBy'))
    updateDate = str(request.args.get('updateDate'))
    active = str(request.args.get('active'))
    return str(
        inspectionApis.updateFacilityEmailData(facNum, clubCode, emailId, emailTypeId, email, insertBy, insertDate,
                                               updateBy, updateDate, active))


@app.route('/updateFacilityPhoneData')
def updateFacilityPhoneData():
    facNum = str(request.args.get('facNum'))
    clubCode = str(request.args.get('clubCode'))
    phoneId = str(request.args.get('phoneId'))
    phoneTypeId = str(request.args.get('phoneTypeId'))
    phoneNumber = str(request.args.get('phoneNumber'))
    extension = str(request.args.get('extension'))
    description = str(request.args.get('description'))
    insertBy = str(request.args.get('insertBy'))
    insertDate = str(request.args.get('insertDate'))
    updateBy = str(request.args.get('updateBy'))
    updateDate = str(request.args.get('updateDate'))
    active = str(request.args.get('active'))
    return str(inspectionApis.updateFacilityPhoneData(facNum, clubCode, phoneId, phoneTypeId, phoneNumber, extension,
                                                      description, insertBy, insertDate, updateBy, updateDate, active))


@app.route('/updateFacilityPersonnelData')
def updateFacilityPersonnelData(facNum, clubCode, personnelId, personnelTypeId, firstName, lastName,
                                seniorityDate, certificationNum, startDate, contractSigner
                                , insertBy, insertDate, updateBy, updateDate, active, primaryMailRecipient,
                                rsp_userName, rsp_email, rsp_phone):
    facNum = str(request.args.get('facNum'))
    clubCode = str(request.args.get('clubCode'))
    personnelId = str(request.args.get('personnelId'))
    personnelTypeId = str(request.args.get('personnelTypeId'))
    firstName = str(request.args.get('firstName'))
    lastName = str(request.args.get('lastName'))
    seniorityDate = str(request.args.get('seniorityDate'))
    certificationNum = str(request.args.get('certificationNum'))
    startDate = str(request.args.get('startDate'))
    contractSigner = str(request.args.get('contractSigner'))
    insertBy = str(request.args.get('insertBy'))
    insertDate = str(request.args.get('insertDate'))
    updateBy = str(request.args.get('updateBy'))
    updateDate = str(request.args.get('updateDate'))
    active = str(request.args.get('active'))
    primaryMailRecipient = str(request.args.get('primaryMailRecipient'))
    rsp_userName = str(request.args.get('rsp_userName'))
    rsp_email = str(request.args.get('rsp_email'))
    rsp_phone = str(request.args.get('rsp_phone'))
    return str(
        inspectionApis.updateFacilityPersonnelData(facNum, clubCode, personnelId, personnelTypeId, firstName, lastName,
                                                   seniorityDate, certificationNum, startDate, contractSigner, insertBy,
                                                   insertDate, updateBy, updateDate, active, primaryMailRecipient,
                                                   rsp_userName, rsp_email, rsp_phone))


@app.route('/updateScopeOfServiceData')
def updateScopeOfServiceData():
    facNum = str(request.args.get('facNum'))
    clubCode = str(request.args.get('clubCode'))
    laborRateId = str(request.args.get('laborRateId'))
    fixedLaborRate = str(request.args.get('fixedLaborRate'))
    laborMin = str(request.args.get('laborMin'))
    laborMax = str(request.args.get('laborMax'))
    diagnosticRate = str(request.args.get('diagnosticRate'))
    numOfBays = str(request.args.get('numOfBays'))
    numOfLifts = str(request.args.get('numOfLifts'))
    warrantyTypeId = str(request.args.get('warrantyTypeId'))
    active = str(request.args.get('active'))
    insertBy = str(request.args.get('insertBy'))
    insertDate = str(request.args.get('insertDate'))
    updateBy = str(request.args.get('updateBy'))
    updateDate = str(request.args.get('updateDate'))
    return str(
        inspectionApis.updateScopeOfServiceData(facNum, clubCode, laborRateId, fixedLaborRate, laborMin, laborMax,
                                                diagnosticRate, numOfBays, numOfLifts, warrantyTypeId, active,
                                                insertBy, insertDate, updateBy, updateDate))


@app.route('/updatevisitationTrackingData')
def updateVisitationTrackingData():
    facNum = str(request.args.get('facNum'))
    clubCode = str(request.args.get('clubCode'))
    visitationId = str(request.args.get('visitationId'))
    performedBy = str(request.args.get('performedBy'))
    datePerformed = str(request.args.get('datePerformed'))
    dateReceived = str(request.args.get('dateReceived'))
    insertBy = str(request.args.get('insertBy'))
    insertDate = str(request.args.get('insertDate'))
    updateBy = str(request.args.get('updateBy'))
    updateDate = str(request.args.get('updateDate'))
    return str(inspectionApis.updateVisitationTrackingData(facNum, clubCode, visitationId, performedBy, datePerformed,
                                                           dateReceived, insertBy, insertDate, updateBy, updateDate))


@app.route('/updateAARPortalAdminDate')
def updateAARPortalAdminData():
    facNum = str(request.args.get('facNum'))
    clubCode = str(request.args.get('clubCode'))
    startDate = str(request.args.get('startDate'))
    endDate = str(request.args.get('endDate'))
    addendumSigned = str(request.args.get('addendumSigned'))
    cardReaders = str(request.args.get('cardReaders'))
    insertBy = str(request.args.get('insertBy'))
    insertDate = str(request.args.get('insertDate'))
    updateBy = str(request.args.get('updateBy'))
    updateDate = str(request.args.get('updateDate'))
    active = str(request.args.get('active'))
    return str(
        inspectionApis.updateAARPortalAdminData(facNum, clubCode, startDate, endDate, addendumSigned, cardReaders,
                                                insertBy, insertDate, updateBy, updateDate, active))


@app.route('/updateAffiliationsData')
def updateAffiliationsData():
    facNum = str(request.args.get('facNum'))
    clubCode = str(request.args.get('clubCode'))
    affiliationId = str(request.args.get('affiliationId'))
    affiliationTypeId = str(request.args.get('affiliationTypeId'))
    affiliationTypeDetailsId = str(request.args.get('affiliationTypeDetailsId'))
    effDate = str(request.args.get('effDate'))
    expDate = str(request.args.get('expDate'))
    comment = str(request.args.get('comment'))
    active = str(request.args.get('active'))
    insertBy = str(request.args.get('insertBy'))
    insertDate = str(request.args.get('insertDate'))
    updateBy = str(request.args.get('updateBy'))
    updateDate = str(request.args.get('updateDate'))
    return str(inspectionApis.updateAffiliationsData(facNum, clubCode, affiliationId, affiliationTypeId,
                                                     affiliationTypeDetailsId, effDate, expDate, comment, active,
                                                     insertBy, insertDate, updateBy, updateDate))


@app.route('/updateAmendmentOrderTrackingData')
def updateAmendmentOrderTrackingData():
    facNum = str(request.args.get('facNum'))
    clubCode = str(request.args.get('clubCode'))
    facId = str(request.args.get('facId'))
    aoId = str(request.args.get('aoId'))
    employeeId = str(request.args.get('employeeId'))
    reasonId = str(request.args.get('reasonId'))
    insertBy = str(request.args.get('insertBy'))
    insertDate = str(request.args.get('insertDate'))
    updateBy = str(request.args.get('updateBy'))
    updateDate = str(request.args.get('updateDate'))
    active = str(request.args.get('active'))
    return str(
        inspectionApis.updateAmendmentOrderTrackingData(facNum, clubCode, facId, aoId, employeeId, reasonId, insertBy,
                                                        insertDate, updateBy, updateDate, active))


@app.route('/updateDeficiencyData')
def updateDeficiencyData():
    facNum = str(request.args.get('facNum'))
    clubCode = str(request.args.get('clubCode'))
    defId = str(request.args.get('defId'))
    defTypeId = str(request.args.get('defTypeId'))
    visitationDate = str(request.args.get('visitationDate'))
    enteredDate = str(request.args.get('enteredDate'))
    clearedDate = str(request.args.get('clearedDate'))
    comments = str(request.args.get('comments'))
    insertBy = str(request.args.get('insertBy'))
    insertDate = str(request.args.get('insertDate'))
    updateBy = str(request.args.get('updateBy'))
    updateDate = str(request.args.get('updateDate'))
    return str(inspectionApis.updateDeficiencyData(facNum, clubCode, defId, defTypeId, visitationDate, enteredDate,
                                                   clearedDate, comments, insertBy, insertDate, updateBy, updateDate))


@app.route('/updateComplaintFilesData')
def updateComplaintFilesData():
    facnum = str(request.args.get('facnum'))
    clubcode = str(request.args.get('clubcode'))
    RecordID = str(request.args.get('RecordID'))
    ComplaintID = str(request.args.get('ComplaintID'))
    FACID = str(request.args.get('FACID'))
    initiatedBy = str(request.args.get('initiatedBy'))
    IsTowIn, = str(request.args.get('IsTowIn,'))
    IsOutofState = str(request.args.get('IsOutofState'))
    SOSSID = str(request.args.get('SOSSID'))
    FirstName = str(request.args.get('FirstName'))
    LastName = str(request.args.get('LastName'))
    ComplaintNotCounted = str(request.args.get('ComplaintNotCounted'))
    IsERSComplaint, = str(request.args.get('IsERSComplaint,'))
    AssignedTo = str(request.args.get('AssignedTo'))
    ComplaintReasonID = str(request.args.get('ComplaintReasonID'))
    ComplaintResolutionID = str(request.args.get('ComplaintResolutionID'))
    ReceivedDate = str(request.args.get('ReceivedDate'))
    OpenedDate, = str(request.args.get('OpenedDate,'))
    ClosedDate = str(request.args.get('ClosedDate'))
    SecondOpenedDate = str(request.args.get('SecondOpenedDate'))
    SecondClosedDate = str(request.args.get('SecondClosedDate'))
    WorkDaysNotCounted = str(request.args.get('WorkDaysNotCounted'))
    insertBy, = str(request.args.get('insertBy,'))
    insertDate = str(request.args.get('insertDate'))
    updateBy = str(request.args.get('updateBy'))
    updateDate = str(request.args.get('updateDate'))
    return str(
        inspectionApis.updateComplaintFilesData(facnum, clubcode, RecordID, ComplaintID, FACID, initiatedBy, IsTowIn,
                                                IsOutofState, SOSSID, FirstName, LastName, ComplaintNotCounted,
                                                IsERSComplaint, AssignedTo, ComplaintReasonID, ComplaintResolutionID,
                                                ReceivedDate, OpenedDate, ClosedDate, SecondOpenedDate,
                                                SecondClosedDate, WorkDaysNotCounted, insertBy, insertDate, updateBy,
                                                updateDate))


@app.route('/updateFacilityClosureData')
def updateFacilityClosureData():
    facNum = str(request.args.get('facNum'))
    clubCode = str(request.args.get('clubCode'))
    facilityClosureId = str(request.args.get('facilityClosureId'))
    closureId = str(request.args.get('closureId'))
    effDate = str(request.args.get('effDate'))
    expDate, = str(request.args.get('expDate,'))
    comments = str(request.args.get('comments'))
    active = str(request.args.get('active'))
    insertBy = str(request.args.get('insertBy'))
    insertDate = str(request.args.get('insertDate'))
    updateBy = str(request.args.get('updateBy'))
    updateDate, = str(request.args.get('updateDate,'))
    prgFacilityClosureId = str(request.args.get('prgFacilityClosureId'))
    return str(
        inspectionApis.updateFacilityClosureData(facNum, clubCode, facilityClosureId, closureId, effDate, expDate,
                                                 comments, active, insertBy, insertDate, updateBy, updateDate,
                                                 prgFacilityClosureId))


@app.route('/updateFacilityHoursData')
def updateFacilityHoursData():
    facNum = str(request.args.get('facNum'))
    clubCode = str(request.args.get('clubCode'))
    monOpen = str(request.args.get('monOpen'))
    monClose = str(request.args.get('monClose'))
    tueOpen = str(request.args.get('tueOpen'))
    tueClose = str(request.args.get('tueClose'))
    wedOpen = str(request.args.get('wedOpen'))
    wedClose, = str(request.args.get('wedClose,'))
    thuOpen = str(request.args.get('thuOpen'))
    thuClose = str(request.args.get('thuClose'))
    friOpen = str(request.args.get('friOpen'))
    friClose = str(request.args.get('friClose'))
    satOpen = str(request.args.get('satOpen'))
    satClose = str(request.args.get('satClose'))
    sunOpen = str(request.args.get('sunOpen'))
    sunClose, = str(request.args.get('sunClose,'))
    nightDrop = str(request.args.get('nightDrop'))
    nightDropInstr = str(request.args.get('nightDropInstr'))
    insertBy = str(request.args.get('insertBy'))
    insertDate = str(request.args.get('insertDate'))
    updateBy = str(request.args.get('updateBy'))
    updateDate, = str(request.args.get('updateDate,'))
    facAvailability = str(request.args.get('facAvailability'))
    availEffDate = str(request.args.get('availEffDate'))
    availExpDate = str(request.args.get('availExpDate'))
    return str(inspectionApis.updateFacilityHoursData(facNum, clubCode, monOpen, monClose, tueOpen, tueClose, wedOpen,
                                                      wedClose,
                                                      thuOpen, thuClose, friOpen, friClose, satOpen, satClose, sunOpen,
                                                      sunClose,
                                                      nightDrop, nightDropInstr, insertBy, insertDate, updateBy,
                                                      updateDate,
                                                      facAvailability, availEffDate, availExpDate))


@app.route('/updateFacilityManagersData')
def updateFacilityManagersData():
    facNum = str(request.args.get('facNum'))
    clubCode = str(request.args.get('clubCode'))
    managerId = str(request.args.get('managerId'))
    insertBy = str(request.args.get('insertBy'))
    insertDate = str(request.args.get('insertDate'))
    return str(inspectionApis.updateFacilityManagersData(facNum, clubCode, managerId, insertBy, insertDate))


@app.route('/updateFacilityLanguageData')
def updateFacilityLanguageData():
    facNum = str(request.args.get('facNum'))
    clubCode = str(request.args.get('clubCode'))
    langTypeId = str(request.args.get('langTypeId'))
    insertBy = str(request.args.get('insertBy'))
    insertDate = str(request.args.get('insertDate'))
    return str(inspectionApis.updateFacilityLanguageData(facNum, clubCode, langTypeId, insertBy, insertDate))


@app.route('/updateFacilityPhotosData')
def updateFacilityPhotosData():
    facNum = str(request.args.get('facNum'))
    clubCode = str(request.args.get('clubCode'))
    photoId = str(request.args.get('photoId'))
    fileName = str(request.args.get('fileName'))
    fileDescription = str(request.args.get('fileDescription'))
    primaryPhoto = str(request.args.get('primaryPhoto,'))
    approvalRequest = str(request.args.get('approvalRequest'))
    approved = str(request.args.get('approved'))
    seqNum = str(request.args.get('seqNum'))
    approvedBy = str(request.args.get('approvedBy'))
    approvedDate = str(request.args.get('approvedDate'))
    lastUpdateBy = str(request.args.get('lastUpdateBy,'))
    lastUpdateDate = str(request.args.get('lastUpdateDate'))
    return str(
        inspectionApis.updateFacilityPhotosData(facNum, clubCode, photoId, fileName, fileDescription, primaryPhoto,
                                                approvalRequest, approved, seqNum, approvedBy, approvedDate,
                                                lastUpdateBy, lastUpdateDate))


@app.route('/updateFacilityServiceProviderData')
def updateFacilityServiceProviderData():
    facNum = str(request.args.get('facNum'))
    clubCode = str(request.args.get('clubCode'))
    srvProviderId = str(request.args.get('srvProviderId'))
    providerNum = str(request.args.get('providerNum'))
    active = str(request.args.get('active'))
    insertBy = str(request.args.get('insertBy'))
    insertDate = str(request.args.get('insertDate'))
    updateBy = str(request.args.get('updateBy'))
    updateDate = str(request.args.get('updateDate'))
    return str(
        inspectionApis.updateFacilityServiceProviderData(facNum, clubCode, srvProviderId, providerNum, active, insertBy,
                                                         insertDate, updateBy, updateDate))


@app.route('/updateFacilityServicesData')
def updateFacilityServicesData(facNum, clubCode, facilityServicesId, serviceId, effDate, expDate, comments,
                               active, insertBy, insertDate, updateBy, updateDate):
    facNum = str(request.args.get('facNum'))
    clubCode = str(request.args.get('clubCode'))
    facilityServicesId = str(request.args.get('facilityServicesId'))
    serviceId = str(request.args.get('serviceId'))
    effDate = str(request.args.get('effDate'))
    expDate = str(request.args.get('expDate'))
    comments, = str(request.args.get('comments,'))
    active = str(request.args.get('active'))
    insertBy = str(request.args.get('insertBy'))
    insertDate = str(request.args.get('insertDate'))
    updateBy = str(request.args.get('updateBy'))
    updateDate = str(request.args.get('updateDate'))
    return str(
        inspectionApis.updateFacilityServicesData(facNum, clubCode, facilityServicesId, serviceId, effDate, expDate,
                                                  comments, active, insertBy, insertDate, updateBy, updateDate))


@app.route('/updateProgramsData')
def updateProgramsData(facNum, clubCode, programId, programTypeId, effDate, expDate, comments, active,
                       insertBy, insertDate, updateBy, updateDate):
    facNum = str(request.args.get('facNum'))
    clubCode = str(request.args.get('clubCode'))
    programId = str(request.args.get('programId'))
    programTypeId = str(request.args.get('programTypeId'))
    effDate = str(request.args.get('effDate'))
    expDate = str(request.args.get('expDate'))
    comments = str(request.args.get('comments'))
    active, = str(request.args.get('active,'))
    insertBy = str(request.args.get('insertBy'))
    insertDate = str(request.args.get('insertDate'))
    updateBy = str(request.args.get('updateBy'))
    updateDate = str(request.args.get('updateDate'))
    return str(inspectionApis.updateProgramsData(facNum, clubCode, programId, programTypeId, effDate, expDate, comments,
                                                 active, insertBy, insertDate, updateBy, updateDate))


@app.route('/updateSurveySoftwaresData')
def updateSurveySoftwaresData():
    facNum = str(request.args.get('facNum'))
    clubCode = str(request.args.get('clubCode'))
    softwareSurveyNum = str(request.args.get('softwareSurveyNum'))
    repairSoftwareId = str(request.args.get('repairSoftwareId'))
    repairSoftwareVersion = str(request.args.get('repairSoftwareVersion'))
    repairSoftwarePurchaseY = str(request.args.get('repairSoftwarePurchaseY'))
    repairSoftwarePurchaseAmt = str(request.args.get('repairSoftwarePurchaseAmt'))
    repairSoftwareMonthlyFee = str(request.args.get('repairSoftwareMonthlyFee'))
    repairSoftwareOnetimeFee = str(request.args.get('repairSoftwareOnetimeFee'))
    shopMgmtSoftwareName = str(request.args.get('shopMgmtSoftwareName'))
    shopMgmtSoftwareVersion = str(request.args.get('shopMgmtSoftwareVersion'))
    shopMgmtSoftwarePurcharY = str(request.args.get('shopMgmtSoftwarePurcharY'))
    shopMgmtSoftwarePurcharAmt = str(request.args.get('shopMgmtSoftwarePurcharAmt'))
    shopMgmtSoftwareMonthlyFee = str(request.args.get('shopMgmtSoftwareMonthlyFee'))
    shopMgmtSoftwareOnetimeFee = str(request.args.get('shopMgmtSoftwareOnetimeFee'))
    surveyCompleteDate = str(request.args.get('surveyCompleteDate'))
    insertBy = str(request.args.get('insertBy'))
    insertDate = str(request.args.get('insertDate'))
    updateBy = str(request.args.get('updateBy'))
    updateDate = str(request.args.get('updateDate'))
    return str(inspectionApis.updateSurveySoftwaresData(facNum, clubCode, softwareSurveyNum, repairSoftwareId,
                                                        repairSoftwareVersion, repairSoftwarePurchaseY,
                                                        repairSoftwarePurchaseAmt, repairSoftwareMonthlyFee,
                                                        repairSoftwareOnetimeFee, shopMgmtSoftwareName,
                                                        shopMgmtSoftwareVersion, shopMgmtSoftwarePurcharY,
                                                        shopMgmtSoftwarePurcharAmt, shopMgmtSoftwareMonthlyFee,
                                                        shopMgmtSoftwareOnetimeFee, surveyCompleteDate, insertBy,
                                                        insertDate, updateBy, updateDate))


@app.route('/updateVisitationDetailsData')
def updateVisitationDetailsData():
    facNum = str(request.args.get('facNum'))
    clubCode = str(request.args.get('clubCode'))
    staffTraining = str(request.args.get('staffTraining'))
    qualityControl = str(request.args.get('qualityControl'))
    aarSigns = str(request.args.get('aarSigns'))
    certificateOfApproval = str(request.args.get('certificateOfApproval'))
    memberBenefitPoster = str(request.args.get('memberBenefitPoster'))
    insertBy = str(request.args.get('insertBy'))
    insertDate = str(request.args.get('insertDate'))
    updateBy = str(request.args.get('updateBy'))
    updateDate = str(request.args.get('updateDate'))
    return str(inspectionApis.updateVisitationDetailsData(facNum, clubCode, staffTraining, qualityControl, aarSigns,
                                                          certificateOfApproval, memberBenefitPoster, insertBy,
                                                          insertDate, updateBy, updateDate))


@app.route('/updateFacilityVehicles')
def updateFacilityVehicles():
    facnum = str(request.args.get('facnum'))
    clubcode = str(request.args.get('clubcode'))
    vehicleId = str(request.args.get('vehicleId'))
    insertBy = str(request.args.get('insertBy'))
    insertDate = str(request.args.get('insertDate'))
    return str(inspectionApis.updateFacilityVehicles(facnum, clubcode, vehicleId, insertBy, insertDate))


@app.route('/updatePersonnelCertification')
def updatePersonnelCertification():
    facnum = str(request.args.get('facnum'))
    clubcode = str(request.args.get('clubcode'))
    personnelId = str(request.args.get('personnelId'))
    certId = str(request.args.get('certId'))
    certificationTypeId, = str(request.args.get('certificationTypeId,'))
    certificationDate = str(request.args.get('certificationDate'))
    expirationDate = str(request.args.get('expirationDate'))
    certDesc = str(request.args.get('certDesc'))
    insertBy = str(request.args.get('insertBy'))
    insertDate = str(request.args.get('insertDate'))
    updateBy, = str(request.args.get('updateBy,'))
    updateDate = str(request.args.get('updateDate'))
    active = str(request.args.get('active'))
    return str(inspectionApis.updatePersonnelCertification(facnum, clubcode, personnelId, certId, certificationTypeId,
                                                           certificationDate, expirationDate, certDesc, insertBy,
                                                           insertDate, updateBy, updateDate, active))


@app.route('/updateFacilityPersonnelSignerData')
def updateFacilityPersonnelSignerData():
    facnum = str(request.args.get('facnum'))
    clubcode = str(request.args.get('clubcode'))
    personnelId = str(request.args.get('personnelId'))
    addr1 = str(request.args.get('addr1'))
    addr2 = str(request.args.get('addr2'))
    city = str(request.args.get('city'))
    st = str(request.args.get('st'))
    zip = str(request.args.get('zip'))
    zip4 = str(request.args.get('zip4'))
    phone = str(request.args.get('phone'))
    email = str(request.args.get('email'))
    contractStartDate = str(request.args.get('contractStartDate'))
    contractEndDate = str(request.args.get('contractEndDate'))
    insertBy = str(request.args.get('insertBy'))
    insertDate = str(request.args.get('insertDate'))
    updateBy = str(request.args.get('updateBy'))
    updateDate = str(request.args.get('updateDate'))
    active = str(request.args.get('active'))
    return str(
        inspectionApis.updateFacilityPersonnelSignerData(facnum, clubcode, personnelId, addr1, addr2, city, st, zip,
                                                         zip4, phone, email, contractStartDate, contractEndDate,
                                                         insertBy, insertDate, updateBy, updateDate, active))


@app.route('/updateVehicleServices')
def updateVehicleServices():
    facnum = str(request.args.get('facnum'))
    clubcode = str(request.args.get('clubcode'))
    vehiclesTypeId = str(request.args.get('vehiclesTypeId'))
    scopeServiceId = str(request.args.get('scopeServiceId'))
    insertBy = str(request.args.get('insertBy'))
    return str(inspectionApis.updateVehicleServices(facnum, clubcode, vehiclesTypeId, scopeServiceId, insertBy))


@app.route('/updateAARPortalTracking')
def updateAARPortalTracking():
    facnum = str(request.args.get('facnum'))
    clubcode = str(request.args.get('clubcode'))
    trackingId = str(request.args.get('trackingId'))
    portalInspectionDate = str(request.args.get('portalInspectionDate'))
    loggedIntoPortal = str(request.args.get('loggedIntoPortal'))
    numberUnacknowledgedTows = str(request.args.get('numberUnacknowledgedTows'))
    inProgressTows = str(request.args.get('inProgressTows'))
    inProgressWalkIns = str(request.args.get('inProgressWalkIns'))
    insertBy = str(request.args.get('insertBy'))
    insertDate = str(request.args.get('insertDate'))
    updateBy = str(request.args.get('updateBy'))
    updateDate = str(request.args.get('updateDate'))
    active = str(request.args.get('active'))
    return str(
        inspectionApis.updateAARPortalTracking(facnum, clubcode, trackingId, portalInspectionDate, loggedIntoPortal,
                                               numberUnacknowledgedTows, inProgressTows, inProgressWalkIns, insertBy,
                                               insertDate, updateBy, updateDate, active))


@app.route('/updateVehicles')
def updateVehicles():
    facnum = str(request.args.get('facnum'))
    clubcode = str(request.args.get('clubcode'))
    vehicleid = str(request.args.get('vehicleid'))
    insertDate = str(request.args.get('insertDate'))
    insertBy = str(request.args.get('insertBy'))
    return str(inspectionApis.updateVehicles(facnum, clubcode, vehicleid, insertDate, insertBy))


@app.route('/<path:path>')
def catch_all(path):
    return '[]'


if __name__ == '__main__':
    app.run()
