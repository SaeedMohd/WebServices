import random
import os
from datetime import datetime
from flask import Flask, request, redirect, url_for
from flask import send_file
from werkzeug.utils import secure_filename
from InspectionAPIs import InspectionAPIs
from SendMail import sendMailTo
from SendMail import sendPDFTo
from static.DbConnection import *
import requests

class Group():
    Visitation = "Visitation"
    Facility = "Facility"
    SoS = "Scope Of Services"
    Deficiency = "Deficiency"
    Complaints = "Complaints"
    Billing = "Billing"
    Surveys = "Surveys"
    Photos = "Photos"
    Login = "Login"


class Screens():
    Visitation = "Visitation"
    General = "General Information"
    RSP = "RSP Tracking"
    Location = "Location & Contact Info"
    Personnel = "Personnel"
    VehicleServices = "Vehicle Services"
    FacilityServices = "Facility Services"
    Vehicles = "Vehicles"
    Programs = "Programs"
    Affiliations = "Affiliations"
    Deficiency = "Deficiency"
    Complaints = "Complaints"
    Photos = "Photos"
    LoginTrial = "Login Trial"
    ResetPassword= "Reset Password"


class Sections():
    Main = "Main"
    Admin = "Admin"
    Tracking = "Tracking"
    Address = "Address"
    Phone = "Phone"
    Email = "Email"
    Hours = "Hours"
    Night = "Night Drop"
    Languages = "Languages"
    Certifications = "Certifications"
    Detail = "Details"
    Signer = "Contract Signer"
    LoginSucceeded = "Success"
    LoginFailed = "Failed"
    ResetFailed = "Invalid Email"



UPLOAD_FOLDER = '/var/www/Inspection/WebServices/PRG/uploads'
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# "Server};Server=localhost,1401;Database=Inspection;uid=SA;pwd=InspectionDoesntHaveAStrongRootPass9211@")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploadFile', methods=['POST'])
def uploadFile():
    email = request.args.get('email')
    type = request.args.get('type')
    specialistEmail = request.args.get('specialistEmail')
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        sendPDFTo(specialistEmail,filename, type)
        sendPDFTo('Brandon.Rick@aaa-calif.com', filename, type)
        sendPDFTo('saeed@pacificresearchgroup.com', filename, type)
        return 'File uploded succesfully'


@app.route('/sendCompletedPDF')
def sendCompletedPDF():
    shopEmail = request.args.get('email')
    specialistEmail = request.args.get('specialistEmail')
    visitationID = request.args.get('visitationID')
    sendPDFTo(shopEmail, visitationID + "_VisitationDetails_ForShop.pdf", "Shop")
    sendPDFTo('Brandon.Rick@aaa-calif.com', visitationID+"_VisitationDetails_ForShop.pdf", "Shop")
    sendPDFTo(specialistEmail, visitationID + "_VisitationDetails_ForSpecialist.pdf", "Specialist")
    sendPDFTo('Brandon.Rick@aaa-calif.com', visitationID + "_VisitationDetails_ForSpecialist.pdf", "Specialist")
    # sendPDFTo('saeed@pacificresearchgroup.com', visitationID+"_VisitationDetails_ForSpecialist.pdf", "Specialist")
    return 'Success'


@app.route('/uploadPhoto', methods=['POST'])
def uploadPhoto():
    # facId = str(request.args.get('facId'))
    fileNameToSave = str(request.args.get('fileNameToSave'))
    if request.method == 'POST':
        file = request.files['file']
        # filename = secure_filename(facId+file.filename)
        filename = secure_filename(fileNameToSave)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'File uploded succesfully'

counter = 0

inspectionApis = InspectionAPIs()


def getRandomPass():
    s = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ#$%*"
    passlen = 8
    p = "".join(random.sample(s, passlen))
    return p


# @app.route('/logActiontoPRG')
def logAction(sessionid,facid,clubcode,userid,groupname,screenname,sectionname,datachanged,action):
    statement = "insert into tblPRGLogChanges values ('"+sessionid+"',"+facid+","+clubcode+",'"+userid+"','"+groupname+"','"+screenname+"','"+sectionname+"',"+action+",'"+datachanged+"',current_timestamp)"
    return str(DbConnection.updateDB(statement))


def saveCompletedVisitation(facid,clubcode,visitationid,visitationtype):
    statement = "insert into tblPRGCompletedVisitations values ("+facid+","+clubcode+",'"+visitationid+"',current_timestamp,'"+visitationtype+"')"
    return str(DbConnection.updateDB(statement))


def markVisitationLogAsCompleted(facid,clubcode,visitationtype):
    statement = "update tblPRGVisitationsLog set completed=1 where facid="+facid+" and clubcode=" + clubcode +" and visitationtype='"+visitationtype+"'"
    return str(DbConnection.updateDB(statement))


@app.route('/saveVisitedScreens')
def saveVisitedScreens():
    facid = request.args.get('facId')
    clubcode = request.args.get('clubCode')
    sessionid = request.args.get('sessionId')
    FacAnnualInspectionMonth = request.args.get('facAnnualInspectionMonth')
    InspectionCycle = request.args.get('inspectionCycle')
    UserID = request.args.get('userId')
    visitedScreens = request.args.get('visitedScreens')
    visitationtype = request.args.get('visitationType')
    cancelled = request.args.get('cancelled')
    result = DbConnection.getCountFromDB(
        "select count(1) from tblPRGVisitationsLog where facid="+facid+" and clubcode = "+clubcode+" and sessionid = '" + sessionid + "' and cancelled=0 and completed =0 and visitationtype = '"+visitationtype+"'")
    if result > 0:
        statement = "update tblPRGVisitationsLog set visitedscreens = '"+visitedScreens+"',changeDate=current_timestamp,cancelled="+cancelled+" where facid="+facid+" and clubcode = "+clubcode+" and sessionid = '" + sessionid + "' and cancelled=0 and completed =0 and sessionid = '" + sessionid + "' and visitationtype = '"+visitationtype+"'"
    else:
        statement = "update tblPRGVisitationsLog set cancelled=1,changeDate=current_timestamp where facid=" + facid + " and clubcode = " + clubcode + " and cancelled=0 and completed =0 and visitationtype = '" + visitationtype + "'"
        str(DbConnection.updateDB(statement))
        statement = "insert into tblPRGVisitationsLog values (" + facid + "," + clubcode + ",'" + sessionid + "'," + FacAnnualInspectionMonth + ",'" + InspectionCycle + "','" + visitationtype + "','" + UserID + "','" + visitedScreens + "',current_timestamp,0,0)"
    return str(DbConnection.updateDB(statement))



@app.route('/logTracking')
def logTracking():
    sessionId = request.args.get('sessionId')
    userId = request.args.get('userId')
    deviceId = request.args.get('deviceId')
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    statement = "insert into tblPRGDeviceTracking values ('"+sessionId+"','"+deviceId+"','"+userId+"','"+latitude+"','"+longitude+"',current_timestamp)"
    return str(DbConnection.updateDB(statement))


def logVisitationHeader(sessionid,facid,clubcode,userid,visitationType,visitationReason,emailPDF,emailTo,waiveVisitation,waiveComments,facilityRep,automotiveSpecialist,visitationId):
    saveCompletedVisitation(facid,clubcode,visitationId,visitationType)
    markVisitationLogAsCompleted(facid,clubcode,visitationType)
    result = DbConnection.getCountFromDB(
        "select count(1) from tblPRGVisitationHeader where facid=" + facid + " and clubcode = " + clubcode + " and visitationid =0 and visitationtype = '" + visitationType + "'")
    if result > 0: # to update currently in progress data
        statement = "update tblPRGVisitationHeader set userid='" + userid + "',changeDate=current_timestamp,visitationreason='" + visitationReason + "',emailpdf=" + emailPDF + ",emailto='" + emailTo + "',waivevisitation=" + waiveVisitation + ",waivecomments='" + waiveComments + "',facilityrep='" + facilityRep + "',automotiveSpecialist ='" + automotiveSpecialist + "',visitationid='" + visitationId + "' where facid="+facid+" and clubcode="+clubcode+" and visitationid =0 and visitationtype = '" + visitationType + "'"
    else:
        statement = "insert into tblPRGVisitationHeader values ('" + sessionid + "'," + facid + "," + clubcode + ",'" + userid + "',current_timestamp,'" + visitationType + "','" + visitationReason + "'," + emailPDF + ",'" + emailTo + "'," + waiveVisitation + ",'" + waiveComments + "','" + facilityRep + "','"+automotiveSpecialist+"','"+visitationId+"','','','','','')"
    return str(DbConnection.updateDB(statement))


def logVisitationHeaderProgress(sessionId, facid, clubcode, userId, visitationType, visitationReason, emailPDF,emailTo,waiveVisitation,waiveComments,facilityRep,automotiveSpecialist,visitationId,staffTraining,qualityControl,aarSigns,certificateOfApproval,memberBenefitPoster):
    result = DbConnection.getCountFromDB(
        "select count(1) from tblPRGVisitationHeader where facid=" + facid + " and clubcode =" + clubcode + " and visitationid=0 and visitationtype= '" + visitationType + "'")
    if result > 0:  # to update currently in progress data
        statement = "update tblPRGVisitationHeader set userid='" + userId + "',changeDate=current_timestamp,visitationreason='" + visitationReason + "',emailpdf=" + emailPDF + ",emailto='" + emailTo + "',waivevisitation=" + waiveVisitation + ",waivecomments='" + waiveComments + "',facilityrep='" + facilityRep + "',automotiveSpecialist ='" + automotiveSpecialist + "',visitationid='" + visitationId + "',staffTraining='"+staffTraining+"',qualityControl='"+qualityControl+"',aarSigns='"+aarSigns+"',certificateOfApproval='"+certificateOfApproval+"',memberBenefitPoster='"+memberBenefitPoster+"' where facid=" + facid + " and clubcode=" + clubcode + " and visitationid =0 and visitationtype = '" + visitationType + "'"
    else:
        statement = "insert into tblPRGVisitationHeader values ('" + sessionId + "'," + facid + "," + clubcode + ",'" + userId + "',current_timestamp,'" + visitationType + "','" + visitationReason + "'," + emailPDF + ",'" + emailTo + "'," + waiveVisitation + ",'" + waiveComments + "','" + facilityRep + "','" + automotiveSpecialist + "','" + visitationId + "','"+staffTraining+"','"+qualityControl+"','"+aarSigns+"','"+certificateOfApproval+"','"+memberBenefitPoster+"')"
    return str(DbConnection.updateDB(statement))


def getRequestParam(req, param):
    return req.args.get(param)


@app.route('/getAllFacilities')
def getAllFacilities():
    return DbConnection.queryCsiDB(
        "select distinct(RIGHT('00'+ CONVERT(VARCHAR,a.clubcode),3)) as clubcode, a.facnum, a.facname, b.AccSpecID as specialistid from csi.dbo.AAAFacilities a, csi.dbo.aaaspecialist b where a.SpecialistID = b.ID and a.acnm = 'aaaphone' and active = 1")
# "select clubcode, facnum, facname from csi.dbo.AAAFacilities where acnm = 'aaaphone' and active = 1")

# GET /api.asmx/SendTransactionalEmail?Username=string&Password=string&FromEmail=string&FromName=string&ToEmailAddress=string&Subject=string&MessagePlain=string&MessageHTML=string&Options=string HTTP/1.1

@app.route('/testJangoMail')
def testJangoMail():
    try:
        response = requests.post(
        url="https://api.jangomail.com/api.asmx/SendTransactionalEmail",
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
        },
            data={
                "Username": "pa32rt300t",
                "FromEmail": "NoReply@pacificresearchgroup.com",
                "Password": "Miles78!",
                "Subject": "TEST",
                "ToEmailAddress": "saeed@pacificresearchgroup.com",
                "FromName": "test",
                "MessageHTML": "",
                "MessagePlain": "YES PLAIN",
                "Options": "",
            },)
        return response.content
    except requests.exceptions.RequestException:
        return 'Fail'


@app.route('/getLoggedActions')
def getLoggedActions():
    facnum = request.args.get('facNum')
    clubcode = request.args.get('clubCode')
    userid = request.args.get('userId')
    return DbConnection.queryDb(
        "select * from tblPRGLogChanges where FacId="+facnum+" and ClubCode="+clubcode+" and userId='"+userid+"'")

@app.route('/getAllLoggedActions')
def getAllLoggedActions():
    return DbConnection.queryDb(
        "select * from tblPRGLogChanges order by changeDate desc")


@app.route('/getVisitationHeader')
def getVisitationHeader():
    facnum = request.args.get('facNum')
    clubcode = request.args.get('clubCode')
    return DbConnection.queryDb(
        "select top 1 * from tblPRGVisitationHeader where FacId="+facnum+" and ClubCode="+clubcode+" order by recordId desc")


@app.route('/getPRGCompletedVisitations')
def getPRGCompletedVisitations():
    return DbConnection.queryDb(
        "select * ,Month(CompletionDate) as completionmonth from tblPRGCompletedVisitations where completiondate>=current_timestamp - 90")


@app.route('/getPRGVisitationsLog')
def getPRGVisitationsLog():
    return DbConnection.queryDb(
        "select * ,Month(changeDate) as changemonth  from tblPRGVisitationsLog where changeDate>=current_timestamp - 90 and cancelled = 0 and completed=0")


@app.route('/getFacilityData')
def getFacilityData():
    facnum = request.args.get('facnum')
    clubcode = request.args.get('clubcode')
    return str(
        inspectionApis.getFacilityData(facnum, clubcode))

@app.route('/getFacilityEmails')
def getFacilityEmails():
    return DbConnection.getFacilityEmailsFromDB()


@app.route('/fillFacilityEmailsData')
def fillFacilityEmailsData():
    # facnum = request.args.get('facnum')
    # clubcode = request.args.get('clubcode')
    # result = getFacilityEmailsByFacNum('2033','252')
    # result += "\n" + getFacilityEmailsByFacNum('5266', '252')
    DbConnection.getFacNumAndClubs()
    return 'SUCCESS'


# @app.route('/getFacilityEmailsByFacNum')
@staticmethod
def getFacilityEmailsByFacNum(facnum,clubcode):
    # facnum = request.args.get('facnum')
    # clubcode = request.args.get('clubcode')
    result = str(inspectionApis.getFacilityData(facnum, clubcode))
    indexFrom = result.find("<tblFacilityEmail>")
    indexTo = result.rfind("</tblFacilityEmail>")
    result = result[indexFrom:indexTo + 19]
    emails = "FacNo:"+facnum+" - ClubCode:"+clubcode+" - emails:"
    while result.find("<email>")>-1:
        indexFrom = result.find("<email>")
        indexTo = result.find("</email>")
        emails += result[indexFrom+7:indexTo] + ","
        indexFrom = indexTo+8
        indexTo = result.rfind("</email>")+8
        result = result[indexFrom:indexTo ]
    return DbConnection.updateCsiDB("insert into AAAFacilityEmails values ("+facnum+",'"+clubcode+"','','','','"+emails[:-1]+"')")


@app.route('/getAllSpecialists')
def getAllSpecialists():
    # return queryCsiDB("select id, AccSpecID, specialistName from csi.dbo.aaaspecialist where acnm = 'aaaphone'")
    return DbConnection.queryCsiDB("exec csi.dbo.ACE_Specialists")


@app.route('/getClubCodes')
def getClubCodes():
    clubCodeQuery = str(request.args.get('clubCode'))
    queryString = "SELECT distinct(RIGHT('00'+ CONVERT(VARCHAR,clubcode),3)) AS clubcode FROM aaafacilities a where acnm = 'aaaphone' and active = 1"
    if clubCodeQuery is not None:
        queryString += " and RIGHT('00'+ CONVERT(VARCHAR,clubcode),3) like '" + clubCodeQuery + "%'"
    queryString += " order by 1"
    return DbConnection.queryCsiDB(queryString)


@app.route('/getFacilityPhotos')
def getFacilityPhotos():
    facId = request.args.get('facId')
    clubCode = request.args.get('clubCode')
    return DbConnection.queryDb("select * from tblFacilityPhotos where facid="+facId+" and clubCode="+clubCode)



@app.route('/getImage')
def get_image():
    file = request.args.get('file')
    filename = os.path.join(app.config['UPLOAD_FOLDER'], file)
    if os.path.isfile(filename):
        return send_file(filename)
    return ''

@app.route('/updateFacilityPhotos')
def updateFacilityPhotos():
    facId = request.args.get('facId')
    clubCode = request.args.get('clubCode')
    photoId = request.args.get('photoId')
    downstreamApps = str(request.args.get('downstreamApps'))
    fileDescription = str(request.args.get('fileDescription'))
    fileName = str(request.args.get('fileName'))
    lastUpdateBy = str(request.args.get('lastUpdateBy'))
    approvalRequested = request.args.get('approvalRequested')
    operation = str(request.args.get('operation'))
    if operation == 'EDIT':
        updateStatement = "update tblFacilityPhotos set clubCode="+clubCode+", downstreamapps='"+downstreamApps+"', filedescription='"+fileDescription+"' , lastUpdateBy='"+lastUpdateBy+"' , lastUpdateDate=current_timestamp , approvalrequested="+approvalRequested+" where facid=" + facId + "and photoid=" + photoId
    else :
        updateStatement = "insert into tblFacilityPhotos values ("+facId+",'"+fileName+"','"+fileDescription+"',"+approvalRequested+",0,'','','"+lastUpdateBy+"',current_timestamp,'"+downstreamApps+"',"+clubCode+")"
    result = str(DbConnection.updateDB(updateStatement))
    changeAction = str(request.args.get('changeAction'))
    dataChanged = str(request.args.get('dataChanged'))
    sessionId = str(request.args.get('sessionId'))
    userId = str(request.args.get('userId'))
    if 'Success' in result:
        logAction(sessionId, facId, clubCode, userId, Group.Photos, Screens.Photos, Sections.Main, dataChanged,
                  changeAction)
    return result


@app.route('/getSpecialistNameFromEmail')
def getSpecialistNameFromEmail():
    specialistEmail = request.args.get('specialistEmail')
    return DbConnection.queryCsiDB(
        "select clubcode, specialistName from csi.dbo.aaaspecialist where acnm = 'aaaphone' and lower(specialistemail) = lower('" + specialistEmail + "')")


@app.route('/getVisitationPlanningList')
def getVisitationPlanningList():
    facilityName = request.args.get('facilityName')
    month = request.args.get('month')
    year = request.args.get('year')
    if facilityName is not None and len(facilityName) > 0:
        return DbConnection.queryCsiDB(
            "select FacNum, facname, joindate from csi.dbo.aaafacilities where facname = '" + facilityName + "' and month(JoinDate) = " + month + " and year(JoinDate) < " + year)
    else:
        return DbConnection.queryCsiDB(
            "select FacNum, facname, joindate from csi.dbo.aaafacilities where month(JoinDate) = " + month + " and year(JoinDate) < " + year)


@app.route('/getFacilities')
def getFacilities():
    facilityName = str(request.args.get('facilityName')).lower()
    return DbConnection.queryDb(
        "select * from tblFacilities$ where active = 1 and BusinessName like '" + facilityName + "%'")


@app.route('/getFacilityWithId')
def getFacilityWithId():
    facilityId = request.args.get('facilityId')
    return DbConnection.queryDb("select * from tblFacilities$ where active = 1 and facId = " + facilityId)


@app.route('/getFacilitiesWithFilters')
def getFacilitiesWithFilters():
    facilityNumber = request.args.get('facilityNumber')
    clubCode = request.args.get('clubCode')
    dba = request.args.get('dba')
    assignedSpecialist = request.args.get('assignedSpecialist')
    contractStatus = request.args.get('contractStatus')
    queryString = "select RIGHT('00'+ CONVERT(VARCHAR,clubcode),3) as clubcode, facName, status, facNum from csi.dbo.aaafacilities where acnm = 'aaaphone' and RIGHT('00'+ CONVERT(VARCHAR,clubcode),3) like '%" + clubCode + "%' and facName like '%" + dba + "%'"
    if len(contractStatus) > 0:
        queryString += str(" and status = " + contractStatus)
    if len(facilityNumber) > 0:
        queryString += str(" and facNum like '%" + facilityNumber + "%'")
    if len(assignedSpecialist) > 0:
        queryString += str(
            " and specialistid = (select id from csi.dbo.aaaspecialist where accspecid = '" + assignedSpecialist + "')")
    return DbConnection.queryCsiDB(queryString)


@app.route('/getFacilityHours')
def getFacilityHours():
    facilityId = str(request.args.get('facilityId'))
    return DbConnection.queryDb("select * from tblHours$ where facid = " + facilityId)


@app.route('/getPersonnelTypes')
def getPersonnelTeypes():
    facilityId = str(request.args.get('facilityId'))
    return DbConnection.queryDb(
        "select distinct(personnelTypeName), a.PersonnelTypeID  from tblPersonnelType$ a, tblPersonnel$ b where a.PersonnelTypeID = b.PersonnelTypeID and FacID = " + facilityId)


@app.route('/getPersonnelsDetails')
def getPersonnelDetails():
    facilityId = str(request.args.get('facilityId'))
    personnelTypeId = str(request.args.get('personnelTypeId'))
    return DbConnection.queryDb(
        "select a.FacID, a.PersonnelID,a.PersonnelTypeID,a.FirstName,a.LastName,a.SeniorityDate,a.CertificationNum,a.startDate,a.endDate,a.ContractSigner,a.PrimaryMailRecipient,a.RSP_UserName,a.RSP_Email,a.RSP_Phone,b.Addr1,b.Addr2,b.CITY, case when (b.ST is not null) then (select LongDesc from tblStateMapping where ShortDesc=b.st) else null end as State ,b.ZIP,b.ZIP4,b.Phone,b.email,b.ContractStartDate,b.ContractEndDate from tblPersonnel$ a LEFT OUTER JOIN tblPersonnelSigner$ b on a.PersonnelID=b.PersonnelID where facid = " + facilityId + " and personnelTypeId = " + personnelTypeId)


@app.route('/getAllPersonnelsDetails')
def getAllPersonnelDetails():
    return DbConnection.queryDb(
        "select a.FacID, a.PersonnelID,a.PersonnelTypeID,a.FirstName,a.LastName,a.SeniorityDate,a.CertificationNum,a.startDate,a.endDate,a.ContractSigner,a.PrimaryMailRecipient,a.RSP_UserName,a.RSP_Email,a.RSP_Phone,b.Addr1,b.Addr2,b.CITY, case when (b.ST is not null) then (select LongDesc from tblStateMapping where ShortDesc=b.st) else null end as State ,b.ZIP,b.ZIP4,b.Phone,b.email,b.ContractStartDate,b.ContractEndDate from tblPersonnel$ a LEFT OUTER JOIN tblPersonnelSigner$ b on a.PersonnelID=b.PersonnelID")


@app.route('/getPersonnelDetailsWithId')
def getPersonnelDetailsWithId():
    personneId = str(request.args.get('personnelId'))
    return DbConnection.queryDb(
        "select a.FacID, a.PersonnelID,a.PersonnelTypeID,a.FirstName,a.LastName,a.SeniorityDate,a.CertificationNum,a.startDate,a.endDate,a.ContractSigner,a.PrimaryMailRecipient,a.RSP_UserName,a.RSP_Email,a.RSP_Phone,b.Addr1,b.Addr2,b.CITY, case when (b.ST is not null) then (select LongDesc from tblStateMapping where ShortDesc=b.st) else null end as State ,b.ZIP,b.ZIP4,b.Phone,b.email,b.ContractStartDate,b.ContractEndDate from tblPersonnel$ a LEFT OUTER JOIN tblPersonnelSigner$ b on a.PersonnelID=b.PersonnelID where a.personnelId = " + personneId)


@app.route('/getScopeOfServicDetails')
def getScopeOfService():
    facilityId = str(request.args.get('facilityId'))
    return DbConnection.queryDb("select * from tblScopeofService$ where FACID = " + facilityId)


@app.route('/getVehicleServicesForFacility')
def getVehicleServicesForFaacility():
    facilityId = str(request.args.get('facilityId'))
    return DbConnection.queryDb(
        "select * from tblScopeofServiceType$ a, tblVehicleServices$ b where a.ScopeServiceID = b.ScopeServiceID and a.active = 1 and FACID = " + facilityId)


@app.route('/getPaymentMethods')
def getPaymentMethods():
    return DbConnection.queryDb("select * from tblPaymentMethodsType$ where active = 1")


@app.route('/getFacilityAddresses')
def getFacilityAddresses():
    facilityId = str(request.args.get('facilityId'))
    return DbConnection.queryDb(
        "select a.*, b.LocTypeName from tblAddress$ a, tblLocationType$ b where a.LocationTypeID = b.LocTypeID and facid = " + facilityId + " and a.active = 1 and b.active = 1")


@app.route('/getProgramTypes')
def getProgramTypes():
    return DbConnection.queryDb("SELECT programtypeid,programtypename from tblProgramsType$ where active=1")


# @app.route('/getFacilityComplaints')
# def getFacilityComplaints():
#     facilityId = str(request.args.get('facilityId'))
#     return DbConnection.queryDb(
#         "select a.RecordID,a.ComplaintID,a.FirstName,a.LastName,a.ReceivedDate,c.ComplaintReasonName,(select count(1) from tblComplaintFiles$ cf where a.FACID=cf.FACID and cf.ReceivedDate>=current_timestamp-365) as NoOfComplaintsLastYear from tblComplaintFiles$ a,tblComplaintFilesReason$ b, tblComplaintFilesReasonType$ c where a.RecordID=b.ComplaintRecordID and b.ComplaintReasonID=c.ComplaintReasonID and ComplaintNotCounted=0 and FACID = " + facilityId)

@app.route('/getFacilityEmailsFromDB')
def getFacilityEmailsFromDB():
    return DbConnection.queryDb(
        "select FacID,'EMAIL' as ContactType,emailTypeId as 'TYPE',case (emailTypeId) when 0 then 'Business' else 'Personal' END as 'TypeName',email as 'ContactDetail' from tblFacilityEmail$")


@app.route('/getFacilityEmailAndPhone')
def getFacilityEmailaAndPhone():
    facilityId = str(request.args.get('facilityId'))
    return DbConnection.queryDb(
        "select FacID,'EMAIL' as ContactType,emailTypeId as 'TYPE',case (emailTypeId) when 0 then 'Business' else 'Personal' END as 'TypeName',email as 'ContactDetail' from tblFacilityEmail$ a where FacID=" + facilityId + " union All select FacID,'PHONE',PhoneTypeID,case (PhoneTypeID) when 0 then 'Business' when 1 then 'Cell' when 2 then 'Fax' else 'Home' END ,LTRIM(str(PhoneNumber,20)) from tblPhone$ where FacID=" + facilityId)


@app.route('/getVisitationRecords')
def getVisitationRecords():
    facilityName = str(request.args.get('facilityName'))
    inspectionType = str(request.args.get('inspectionType'))
    if inspectionType == '0':
        return DbConnection.queryDb(
            "select a.facID, a.visitationID, a.performedBy, a.DatePerformed, a.DatePlanned, c.businessName as name, case when(DatePlanned is not null) then 'Planned Visitation' else 'New Visitation' end as InspectionStatus from tblVisitationRecords a, tblInspectiontypes b, tblFacilities$ c where a.facID = c.FacID and  a.InspectionType = b.id and (BusinessName like '%" + facilityName + "%' or EntityName like '%" + facilityName + "%')")
    else:
        return DbConnection.queryDb(
            "select a.facID, a.visitationID, a.performedBy, a.DatePerformed, a.DatePlanned, c.businessName as name, case when(DatePlanned is not null) then 'Planned Visitation' else 'New Visitation' end as InspectionStatus from tblVisitationRecords a, tblInspectiontypes b, tblFacilities$ c where a.facID = c.FacID and  a.InspectionType = b.id and (BusinessName like '%" + facilityName + "%' or EntityName like '%" + facilityName + "%') and a.InspectionType = " + inspectionType)


@app.route('/getContractSignerDetails')
def getContractSignerDetails():
    personnelId = str(request.args.get('personnelId'))
    return DbConnection.queryDb(
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

    return DbConnection.queryDb(queryString)


@app.route('/getLastAnnualVisitationInspectionForFacility')
def getLastAnnualVisitationInspectionForFacility():
    facilityId = str(request.args.get('facilityId'))
    return DbConnection.queryDb(
        "select * from tblAnnualVisitationInspectionFormData where facilityId=" + facilityId)


@app.route('/getPhoneNumberWithFacilityAndId')
def getPhoneNumberWithFacilityAndId():
    facilityId = str(request.args.get('facilityId'))
    phoneId = str(request.args.get('phoneId'))
    return DbConnection.queryDb(
        "select * from tblPhone$ a where FacID = " + facilityId + " and phoneId = " + phoneId + " and active = 1")


@app.route('/getEmailFromFacilityAndId')
def getEmailFromFacilityAndId():
    facilityId = str(request.args.get('facilityId'))
    emailId = str(request.args.get('emailId'))
    return DbConnection.queryDb(
        "select * from tblFacilityEmail$ where facId = " + facilityId + " and emailId = " + emailId + "")


@app.route('/getVehicleServices')
def getVehicleServices():
    return DbConnection.queryDb(
        "select * from tblScopeofServiceType$ where active = 1 order by scopeservicename")


@app.route('/getFacilityPrograms')
def getFacilityPrograms():
    facilityId = str(request.args.get('facilityId'))
    return DbConnection.queryDb(
        "select ProgramID,ProgramTypeName,effDate,expDate,Comments from tblPrograms$ a, tblProgramsType$ b where a.ProgramTypeID=b.ProgramTypeID and a.active=1 and FACID=" + facilityId)


@app.route('/getVehicles')
def getVehicles():
    return DbConnection.queryDb(
        "select * from tblVehicleMakesType$ where active = 1 order by 2")


@app.route('/getAffiliationTypes')
def getAffiliationTypes():
    return DbConnection.queryDb(
        "select a.typeID,typeName,typeDetailID,typeDetailName from tblAffiliationType a left OUTER JOIN tblAffiliationTypeDetail b on a.typeID=b.typeID")


@app.route('/getFacilityAffiliations')
def getFacilityAffiliations():
    facilityId = str(request.args.get('facilityId'))
    return DbConnection.queryDb(
        "select a.AffiliationID,b.typeName,(select typeDetailName from tblAffiliationTypeDetail where typeDetailID=AffiliationTypeDetailID) as typeDetailName ,effDate,expDate,comment from tblAffiliations$ a, tblAffiliationType b where a.AffiliationTypeID=b.typeID and a.active=1 and FACID=" + facilityId)


@app.route('/getFacilityComplaints')
def getFacilityComplaints():
    facilityId = str(request.args.get('facilityId'))
    all = str(request.args.get('all'))
    if all == 'true':
        return DbConnection.queryDb(
            "select a.RecordID,a.ComplaintID,a.FirstName,a.LastName,a.ReceivedDate,c.ComplaintReasonName,f.ComplaintResolutionName,(select count(1) from tblComplaintFiles$ cf where a.FACID=cf.FACID and cf.ReceivedDate<=current_timestamp) as NoOfComplaintsLastYear, (select count(1) from tblComplaintFiles$ cf,tblComplaintFilesResolution$ cfr, tblComplaintFilesResolutionType$ cfrt where a.FACID=cf.FACID and cfr.ComplaintRecordID=cf.RecordID and cfr.ComplaintResolutionID=cfrt.ComplaintResolutionID and cf.ReceivedDate<=current_timestamp and lower(ComplaintResolutionName) ='justified') as NoOfJustifiedLastYear, (FacilityRepairOrderCount*12) as TotalOrders, '' as comments from tblComplaintFiles$ a,tblComplaintFilesReason$ b, tblComplaintFilesReasonType$ c,tblFacilities$ d, tblComplaintFilesResolution$ e, tblComplaintFilesResolutionType$ f where a.RecordID=b.ComplaintRecordID and b.ComplaintReasonID=c.ComplaintReasonID and a.RecordID=e.ComplaintRecordID and e.ComplaintResolutionID=f.ComplaintResolutionID and ComplaintNotCounted=0 and a.FACID=d.FacID and ReceivedDate<=current_timestamp and a.FACID=" + facilityId)
    else:
        return DbConnection.queryDb(
            "select a.RecordID,a.ComplaintID,a.FirstName,a.LastName,a.ReceivedDate,c.ComplaintReasonName,f.ComplaintResolutionName,(select count(1) from tblComplaintFiles$ cf where a.FACID=cf.FACID and cf.ReceivedDate>=current_timestamp-365) as NoOfComplaintsLastYear, (select count(1) from tblComplaintFiles$ cf,tblComplaintFilesResolution$ cfr, tblComplaintFilesResolutionType$ cfrt where a.FACID=cf.FACID and cfr.ComplaintRecordID=cf.RecordID and cfr.ComplaintResolutionID=cfrt.ComplaintResolutionID and cf.ReceivedDate>=current_timestamp-365 and lower(ComplaintResolutionName) ='justified') as NoOfJustifiedLastYear, (FacilityRepairOrderCount*12) as TotalOrders, '' as comments from tblComplaintFiles$ a,tblComplaintFilesReason$ b, tblComplaintFilesReasonType$ c,tblFacilities$ d, tblComplaintFilesResolution$ e, tblComplaintFilesResolutionType$ f where a.RecordID=b.ComplaintRecordID and b.ComplaintReasonID=c.ComplaintReasonID and a.RecordID=e.ComplaintRecordID and e.ComplaintResolutionID=f.ComplaintResolutionID and ComplaintNotCounted=0 and a.FACID=d.FacID and ReceivedDate>=current_timestamp-365 and a.FACID=" + facilityId)


@app.route('/updatePaymentMethodsData')
def updatePaymentMethodsData():
    facNum = str(request.args.get('facnum'))
    clubCode = str(request.args.get('clubcode'))
    paymentMethodID = str(request.args.get('paymentMethodID'))
    insertBy = str(request.args.get('insertBy'))
    insertDate = str(request.args.get('insertDate'))
    result = str(inspectionApis.updatePaymentMethodsData(facNum, clubCode, paymentMethodID, insertBy, insertDate))
    changeAction = str(request.args.get('changeAction'))
    dataChanged = str(request.args.get('dataChanged'))
    sessionId = str(request.args.get('sessionId'))
    userId = str(request.args.get('userId'))
    if 'returnCode>0<' in result:
        logAction(sessionId, facNum, clubCode,userId ,Group.Facility, Screens.General, Sections.Main, dataChanged, changeAction)
    return result


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
    result = str(
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
    changeAction = str(request.args.get('changeAction'))
    dataChanged = str(request.args.get('dataChanged'))
    sessionId = str(request.args.get('sessionId'))
    userId = str(request.args.get('userId'))
    if 'returnCode>0<' in result:
        logAction(sessionId, facNum,clubCode, userId, Group.Facility, Screens.General, Sections.Main, dataChanged, changeAction)
    return result


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
    result = str(
        inspectionApis.updateFacilityAddressData(facnum, clubcode, locationTypeID, FAC_Addr1, FAC_Addr2, CITY, ST, ZIP,
                                                 Country, BranchName, BranchNumber, LATITUDE, LONGITUDE, insertBy,
                                                 insertDate, updateBy, updateDate, active))
    changeAction = str(request.args.get('changeAction'))
    dataChanged = str(request.args.get('dataChanged'))
    sessionId = str(request.args.get('sessionId'))
    userId = str(request.args.get('userId'))
    if 'returnCode>0<' in result:
        logAction(sessionId, facnum,clubcode, userId, Group.Facility, Screens.Location, Sections.Address, dataChanged, changeAction)
    return result


@app.route('/updateFacilityEmailData')
def updateFacilityEmailData():
    facNum = str(request.args.get('facnum'))
    clubCode = str(request.args.get('clubcode'))
    emailId = str(request.args.get('emailId'))
    emailTypeId = str(request.args.get('emailTypeId'))
    email = str(request.args.get('email'))
    insertBy = str(request.args.get('insertBy'))
    insertDate = str(request.args.get('insertDate'))
    updateBy = str(request.args.get('updateBy'))
    updateDate = str(request.args.get('updateDate'))
    active = str(request.args.get('active'))
    result = str(
        inspectionApis.updateFacilityEmailData(facNum, clubCode, emailId, emailTypeId, email, insertBy, insertDate,
                                               updateBy, updateDate, active))
    changeAction = str(request.args.get('changeAction'))
    dataChanged = str(request.args.get('dataChanged'))
    sessionId = str(request.args.get('sessionId'))
    userId = str(request.args.get('userId'))
    if 'returnCode>0<' in result:
        logAction(sessionId, facNum, clubCode, userId, Group.Facility, Screens.Location, Sections.Email, dataChanged, changeAction)
    return result



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
    result = str(inspectionApis.updateFacilityPhoneData(facNum, clubCode, phoneId, phoneTypeId, phoneNumber, extension,
                                                      description, insertBy, insertDate, updateBy, updateDate, active))
    changeAction = str(request.args.get('changeAction'))
    dataChanged = str(request.args.get('dataChanged'))
    sessionId = str(request.args.get('sessionId'))
    userId = str(request.args.get('userId'))
    if 'returnCode>0<' in result:
        logAction(sessionId, facNum, clubCode, userId, Group.Facility, Screens.Location, Sections.Phone, dataChanged,
                  changeAction)
    return result



@app.route('/updateFacilityPersonnelData')
def updateFacilityPersonnelData():
    facNum = str(request.args.get('facNum'))
    clubCode = str(request.args.get('clubCode'))
    personnelId = str(request.args.get('personnelId'))
    personnelTypeId = str(request.args.get('personnelTypeId'))
    firstName = str(request.args.get('firstName'))
    lastName = str(request.args.get('lastName'))
    seniorityDate = str(request.args.get('seniorityDate'))
    certificationNum = str(request.args.get('certificationNum'))
    startDate = str(request.args.get('startDate'))
    endDate = str(request.args.get('endDate'))
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
    result = str(
        inspectionApis.updateFacilityPersonnelData(facNum, clubCode, personnelId, personnelTypeId, firstName, lastName,
                                                   seniorityDate, certificationNum, startDate, endDate, contractSigner,
                                                   insertBy, insertDate, updateBy, updateDate, active,
                                                   primaryMailRecipient,rsp_userName, rsp_email, rsp_phone))
    changeAction = str(request.args.get('changeAction'))
    dataChanged = str(request.args.get('dataChanged'))
    sessionId = str(request.args.get('sessionId'))
    userId = str(request.args.get('userId'))
    if 'returnCode>0<' in result:
        logAction(sessionId, facNum, clubCode, userId, Group.Facility, Screens.Personnel, Sections.Main, dataChanged,
                  changeAction)
    return result


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
    result = str(
        inspectionApis.updateScopeOfServiceData(facNum, clubCode, laborRateId, fixedLaborRate, laborMin, laborMax,
                                                diagnosticRate, numOfBays, numOfLifts, warrantyTypeId, active,
                                                insertBy, insertDate, updateBy, updateDate))
    changeAction = str(request.args.get('changeAction'))
    dataChanged = str(request.args.get('dataChanged'))
    sessionId = str(request.args.get('sessionId'))
    userId = str(request.args.get('userId'))
    if 'returnCode>0<' in result:
        logAction(sessionId, facNum, clubCode, userId, Group.SoS, Screens.General, Sections.Main, dataChanged,
                  changeAction)
    return result



@app.route('/updateVisitationTrackingData')
def updateVisitationTrackingData():
    facNum = str(request.args.get('facnum'))
    clubCode = str(request.args.get('clubcode'))
    visitationId = str(request.args.get('visitationID'))
    performedBy = str(request.args.get('performedBy'))
    datePerformed = str(request.args.get('DatePerformed'))
    dateReceived = str(request.args.get('DateReceived'))
    insertBy = str(request.args.get('insertBy'))
    insertDate = str(request.args.get('insertDate'))
    updateBy = str(request.args.get('updateBy'))
    updateDate = str(request.args.get('updateDate'))
    result = str(inspectionApis.updateVisitationTrackingData(facNum, clubCode, visitationId, performedBy, datePerformed,
                                                           dateReceived, insertBy, insertDate, updateBy, updateDate))
    changeAction = str(request.args.get('changeAction'))
    dataChanged = str(request.args.get('dataChanged'))
    sessionId = str(request.args.get('sessionId'))
    userId = str(request.args.get('userId'))
    if 'returnCode>0<' in result:
        logAction(sessionId, facNum, clubCode, userId, Group.Visitation, Screens.Visitation, Sections.Tracking, dataChanged,
                  changeAction)
    return result



@app.route('/updateAARPortalAdminData')
def updateAARPortalAdminData():
    facNum = str(request.args.get('facNum'))
    clubCode = str(request.args.get('clubCode'))
    facId = str(request.args.get('facId'))
    startDate = str(request.args.get('startDate'))
    endDate = str(request.args.get('endDate'))
    addendumSigned = str(request.args.get('AddendumSigned'))
    cardReaders = str(request.args.get('cardReaders'))
    insertBy = str(request.args.get('insertBy'))
    insertDate = str(request.args.get('insertDate'))
    updateBy = str(request.args.get('updateBy'))
    updateDate = str(request.args.get('updateDate'))
    active = str(request.args.get('active'))
    result = str(
        inspectionApis.updateAARPortalAdminData(facNum, clubCode, facId, startDate, endDate, addendumSigned,
                                                cardReaders,
                                                insertBy, insertDate, updateBy, updateDate, active))
    changeAction = str(request.args.get('changeAction'))
    dataChanged = str(request.args.get('dataChanged'))
    sessionId = str(request.args.get('sessionId'))
    userId = str(request.args.get('userId'))
    if 'returnCode>0<' in result:
        logAction(sessionId, facNum, clubCode, userId, Group.Facility, Screens.RSP, Sections.Admin, dataChanged,
                  changeAction)
    return result


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
    result = str(inspectionApis.updateAffiliationsData(facNum, clubCode, affiliationId, affiliationTypeId,
                                                     affiliationTypeDetailsId, effDate, expDate, comment, active,
                                                     insertBy, insertDate, updateBy, updateDate))
    changeAction = str(request.args.get('changeAction'))
    dataChanged = str(request.args.get('dataChanged'))
    sessionId = str(request.args.get('sessionId'))
    userId = str(request.args.get('userId'))
    if 'returnCode>0<' in result:
        logAction(sessionId, facNum, clubCode, userId, Group.SoS, Screens.Affiliations, Sections.Main, dataChanged,
                  changeAction)
    return result


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
    result = str(
        inspectionApis.updateAmendmentOrderTrackingData(facNum, clubCode, facId, aoId, employeeId, reasonId, insertBy,
                                                        insertDate, updateBy, updateDate, active))
    changeAction = str(request.args.get('changeAction'))
    dataChanged = str(request.args.get('dataChanged'))
    sessionId = str(request.args.get('sessionId'))
    userId = str(request.args.get('userId'))
    if 'returnCode>0<' in result:
        logAction(sessionId, facNum, clubCode, userId, Group.Facility, Screens.RSP, Sections.Tracking, dataChanged,
                  changeAction)
    return result


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
    result = str(inspectionApis.updateDeficiencyData(facNum, clubCode, defId, defTypeId, visitationDate, enteredDate,
                                                   clearedDate, comments, insertBy, insertDate, updateBy, updateDate))
    changeAction = str(request.args.get('changeAction'))
    dataChanged = str(request.args.get('dataChanged'))
    sessionId = str(request.args.get('sessionId'))
    userId = str(request.args.get('userId'))
    if 'returnCode>0<' in result:
        logAction(sessionId, facNum, clubCode, userId, Group.Deficiency, Screens.Deficiency, Sections.Main, dataChanged,
                  changeAction)
    return result


@app.route('/updateComplaintFilesData')
def updateComplaintFilesData():
    facnum = str(request.args.get('facnum'))
    clubcode = str(request.args.get('clubcode'))
    RecordID = str(request.args.get('RecordID'))
    ComplaintID = str(request.args.get('ComplaintID'))
    FACID = str(request.args.get('FACID'))
    initiatedBy = str(request.args.get('initiatedBy'))
    IsTowIn = str(request.args.get('IsTowIn'))
    IsOutofState = str(request.args.get('IsOutofState'))
    SOSSID = str(request.args.get('SOSSID'))
    FirstName = str(request.args.get('FirstName'))
    LastName = str(request.args.get('LastName'))
    ComplaintNotCounted = str(request.args.get('ComplaintNotCounted'))
    IsERSComplaint = str(request.args.get('IsERSComplaint'))
    AssignedTo = str(request.args.get('AssignedTo'))
    ComplaintReasonID = str(request.args.get('ComplaintReasonID'))
    ComplaintResolutionID = str(request.args.get('ComplaintResolutionID'))
    ReceivedDate = str(request.args.get('ReceivedDate'))
    OpenedDate = str(request.args.get('OpenedDate'))
    ClosedDate = str(request.args.get('ClosedDate'))
    SecondOpenedDate = str(request.args.get('SecondOpenedDate'))
    SecondClosedDate = str(request.args.get('SecondClosedDate'))
    WorkDaysNotCounted = str(request.args.get('WorkDaysNotCounted'))
    insertBy = str(request.args.get('insertBy'))
    insertDate = str(request.args.get('insertDate'))
    updateBy = str(request.args.get('updateBy'))
    updateDate = str(request.args.get('updateDate'))
    result = str(
        inspectionApis.updateComplaintFilesData(facnum, clubcode, RecordID, ComplaintID, FACID, initiatedBy, IsTowIn,
                                                IsOutofState, SOSSID, FirstName, LastName, ComplaintNotCounted,
                                                IsERSComplaint, AssignedTo, ComplaintReasonID, ComplaintResolutionID,
                                                ReceivedDate, OpenedDate, ClosedDate, SecondOpenedDate,
                                                SecondClosedDate, WorkDaysNotCounted, insertBy, insertDate, updateBy,
                                                updateDate))
    changeAction = str(request.args.get('changeAction'))
    dataChanged = str(request.args.get('dataChanged'))
    sessionId = str(request.args.get('sessionId'))
    userId = str(request.args.get('userId'))
    if 'returnCode>0<' in result:
        logAction(sessionId, facnum, clubcode, userId, Group.Complaints, Screens.Complaints, Sections.Main, dataChanged,
                  changeAction)
    return result


@app.route('/updateFacilityClosureData')
def updateFacilityClosureData():
    facNum = str(request.args.get('facNum'))
    clubCode = str(request.args.get('clubCode'))
    facilityClosureId = str(request.args.get('facilityClosureId'))
    closureId = str(request.args.get('closureId'))
    effDate = str(request.args.get('effDate'))
    expDate = str(request.args.get('expDate'))
    comments = str(request.args.get('comments'))
    active = str(request.args.get('active'))
    insertBy = str(request.args.get('insertBy'))
    insertDate = str(request.args.get('insertDate'))
    updateBy = str(request.args.get('updateBy'))
    updateDate = str(request.args.get('updateDate'))
    prgFacilityClosureId = str(request.args.get('prgFacilityClosureId'))
    result = str(
        inspectionApis.updateFacilityClosureData(facNum, clubCode, facilityClosureId, closureId, effDate, expDate,
                                                 comments, active, insertBy, insertDate, updateBy, updateDate,
                                                 prgFacilityClosureId))
    changeAction = str(request.args.get('changeAction'))
    dataChanged = str(request.args.get('dataChanged'))
    sessionId = str(request.args.get('sessionId'))
    userId = str(request.args.get('userId'))
    if 'returnCode>0<' in result:
        logAction(sessionId, facNum, clubCode, userId, Group.Facility, Screens.General, Sections.Main, dataChanged,
                  changeAction)
    return result


@app.route('/updateFacilityHoursData')
def updateFacilityHoursData():
    facNum = str(request.args.get('facNum'))
    clubCode = str(request.args.get('clubCode'))
    monOpen = str(request.args.get('monOpen'))
    monClose = str(request.args.get('monClose'))
    tueOpen = str(request.args.get('tueOpen'))
    tueClose = str(request.args.get('tueClose'))
    wedOpen = str(request.args.get('wedOpen'))
    wedClose = str(request.args.get('wedClose'))
    thuOpen = str(request.args.get('thuOpen'))
    thuClose = str(request.args.get('thuClose'))
    friOpen = str(request.args.get('friOpen'))
    friClose = str(request.args.get('friClose'))
    satOpen = str(request.args.get('satOpen'))
    satClose = str(request.args.get('satClose'))
    sunOpen = str(request.args.get('sunOpen'))
    sunClose = str(request.args.get('sunClose'))
    nightDrop = str(request.args.get('nightDrop'))
    nightDropInstr = str(request.args.get('nightDropInstr'))
    insertBy = str(request.args.get('insertBy'))
    insertDate = str(request.args.get('insertDate'))
    updateBy = str(request.args.get('updateBy'))
    updateDate = str(request.args.get('updateDate'))
    facAvailability = str(request.args.get('facAvailability'))
    availEffDate = str(request.args.get('availEffDate'))
    availExpDate = str(request.args.get('availExpDate'))
    result = str(inspectionApis.updateFacilityHoursData(facNum, clubCode, monOpen, monClose, tueOpen, tueClose, wedOpen,
                                                      wedClose,
                                                      thuOpen, thuClose, friOpen, friClose, satOpen, satClose, sunOpen,
                                                      sunClose,
                                                      nightDrop, nightDropInstr, insertBy, insertDate, updateBy,
                                                      updateDate,
                                                      facAvailability, availEffDate, availExpDate))
    changeAction = str(request.args.get('changeAction'))
    dataChanged = str(request.args.get('dataChanged'))
    sessionId = str(request.args.get('sessionId'))
    userId = str(request.args.get('userId'))
    if 'returnCode>0<' in result:
        logAction(sessionId, facNum, clubCode, userId, Group.Facility, Screens.Location, Sections.Hours, dataChanged,
                  changeAction)
    return result


@app.route('/updateFacilityManagersData')
def updateFacilityManagersData():
    facNum = str(request.args.get('facNum'))
    clubCode = str(request.args.get('clubCode'))
    managerId = str(request.args.get('managerId'))
    insertBy = str(request.args.get('insertBy'))
    insertDate = str(request.args.get('insertDate'))
    result = str(inspectionApis.updateFacilityManagersData(facNum, clubCode, managerId, insertBy, insertDate))
    changeAction = str(request.args.get('changeAction'))
    dataChanged = str(request.args.get('dataChanged'))
    sessionId = str(request.args.get('sessionId'))
    userId = str(request.args.get('userId'))
    if 'returnCode>0<' in result:
        logAction(sessionId, facNum, clubCode, userId, Group.Facility, Screens.General, Sections.Main, dataChanged,
                  changeAction)
    return result


@app.route('/updateFacilityLanguageData')
def updateFacilityLanguageData():
    facNum = str(request.args.get('facNum'))
    clubCode = str(request.args.get('clubCode'))
    langTypeId = str(request.args.get('langTypeId'))
    insertBy = str(request.args.get('insertBy'))
    insertDate = str(request.args.get('insertDate'))
    result = str(inspectionApis.updateFacilityLanguageData(facNum, clubCode, langTypeId, insertBy, insertDate))
    changeAction = str(request.args.get('changeAction'))
    dataChanged = str(request.args.get('dataChanged'))
    sessionId = str(request.args.get('sessionId'))
    userId = str(request.args.get('userId'))
    if 'returnCode>0<' in result:
        logAction(sessionId, facNum, clubCode, userId, Group.Facility, Screens.Location, Sections.Languages, dataChanged,
                  changeAction)
    return result


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
    result = str(
        inspectionApis.updateFacilityPhotosData(facNum, clubCode, photoId, fileName, fileDescription, primaryPhoto,
                                                approvalRequest, approved, seqNum, approvedBy, approvedDate,
                                                lastUpdateBy, lastUpdateDate))
    changeAction = str(request.args.get('changeAction'))
    dataChanged = str(request.args.get('dataChanged'))
    sessionId = str(request.args.get('sessionId'))
    userId = str(request.args.get('userId'))
    if 'returnCode>0<' in result:
        logAction(sessionId, facNum, clubCode, userId, Group.Photos, Screens.Photos, Sections.Main, dataChanged,
                  changeAction)
    return result


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
    result = str(
        inspectionApis.updateFacilityServiceProviderData(facNum, clubCode, srvProviderId, providerNum, active, insertBy,
                                                         insertDate, updateBy, updateDate))
    changeAction = str(request.args.get('changeAction'))
    dataChanged = str(request.args.get('dataChanged'))
    sessionId = str(request.args.get('sessionId'))
    userId = str(request.args.get('userId'))
    if 'returnCode>0<' in result:
        logAction(sessionId, facNum, clubCode, userId, Group.Facility, Screens.General, Sections.Main, dataChanged,
                  changeAction)
    return result


@app.route('/updateFacilityServicesData')
def updateFacilityServicesData():
    facNum = str(request.args.get('facNum'))
    clubCode = str(request.args.get('clubCode'))
    facilityServicesId = str(request.args.get('facilityServicesId'))
    serviceId = str(request.args.get('serviceId'))
    effDate = str(request.args.get('effDate'))
    expDate = str(request.args.get('expDate'))
    comments = str(request.args.get('comments'))
    active = str(request.args.get('active'))
    insertBy = str(request.args.get('insertBy'))
    insertDate = str(request.args.get('insertDate'))
    updateBy = str(request.args.get('updateBy'))
    updateDate = str(request.args.get('updateDate'))
    result = str(
        inspectionApis.updateFacilityServicesData(facNum, clubCode, facilityServicesId, serviceId, effDate, expDate,
                                                  comments, active, insertBy, insertDate, updateBy, updateDate))
    changeAction = str(request.args.get('changeAction'))
    dataChanged = str(request.args.get('dataChanged'))
    sessionId = str(request.args.get('sessionId'))
    userId = str(request.args.get('userId'))
    if 'returnCode>0<' in result:
        logAction(sessionId, facNum, clubCode, userId, Group.SoS, Screens.FacilityServices, Sections.Main, dataChanged,
                  changeAction)
    return result


@app.route('/updateProgramsData')
def updateProgramsData():
    facNum = str(request.args.get('facNum'))
    clubCode = str(request.args.get('clubCode'))
    programId = str(request.args.get('programId'))
    programTypeId = str(request.args.get('programTypeId'))
    effDate = str(request.args.get('effDate'))
    expDate = str(request.args.get('expDate'))
    comments = str(request.args.get('comments'))
    active = str(request.args.get('active'))
    insertBy = str(request.args.get('insertBy'))
    insertDate = str(request.args.get('insertDate'))
    updateBy = str(request.args.get('updateBy'))
    updateDate = str(request.args.get('updateDate'))
    result = str(inspectionApis.updateProgramsData(facNum, clubCode, programId, programTypeId, effDate, expDate, comments,
                                                 active, insertBy, insertDate, updateBy, updateDate))
    changeAction = str(request.args.get('changeAction'))
    dataChanged = str(request.args.get('dataChanged'))
    sessionId = str(request.args.get('sessionId'))
    userId = str(request.args.get('userId'))
    if 'returnCode>0<' in result:
        logAction(sessionId, facNum, clubCode, userId, Group.SoS, Screens.Programs, Sections.Main, dataChanged,
                  changeAction)
    return result


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
    result = str(inspectionApis.updateSurveySoftwaresData(facNum, clubCode, softwareSurveyNum, repairSoftwareId,
                                                        repairSoftwareVersion, repairSoftwarePurchaseY,
                                                        repairSoftwarePurchaseAmt, repairSoftwareMonthlyFee,
                                                        repairSoftwareOnetimeFee, shopMgmtSoftwareName,
                                                        shopMgmtSoftwareVersion, shopMgmtSoftwarePurcharY,
                                                        shopMgmtSoftwarePurcharAmt, shopMgmtSoftwareMonthlyFee,
                                                        shopMgmtSoftwareOnetimeFee, surveyCompleteDate, insertBy,
                                                        insertDate, updateBy, updateDate))
    changeAction = str(request.args.get('changeAction'))
    dataChanged = str(request.args.get('dataChanged'))
    sessionId = str(request.args.get('sessionId'))
    userId = str(request.args.get('userId'))
    if 'returnCode>0<' in result:
        logAction(sessionId, facNum, clubCode, userId, Group.Surveys, Screens.General, Sections.Main, dataChanged,
                  changeAction)
    return result


@app.route('/updateVisitationDetailsData')
def updateVisitationDetailsData():
    facNum = str(request.args.get('facnum'))
    clubCode = str(request.args.get('clubcode'))
    staffTraining = str(request.args.get('StaffTraining'))
    qualityControl = str(request.args.get('QualityControl'))
    aarSigns = str(request.args.get('AARSigns'))
    certificateOfApproval = str(request.args.get('CertificateOfApproval'))
    memberBenefitPoster = str(request.args.get('MemberBenefitPoster'))
    insertBy = str(request.args.get('insertBy'))
    insertDate = str(request.args.get('insertDate'))
    updateBy = str(request.args.get('updateBy'))
    updateDate = str(request.args.get('updateDate'))
    result = str(inspectionApis.updateVisitationDetailsData(facNum, clubCode, staffTraining, qualityControl, aarSigns,
                                                       certificateOfApproval, memberBenefitPoster, insertBy,
                                                          insertDate, updateBy, updateDate))
    sessionId = str(request.args.get('sessionId'))
    userId = str(request.args.get('userId'))
    visitationType = str(request.args.get('visitationType'))
    visitationReason = str(request.args.get('visitationReason'))
    emailPDF = str(request.args.get('emailPDF'))
    emailTo = str(request.args.get('emailTo'))
    waiveVisitation = str(request.args.get('waiveVisitation'))
    waiveComments = str(request.args.get('waiveComments'))
    facilityRep = str(request.args.get('facilityRep'))
    automotiveSpecialist = str(request.args.get('automotiveSpecialist'))
    visitationId = str(request.args.get('visitationId'))
    if 'returnCode>0<' in result:
        logVisitationHeader(sessionId, facNum, clubCode, userId, visitationType, visitationReason, emailPDF,
                  emailTo,waiveVisitation,waiveComments,facilityRep,automotiveSpecialist,visitationId)

    return result


@app.route('/updateVisitationDetailsDataProgress')
def updateVisitationDetailsDataProgress():
    facNum = str(request.args.get('facnum'))
    clubCode = str(request.args.get('clubcode'))
    staffTraining = str(request.args.get('StaffTraining'))
    qualityControl = str(request.args.get('QualityControl'))
    aarSigns = str(request.args.get('AARSigns'))
    certificateOfApproval = str(request.args.get('CertificateOfApproval'))
    memberBenefitPoster = str(request.args.get('MemberBenefitPoster'))
    sessionId = str(request.args.get('sessionId'))
    userId = str(request.args.get('userId'))
    visitationType = str(request.args.get('visitationType'))
    visitationReason = str(request.args.get('visitationReason'))
    emailPDF = str(request.args.get('emailPDF'))
    emailTo = str(request.args.get('emailTo'))
    waiveVisitation = str(request.args.get('waiveVisitation'))
    waiveComments = str(request.args.get('waiveComments'))
    facilityRep = str(request.args.get('facilityRep'))
    automotiveSpecialist = str(request.args.get('automotiveSpecialist'))
    visitationId = '0'
    return logVisitationHeaderProgress(sessionId, facNum, clubCode, userId, visitationType, visitationReason, emailPDF,
              emailTo,waiveVisitation,waiveComments,facilityRep,automotiveSpecialist,visitationId,staffTraining,qualityControl,aarSigns,certificateOfApproval,memberBenefitPoster)



@app.route('/updateFacilityVehicles')
def updateFacilityVehicles():
    facnum = str(request.args.get('facnum'))
    clubcode = str(request.args.get('clubcode'))
    vehicleId = str(request.args.get('vehicleId'))
    insertBy = str(request.args.get('insertBy'))
    insertDate = str(request.args.get('insertDate'))
    result = str(inspectionApis.updateFacilityVehicles(facnum, clubcode, vehicleId, insertBy, insertDate))
    changeAction = str(request.args.get('changeAction'))
    dataChanged = str(request.args.get('dataChanged'))
    sessionId = str(request.args.get('sessionId'))
    userId = str(request.args.get('userId'))
    if 'returnCode>0<' in result:
        logAction(sessionId, facnum, clubcode, userId, Group.SoS, Screens.Vehicles, Sections.Main, dataChanged,
                  changeAction)
    return result


@app.route('/updatePersonnelCertification')
def updatePersonnelCertification():
    facnum = str(request.args.get('facNum'))
    clubcode = str(request.args.get('clubCode'))
    personnelId = str(request.args.get('personnelId'))
    certId = str(request.args.get('certId'))
    certificationTypeId = str(request.args.get('certificationTypeId,'))
    certificationDate = str(request.args.get('certificationDate'))
    expirationDate = str(request.args.get('expirationDate'))
    certDesc = str(request.args.get('certDesc'))
    insertBy = str(request.args.get('insertBy'))
    insertDate = str(request.args.get('insertDate'))
    updateBy = str(request.args.get('updateBy,'))
    updateDate = str(request.args.get('updateDate'))
    active = str(request.args.get('active'))
    result = str(inspectionApis.updatePersonnelCertification(facnum, clubcode, personnelId, certId, certificationTypeId,
                                                           certificationDate, expirationDate, certDesc, insertBy,
                                                           insertDate, updateBy, updateDate, active))
    changeAction = str(request.args.get('changeAction'))
    dataChanged = str(request.args.get('dataChanged'))
    sessionId = str(request.args.get('sessionId'))
    userId = str(request.args.get('userId'))
    if 'returnCode>0<' in result:
        logAction(sessionId, facnum, clubcode, userId, Group.Facility, Screens.Personnel, Sections.Certifications, dataChanged,
                  changeAction)
    return result


@app.route('/updateFacilityPersonnelSignerData')
def updateFacilityPersonnelSignerData():
    facnum = str(request.args.get('facNum'))
    clubcode = str(request.args.get('clubCode'))
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
    result = str(
        inspectionApis.updateFacilityPersonnelSignerData(facnum, clubcode, personnelId, addr1, addr2, city, st, zip,
                                                         zip4, phone, email, contractStartDate, contractEndDate,
                                                         insertBy, insertDate, updateBy, updateDate, active))
    # changeAction = str(request.args.get('changeAction'))
    # dataChanged = str(request.args.get('dataChanged'))
    # sessionId = str(request.args.get('sessionId'))
    # userId = str(request.args.get('userId'))
    # if 'returnCode>0<' in result:
    #     logAction(sessionId, facnum, clubcode, userId, Group.Facility, Screens.Personnel, Sections.Signer, dataChanged,
    #               changeAction)
    return result


@app.route('/updateVehicleServices')
def updateVehicleServices():
    facnum = str(request.args.get('facnum'))
    clubcode = str(request.args.get('clubcode'))
    vehiclesTypeId = str(request.args.get('vehiclesTypeId'))
    scopeServiceId = str(request.args.get('scopeServiceId'))
    insertBy = str(request.args.get('insertBy'))
    result = str(inspectionApis.updateVehicleServices(facnum, clubcode, vehiclesTypeId, scopeServiceId, insertBy))
    changeAction = str(request.args.get('changeAction'))
    dataChanged = str(request.args.get('dataChanged'))
    sessionId = str(request.args.get('sessionId'))
    userId = str(request.args.get('userId'))
    if 'returnCode>0<' in result:
        logAction(sessionId, facnum, clubcode, userId, Group.SoS, Screens.VehicleServices, Sections.Main, dataChanged,
                  changeAction)
    return result


@app.route('/updateAARPortalTracking')
def updateAARPortalTracking():
    facnum = str(request.args.get('facNum'))
    clubcode = str(request.args.get('clubCode'))
    facId = str(request.args.get('facId'))
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
    result = str(
        inspectionApis.updateAARPortalTracking(facnum, clubcode, facId, trackingId, portalInspectionDate,
                                               loggedIntoPortal,
                                               numberUnacknowledgedTows, inProgressTows, inProgressWalkIns, insertBy,
                                               insertDate, updateBy, updateDate, active))
    changeAction = str(request.args.get('changeAction'))
    dataChanged = str(request.args.get('dataChanged'))
    sessionId = str(request.args.get('sessionId'))
    userId = str(request.args.get('userId'))
    if 'returnCode>0<' in result:
        logAction(sessionId, facnum, clubcode, userId, Group.Facility, Screens.RSP, Sections.Tracking, dataChanged,
                  changeAction)
    return result


@app.route('/updateVehicles')
def updateVehicles():
    facnum = str(request.args.get('facnum'))
    clubcode = str(request.args.get('clubcode'))
    vehicleid = str(request.args.get('VehicleID'))
    insertDate = str(request.args.get('insertDate'))
    insertBy = str(request.args.get('insertBy'))
    result = str(inspectionApis.updateVehicles(facnum, clubcode, vehicleid, insertDate, insertBy))
    changeAction = str(request.args.get('changeAction'))
    dataChanged = str(request.args.get('dataChanged'))
    sessionId = str(request.args.get('sessionId'))
    userId = str(request.args.get('userId'))
    if 'returnCode>0<' in result:
        logAction(sessionId, facnum, clubcode, userId, Group.SoS, Screens.Vehicles, Sections.Main, dataChanged,
                  changeAction)
    return result


@app.route('/authenticate')
def authenticate():
    email = str(request.args.get('email'))
    password = str(request.args.get('password'))
    logAction('NO ID', '0', '0', '', Group.Login, Screens.LoginTrial, Sections.LoginSucceeded, 'Login Trial with email : ' + email,
              '0')
    return DbConnection.queryCsiDB(
        "exec v2reports.dbo.InspectionLogin @email='" + email + "', @password = '" + password + "';")


@app.route('/resetPassword')
def resetPassword():
    email = str(request.args.get('email'))
    # sessionId = str(request.args.get('sessionId'))
    # dataChanged = str(request.args.get('dataChanged'))
    result = DbConnection.getCountFromCsiDB(
        "select count(*) from v2reports.dbo.V2Login where lower(email) = '" + email + "'")
    if result > 0:
        randomPassword = getRandomPass()
        sendMailTo(email,randomPassword)
        updateStatement = "update v2reports.dbo.v2login set temppassword = '" + randomPassword + "' where Email = '" + email + "'"
        DbConnection.updateCsiDB(updateStatement)
        # logAction(sessionId, '0', '0', '', Group.Login, Screens.ResetPassword, Sections.LoginSucceeded, dataChanged,
        #           '0')
        return 'Success'
    else:
        # logAction(sessionId, '0', '0', "", Group.Login, Screens.ResetPassword, Sections.ResetFailed, dataChanged,
        #           '0')
        return "invalid email/username"


@app.route('/changePassword')
def changePassword():
    email = str(request.args.get('email'))
    password = str(request.args.get('password'))
    updateStatement = "update v2reports.dbo.v2login set temppassword = '', password = '" + password + "' where lower(Email) = loweR('" + email + "')"
    DbConnection.updateCsiDB(updateStatement)
    return "Success"


@app.route('/<path:path>')
def catch_all(path):
    return '[]'


if __name__ == '__main__':
    app.run()


# Web Services to be used for standalone App

def getSchemaOf(clientid):
    if clientid == '2':
        return "AAAClient"



@app.route('/testWS')
def testWS():
    return "Done ....."


@app.route('/authenticatePRG')
def authenticatePRG():
    email = str(request.args.get('email'))
    password = str(request.args.get('password'))
    result = DbConnection.getCountFromDB("select count(1) from AAAMaster.tblPRGUsers where lower(email) = '" + email + "' and temppassword = '"+password+"'")
    if result > 0:
        return "0"
    else:
        result = DbConnection.getCountFromDB(
            "SELECT COUNT(1) FROM AAAMaster.tblPRGUsers WHERE lower(email) = lower('" + email + "') and password= '" + password + "'")
        if result > 0:
            return DbConnection.queryDb(
            "SELECT b.clientId FROM AAAMaster.tblPRGUsers a, AAAMaster.tblPRGClients b where a.clientId = b.clientId and lower(email) = lower('" + email + "') and password= '" + password + "'")
        else:
            return "-1"


@app.route('/getPRGTypeTables')
def getPRGTypeTables():
    clientId= request.args.get('clientId')
    schemaName = getSchemaOf(clientId)
    result = DbConnection.queryDbTypeTables(schemaName,clientId)
    return result


@app.route('/getPRGVisitations')
def getPRGVisitations():
    facNum = str(request.args.get('facNum'))
    clubCode = str(request.args.get('clubCode'))
    specialist = str(request.args.get('specialist'))
    facilityName = str(request.args.get('facilityName'))
    inspectionMonth = str(request.args.get('inspectionMonth'))
    inspectionYear = str(request.args.get('inspectionYear'))
    visitationType = str(request.args.get('visitationType'))
    clientId = str(request.args.get('clientId'))
    visitationStatus = str(request.args.get('visitationStatus'))
    whereCon = "1=1"
    if facNum is not "":
        whereCon += " and facNo = " + facNum
    if clubCode is not "":
        whereCon += " and clubCode = '" + clubCode + "'"
    if specialist is not "":
        whereCon += " and userTrackingID = '" + specialist + "'"
    if facilityName is not "":
        whereCon += " and BusinessName = '" + facilityName + "'"
    if inspectionYear is not "":
        whereCon += " and year(DatePerformed) = " + inspectionYear
    if inspectionMonth is not "":
        whereCon += " and FacilityAnnualInspectionMonth = " + inspectionMonth
    if "0" in  visitationType: # 1: Annual 2: Quarterly 3: AdHoc 4:Defeciency
        whereCon = whereCon
    else:
        whereCon += " and visitationTypeName in ("
        if "1" in  visitationType:
            whereCon += "'Annual',"
        if "2" in  visitationType:
            whereCon += "'Quarterly',"
        if "3" in  visitationType:
            whereCon += "'AdHoc',"
        if "4" in  visitationType:
            whereCon += "'Deficiency',"
        whereCon = whereCon[:-1] + ")"
    if "0" in  visitationStatus: # 1: Annual 2: Quarterly 3: AdHoc 4:Defeciency
        whereCon = whereCon
    else:
        whereCon += " and visitationStatusName in ("
        if "1" in  visitationStatus:
            whereCon += "'Not Started',"
        if "2" in  visitationStatus:
            whereCon += "'In Progress',"
        if "3" in  visitationStatus:
            whereCon += "'Overdue',"
        if "4" in  visitationStatus:
            whereCon += "'Overdue / In Progress',"
        if "5" in  visitationStatus:
            whereCon += "'Completed',"
        whereCon = whereCon[:-1] + ")"
    return DbConnection.queryDb("Select * from "+getSchemaOf(clientId)+".getVisitations where " + whereCon)


@app.route('/resetPasswordPRG')
def resetPasswordPRG():
    email = str(request.args.get('email'))
    result = DbConnection.getCountFromDB(
        "select count(1) from AAAMaster.tblPRGUsers where lower(email) = '" + email + "'")
    if result > 0:
        randomPassword = getRandomPass()
        sendMailTo(email,randomPassword)
        updateStatement = "update AAAMaster.tblPRGUsers set temppassword = '" + randomPassword + "' where Email = '" + email + "'"
        DbConnection.updateDB(updateStatement)
        return 'Success'
    else:
        return "invalid email/username"


@app.route('/changePasswordPRG')
def changePasswordPRG():
    email = str(request.args.get('email'))
    password = str(request.args.get('password'))
    updateStatement = "update AAAMaster.tblPRGUsers set temppassword = '', password = '" + password + "' where lower(Email) = loweR('" + email + "')"
    DbConnection.updateDB(updateStatement)
    return "Success"