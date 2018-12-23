import requests
import os.path


class InspectionAPIs:
    url = 'https://uat.b2b.autoclubextranet.com/prg/ProcessRequest'

    def __init__(self):
        headers = {'content-type': 'text/xml'}
        my_path = os.path.abspath(os.path.dirname(__file__))
        cert = (os.path.join(my_path, "certs/cert.crt"), os.path.join(my_path, "certs/nopassword.key"))
        self.requestDictionary = {'headers': headers, 'cert': cert}
        pass

    def sendRequest(self, body):
        return requests.post(self.url, data=body, headers=self.requestDictionary["headers"],
                             cert=self.requestDictionary["cert"], verify=False).text

    def getTableTypes(self):
        body = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soapenv:Envelope " \
               "xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\"><soapenv:Header /><soapenv:Body> " \
               "<request><requestName>GetTypeTables</requestName><requestXml></requestXml></request> " \
               "</soapenv:Body></soapenv:Envelope>"
        return self.sendRequest(body)

    def updatePaymentMethodsData(self, facnum, clubCode, paymentMethodID, insertBy, insertDate):
        body = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soapenv:Envelope " \
               "xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\"> " \
               "<soapenv:Header/><soapenv:Body><request><requestName>UpdatePaymentMethodsData</requestName" \
               "><requestXml><facnum>" + facnum + "</facnum><clubcode>" + clubCode + "</clubcode><PmtMethodID>" + \
               paymentMethodID + "</PmtMethodID><insertBy>" + insertBy + "</insertBy><insertDate>" + insertDate + \
               "</insertDate></requestXml></request></soapenv:Body></soapenv:Envelope> "

        return self.sendRequest(body)

    def getVisitations(self, clubCode, facNum, specialist, dba, inspectionMonth, inspectionYear, annualVisitations,
                       quarterlyVisitations, pendingVisitations, completedVisitations, deficiencies):
        body = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soapenv:Envelope " \
               "xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\"><soapenv:Header " \
               "/><soapenv:Body><request><requestName>GetVisitations</requestName><requestXml><clubcode>" + clubCode \
               + "</clubcode><facnum>" + facNum + "</facnum><Specialist>" + specialist + "</Specialist><DBA>" + dba + \
               "</DBA><InspectionMonth>" + inspectionMonth + "</InspectionMonth><InspectionYear>" + inspectionYear + \
               "</InspectionYear><AnnualVisitations>" + annualVisitations + \
               "</AnnualVisitations><QuarterlyVisitations>" + quarterlyVisitations + \
               "</QuarterlyVisitations><PendingVisitations>" + pendingVisitations + \
               "</PendingVisitations><CompletedVisitations>" + completedVisitations + \
               "</CompletedVisitations><Deficiencies>" + deficiencies + \
               "</Deficiencies></requestXml></request></soapenv:Body></soapenv:Envelope> "

        if facNum == "":
            body = body.replace("<facnum></facnum>", "")

        if dba == "":
            body = body.replace("<DBA></DBA>", "")

        if specialist == "":
            body = body.replace("<Specialist></Specialist>", "")

        return self.sendRequest(body)

    def updateFacilityData(self, facNum, clubCode, businessName, busTypeId, entityName, assignToId, officeId
                           , taxIdNumber, facilityRepairOrderCount, facilityAnnualInspectionMonth, inspectionCycle,
                           timeZoneId, svcAvailability
                           , facilityTypeId, automotiveRepairNumber, automotiveRepairExpDate, contractCurrentDate,
                           contractInitialDate, billingMonth, billingAmount
                           , internetAccess, webSite, terminationDate, terminationId, terminationComments, insertBy,
                           insertDate, updateBy, updateDate
                           , active, achParticipant, insuranceExpDate, contractTypeId):
        body = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soapenv:Envelope " \
               "xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\"><soapenv:Header/><soapenv:Body><request" \
               "><requestName>UpdateFacilityData</requestName><requestXml><facnum>" + facNum + "</facnum><clubcode>" \
               + clubCode + "</clubcode><BusinessName>" + businessName + "</BusinessName><BusTypeID>" + busTypeId + \
               "</BusTypeID><EntityName>" + entityName + "</EntityName><assignedToID>" + assignToId + \
               "</assignedToID><officeID>" + officeId + "</officeID><TaxIDNumber>" + taxIdNumber + \
               "</TaxIDNumber><FacilityRepairOrderCount>" + facilityRepairOrderCount + \
               "</FacilityRepairOrderCount><FacilityAnnualInspectionMonth>" + facilityAnnualInspectionMonth + \
               "</FacilityAnnualInspectionMonth><InspectionCycle>" + inspectionCycle + \
               "</InspectionCycle><TimezoneID>" + timeZoneId + "</TimezoneID><SvcAvailability>" + svcAvailability + \
               "</SvcAvailability><FacilityTypeID>" + facilityTypeId + "</FacilityTypeID><AutomotiveRepairNumber>" + \
               automotiveRepairNumber + "</AutomotiveRepairNumber><AutomotiveRepairExpDate>" + \
               automotiveRepairExpDate + "</AutomotiveRepairExpDate><ContractCurrentDate>" + contractCurrentDate + \
               "</ContractCurrentDate><ContractInitialDate>" + contractInitialDate + \
               "</ContractInitialDate><BillingMonth>" + billingMonth + "</BillingMonth><BillingAmount>" + \
               billingAmount + "</BillingAmount><InternetAccess>" + internetAccess + "</InternetAccess><WebSite>" + \
               webSite + "</WebSite><TerminationDate>" + terminationDate + "</TerminationDate><TerminationID>" + \
               terminationId + "</TerminationID><TerminationComments>" + terminationComments + \
               "</TerminationComments><insertBy>" + insertBy + "</insertBy><insertDate>" + insertDate + \
               "</insertDate><updateBy>" + updateBy + "</updateBy><updateDate>" + updateDate + \
               "</updateDate><active>" + active + "</active><ACHParticipant>" + achParticipant + \
               "</ACHParticipant><InsuranceExpDate>" + insuranceExpDate + "</InsuranceExpDate><ContractTypeID>" + \
               contractTypeId + "</ContractTypeID></requestXml></request></soapenv:Body></soapenv:Envelope> "
        return self.sendRequest(body)

    def updateFacilityAddressData(self, facnum, clubcode, locationTypeID, FAC_Addr1, FAC_Addr2, CITY, ST, ZIP,
                                  Country, BranchName, BranchNumber, LATITUDE, LONGITUDE, insertBy, insertDate,
                                  updateBy, updateDate, active):
        body = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soapenv:Envelope " \
               "xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\"><soapenv:Header/><soapenv:Body><request" \
               "><requestName>UpdateFacilityAddressData</requestName><requestXml><facnum>" + facnum + \
               "</facnum><clubcode>" + clubcode + "</clubcode><LocationTypeID>" + locationTypeID + \
               "</LocationTypeID><FAC_Addr1>" + FAC_Addr1 + "</FAC_Addr1><FAC_Addr2>" + FAC_Addr2 + \
               "</FAC_Addr2><CITY>" + CITY + "</CITY><ST>" + ST + "</ST><ZIP>" + ZIP + "</ZIP><ZIP4/><County>" + \
               Country + "</County><BranchName>" + BranchName + "</BranchName><BranchNumber>" + BranchNumber + \
               "</BranchNumber><LATITUDE>" + LATITUDE + "</LATITUDE><LONGITUDE>" + LONGITUDE + \
               "</LONGITUDE><insertBy>" + insertBy + "</insertBy><insertDate>" + insertDate + \
               "</insertDate><updateBy>" + updateBy + "</updateBy><updateDate>" + updateDate + \
               "</updateDate><active>" + active + "</active></requestXml></request></soapenv:Body></soapenv:Envelope> "
        return self.sendRequest(body)

    def updateFacilityEmailData(self, facNum, clubCode, emailId, emailTypeId, email, insertBy, insertDate,
                                updateBy, updateDate):
        body = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soapenv:Envelope " \
               "xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\"><soapenv:Header/><soapenv:Body><request" \
               "><requestName>UpdateFacilityEmailData</requestName><requestXml><facnum>" + facNum + \
               "</facnum><clubcode>" + clubCode + "</clubcode><emailID>" + emailId + "</emailID><emailTypeId>" + \
               emailTypeId + "</emailTypeId><email>" + email + "</email><insertBy>" + insertBy + \
               "</insertBy><insertDate>" + insertDate + "</insertDate><updateBy>" + updateBy + \
               "</updateBy><updateDate>" + updateDate + \
               "</updateDate></requestXml></request></soapenv:Body></soapenv:Envelope> "
        return self.sendRequest(body)

    def updateFacilityPhoneData(self, facNum, clubCode, phoneId, phoneTypeId, phoneNumber, extension, description,
                                insertBy, insertDate, updateBy, updateDate, active):
        body = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soapenv:Envelope " \
               "xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\"><soapenv:Header/><soapenv:Body><request" \
               "><requestName>UpdateFacilityPhoneData</requestName><requestXml><facnum>" + facNum + \
               "</facnum><clubcode>" + clubCode + "</clubcode><PhoneID>" + phoneId + "</PhoneID><PhoneTypeID>" + \
               phoneTypeId + "</PhoneTypeID><PhoneNumber>" + phoneNumber + "</PhoneNumber><extension>" + extension + \
               "</extension><description>" + description + "</description><insertBy>" + insertBy + \
               "</insertBy><insertDate>" + insertDate + "</insertDate><updateBy>" + updateBy + \
               "</updateBy><updateDate>" + updateDate + "</updateDate><active>" + active + \
               "</active></requestXml></request></soapenv:Body></soapenv:Envelope> "
        return self.sendRequest(body)

    def updateFacilityPersonnelData(self, facNum, clubCode, personnelId, personnelTypeId, firstName, lastName,
                                    seniorityDate, certificationNum, startDate, contractSigner
                                    , insertBy, insertDate, updateBy, updateDate, active, primaryMailRecipient,
                                    rsp_userName, rsp_email, rsp_phone):
        body = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soapenv:Envelope " \
               "xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\"><soapenv:Header/><soapenv:Body><request" \
               "><requestName>UpdateFacilityPhoneData</requestName><requestXml><facnum>" + facNum + \
               "</facnum><clubcode>" + clubCode + "</clubcode><PersonnelID>" + personnelId + \
               "</PersonnelID><PersonnelTypeID>" + personnelTypeId + "</PersonnelTypeID><FirstName>" + firstName + \
               "</FirstName><LastName>" + lastName + "</LastName><SeniorityDate>" + seniorityDate + \
               "</SeniorityDate><CertificationNum>" + certificationNum + "</CertificationNum><startDate>" + startDate \
               + "</startDate><ContractSigner>" + contractSigner + "</ContractSigner><insertBy>" + insertBy + \
               "</insertBy><insertDate>" + insertDate + "</insertDate><updateBy>" + updateBy + \
               "</updateBy><updateDate>" + updateDate + "</updateDate><active>" + active + \
               "</active><PrimaryMailRecipient>" + primaryMailRecipient + "</PrimaryMailRecipient><RSP_UserName>" + \
               rsp_userName + "</RSP_UserName><RSP_Email>" + rsp_email + "</RSP_Email><RSP_Phone>" + rsp_phone + \
               "</RSP_Phone></requestXml></request></soapenv:Body></soapenv:Envelope> "
        return self.sendRequest(body)

    def updateScopeOfServiceData(self, facNum, clubCode, laborRateId, fixedLaborRate, laborMin, laborMax,
                                 diagnosticRate, numOfBays, numOfLifts
                                 , warrantyTypeId, active, insertBy, insertDate, updateBy, updateDate):
        body = "<?xml version=\"1.0\" encoding=\"utf-8\"?> <soapenv:Envelope " \
               "xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\"><soapenv:Header/><soapenv:Body><request" \
               "><requestName>UpdateScopeofServiceData</requestName><requestXml><facnum>" + facNum + \
               "</facnum><clubcode>" + clubCode + "</clubcode><LaborRateID>" + laborRateId + \
               "</LaborRateID><FixedLaborRate>" + fixedLaborRate + "</FixedLaborRate><LaborMin>" + laborMin + \
               "</LaborMin><LaborMax>" + laborMax + "</LaborMax><DiagnosticsRate>" + diagnosticRate + \
               "</DiagnosticsRate><NumOfBays>" + numOfBays + "</NumOfBays><NumOfLifts>" + numOfLifts + \
               "</NumOfLifts><WarrantyTypeID>" + warrantyTypeId + "</WarrantyTypeID><active>" + active + \
               "</active><insertBy>" + insertBy + "</insertBy><insertDate>" + insertDate + "</insertDate><updateBy>" \
               + updateBy + "</updateBy><updateDate>" + updateDate + \
               "</updateDate></requestXml></request></soapenv:Body></soapenv:Envelope> "
        return self.sendRequest(body)

    def updateVisitationTrackingData(self, facNum, clubCode, visitationId, performedBy, datePerformed,
                                     dateReceived, insertBy, insertDate, updateBy, updateDate):
        body = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soapenv:Envelope " \
               "xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\"><soapenv:Header/><soapenv:Body><request" \
               "><requestName>UpdateVisitationTrackingData</requestName><requestXml><facnum>" + facNum + \
               "</facnum><clubcode>" + clubCode + "</clubcode><visitationID>" + visitationId + \
               "</visitationID><performedBy>" + performedBy + "</performedBy><DatePerformed>" + datePerformed + \
               "</DatePerformed><DateReceived>" + dateReceived + "</DateReceived><insertBy>" + insertBy + \
               "</insertBy><insertDate>" + insertDate + "</insertDate><updateBy>" + updateBy + \
               "</updateBy><updateDate>" + updateDate + \
               "</updateDate></requestXml></request></soapenv:Body></soapenv:Envelope> "
        return self.sendRequest(body)

    def updateAARPortalAdminData(self, facNum, clubCode, facId, startDate, endDate, addendumSigned, cardReaders,
                                 insertBy, insertDate, updateBy, updateDate, active):
        body = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soapenv:Envelope " \
               "xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\"><soapenv:Header/><soapenv:Body><request" \
               "><requestName>UpdateAARPortalAdminData</requestName><requestXml><facnum>" + facNum + \
               "</facnum><clubcode>" + clubCode + "</clubcode><FACID>" + facId + "</FACID><startDate>" + startDate + "</startDate><endDate>" + \
               endDate + "</endDate><AddendumSigned>" + addendumSigned + "</AddendumSigned><CardReaders>" + \
               cardReaders + "</CardReaders><insertBy>" + insertBy + "</insertBy><insertDate>" + insertDate + \
               "</insertDate><updateBy>" + updateBy + "</updateBy><updateDate>" + updateDate + \
               "</updateDate><active>" + active + "</active></requestXml></request></soapenv:Body></soapenv:Envelope>"
        return self.sendRequest(body)

    def updateAffiliationsData(self, facNum, clubCode, affiliationId, affiliationTypeId, affiliationTypeDetailsId,
                               effDate, expDate, comment, active, insertBy, insertDate, updateBy, updateDate):
        body = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soapenv:Envelope " \
               "xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\"><soapenv:Header " \
               "/><soapenv:Body><request><requestName>UpdateAffiliationsData</requestName><requestXml><facnum>" + \
               facNum + "</facnum><clubcode>" + clubCode + "</clubcode><AffiliationID>" + affiliationId + \
               "</AffiliationID><AffiliationTypeID>" + affiliationTypeId + \
               "</AffiliationTypeID><AffiliationTypeDetailID>" + affiliationTypeDetailsId + \
               "</AffiliationTypeDetailID><effDate>" + effDate + "</effDate><expDate>" + expDate + \
               "</expDate><comment>" + comment + "</comment><active>" + active + "</active><insertBy>" + insertBy + \
               "</insertBy><insertDate>" + insertDate + "</insertDate><updateBy>" + updateBy + \
               "</updateBy><updateDate>" + updateDate + \
               "</updateDate></requestXml></request></soapenv:Body></soapenv:Envelope>"
        return self.sendRequest(body)

    def updateAmendmentOrderTrackingData(self, facNum, clubCode, facId, aoId, employeeId, reasonId, insertBy,
                                         insertDate, updateBy, updateDate, active):
        body = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soapenv:Envelope " \
               "xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\"><soapenv:Header " \
               "/><soapenv:Body><request><requestName>UpdateAmendmentOrderTrackingData</requestName><requestXml" \
               "><facnum>" + facNum + "</facnum><clubcode>" + clubCode + "</clubcode><FACID>" + facId + "</FACID><AOID>" + aoId \
               + "</AOID><EmployeeID>" + employeeId + "</EmployeeID><ReasonID>" + reasonId + "</ReasonID><insertBy>" + insertBy \
               + "</insertBy><insertDate>" + insertDate + "</insertDate><updateBy>" + updateBy + "</updateBy><updateDate" \
                                                                                                 ">" + updateDate + "</updateDate><active>" + active + "</active></requestXml></request></soapenv:Body></soapenv:Envelope> "
        return self.sendRequest(body)

    def updateDeficiencyData(self, facNum, clubCode, defId, defTypeId, visitationDate, enteredDate, clearedDate,
                             comments, insertBy, insertDate, updateBy, updateDate):
        body = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soapenv:Envelope " \
               "xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\"><soapenv:Header " \
               "/><soapenv:Body><request><requestName>UpdateDeficiencyData</requestName><requestXml><facnum>" + \
               facNum + "</facnum><clubcode>" + clubCode + "</clubcode><DefID>" + defId + "</DefID><DefTypeID>" + \
               defTypeId + "</DefTypeID><VisitationDate>" + visitationDate + "</VisitationDate><EnteredDate>" + \
               enteredDate + "</EnteredDate><ClearedDate>" + clearedDate + "</ClearedDate><Comments>" + comments + \
               "</Comments><insertBy>" + insertBy + "</insertBy><insertDate>" + insertDate + \
               "</insertDate><updateBy>" + updateBy + "</updateBy><updateDate>" + updateDate + \
               "</updateDate></requestXml></request></soapenv:Body></soapenv:Envelope> "
        return self.sendRequest(body)

    def updateComplaintFilesData(self, facnum, clubcode, RecordID, ComplaintID, FACID, initiatedBy, IsTowIn,
                                 IsOutofState, SOSSID, FirstName, LastName, ComplaintNotCounted, IsERSComplaint,
                                 AssignedTo, ComplaintReasonID, ComplaintResolutionID, ReceivedDate, OpenedDate,
                                 ClosedDate, SecondOpenedDate, SecondClosedDate, WorkDaysNotCounted, insertBy,
                                 insertDate, updateBy, updateDate):
        body = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soapenv:Envelope " \
               "xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\"><soapenv:Header " \
               "/><soapenv:Body><request><requestName>UpdateComplaintFilesData</requestName><requestXml><facnum>" + \
               facnum + "</facnum><clubcode>" + clubcode + "</clubcode><RecordID>" + RecordID + \
               "</RecordID><ComplaintID>" + ComplaintID + "</ComplaintID><FACID>" + FACID + "</FACID><initiatedBy>" + \
               initiatedBy + "</initiatedBy><IsTowIn>" + IsTowIn + "</IsTowIn><IsOutofState>" + IsOutofState + \
               "</IsOutofState><SOSSID>" + SOSSID + "</SOSSID><FirstName>" + FirstName + "</FirstName><LastName>" + \
               LastName + "</LastName><ComplaintNotCounted>" + ComplaintNotCounted + \
               "</ComplaintNotCounted><IsERSComplaint>" + IsERSComplaint + "</IsERSComplaint><AssignedTo>" + \
               AssignedTo + "</AssignedTo><ComplaintReasonID>" + ComplaintReasonID + \
               "</ComplaintReasonID><ComplaintResolutionID>" + ComplaintResolutionID + \
               "</ComplaintResolutionID><ReceivedDate>" + ReceivedDate + "</ReceivedDate><OpenedDate>" + OpenedDate + \
               "</OpenedDate><ClosedDate>" + ClosedDate + "</ClosedDate><SecondOpenedDate>" + SecondOpenedDate + \
               "</SecondOpenedDate><SecondClosedDate>" + SecondClosedDate + "</SecondClosedDate><WorkDaysNotCounted>" \
               + WorkDaysNotCounted + "</WorkDaysNotCounted><insertBy>" + insertBy + "</insertBy><insertDate>" + \
               insertDate + "</insertDate><updateBy>" + updateBy + "</updateBy><updateDate>" + updateDate + \
               "</updateDate></requestXml></request></soapenv:Body></soapenv:Envelope> "
        return self.sendRequest(body)

    def updateFacilityClosureData(self, facNum, clubCode, facilityClosureId, closureId, effDate, expDate,
                                  comments, active, insertBy, insertDate, updateBy, updateDate,
                                  prgFacilityClosureId):
        body = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soapenv:Envelope " \
               "xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\"><soapenv:Header " \
               "/><soapenv:Body><request><requestName>UpdateFacilityClosureData</requestName><requestXml><facnum>" + \
               facNum + "</facnum><clubcode>" + clubCode + "</clubcode><FacilityClosureID>" + facilityClosureId + \
               "</FacilityClosureID><ClosureID>" + closureId + "</ClosureID><effDate>" + effDate + \
               "</effDate><expDate>" + expDate + "</expDate><Comments>" + comments + "</Comments><active>" + active + \
               "</active><insertBy>" + insertBy + "</insertBy><insertDate>" + insertDate + "</insertDate><updateBy>" \
               + updateBy + "</updateBy><updateDate>" + updateDate + "</updateDate><PRGFacilityClosureID>" + \
               prgFacilityClosureId + "</PRGFacilityClosureID></requestXml></request></soapenv:Body></soapenv" \
                                      ":Envelope> "
        return self.sendRequest(body)

    def updateFacilityHoursData(self, facNum, clubCode, monOpen, monClose, tueOpen, tueClose, wedOpen, wedClose,
                                thuOpen, thuClose, friOpen, friClose, satOpen, satClose, sunOpen, sunClose,
                                nightDrop, nightDropInstr, insertBy, insertDate, updateBy, updateDate,
                                facAvailability, availEffDate, availExpDate):
        body = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soapenv:Envelope " \
               "xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\"><soapenv:Header " \
               "/><soapenv:Body><request><requestName>UpdateFacilityHoursData</requestName><requestXml><facnum>" + \
               facNum + "</facnum><clubcode>" + clubCode + "</clubcode><MonOpen>" + monOpen + "</MonOpen><MonClose>" \
               + monClose + "</MonClose><TueOpen>" + tueOpen + "</TueOpen><TueClose>" + tueClose + \
               "</TueClose><WedOpen>" + wedOpen + "</WedOpen><WedClose>" + wedClose + "</WedClose><ThuOpen>" + \
               thuOpen + "</ThuOpen><ThuClose>" + thuClose + "</ThuClose><FriOpen>" + friOpen + \
               "</FriOpen><FriClose>" + friClose + "</FriClose><SatOpen>" + satOpen + "</SatOpen><SatClose>" + \
               satClose + "</SatClose><SunOpen>" + sunOpen + "</SunOpen><SunClose>" + sunClose + \
               "</SunClose><NightDrop>" + nightDrop + "</NightDrop><NightDropInstr>" + nightDropInstr + \
               "</NightDropInstr><insertBy>" + insertBy + "</insertBy><insertDate>" + insertDate + \
               "</insertDate><updateBy>" + updateBy + "</updateBy><updateDate>" + updateDate + \
               "</updateDate><FacAvailability>" + facAvailability + "</FacAvailability><AvailEffDate>" + availEffDate \
               + "</AvailEffDate><AvailExpDate>" + availExpDate + \
               "</AvailExpDate></requestXml></request></soapenv:Body></soapenv:Envelope>"
        return self.sendRequest(body)

    def updateFacilityManagersData(self, facNum, clubCode, managerId, insertBy, insertDate):
        body = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soapenv:Envelope " \
               "xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\"><soapenv:Header " \
               "/><soapenv:Body><request><requestName>UpdateFacilityManagersData</requestName><requestXml><facnum>" + \
               facNum + "</facnum><clubcode>" + clubCode + "</clubcode><ManagerID>" + managerId + \
               "</ManagerID><InsertBy>" + insertBy + "</InsertBy><InsertDate>" + insertDate + \
               "</InsertDate></requestXml></request></soapenv:Body></soapenv:Envelope>"
        return self.sendRequest(body)

    def updateFacilityLanguageData(self, facNum, clubCode, langTypeId, insertBy, insertDate):
        body = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soapenv:Envelope " \
               "xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\"><soapenv:Header " \
               "/><soapenv:Body><request><requestName>UpdateFacilityLanguageData</requestName><requestXml><facnum>" + \
               facNum + "</facnum><clubcode>" + clubCode + "</clubcode><LangTypeID>" + langTypeId + \
               "</LangTypeID><insertBy>" + insertBy + "</insertBy><insertDate>" + insertDate + \
               "</insertDate></requestXml></request></soapenv:Body></soapenv:Envelope> "
        return self.sendRequest(body)

    def updateFacilityPhotosData(self, facNum, clubCode, photoId, fileName, fileDescription, primaryPhoto,
                                 approvalRequest, approved, seqNum, approvedBy, approvedDate, lastUpdateBy,
                                 lastUpdateDate):
        body = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soapenv:Envelope " \
               "xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\"><soapenv:Header " \
               "/><soapenv:Body><request><requestName>UpdateFacilityPhotosData</requestName><requestXml><facnum>" + \
               facNum + "</facnum><clubcode>" + clubCode + "</clubcode><PhotoId>" + photoId + "</PhotoId><FileName>" \
               + fileName + "</FileName><FileDescription>" + fileDescription + "</FileDescription><PrimaryPhoto>" + \
               primaryPhoto + "</PrimaryPhoto><ApprovalRequested>" + approvalRequest + \
               "</ApprovalRequested><Approved>" + approved + "</Approved><SeqNum>" + seqNum + "</SeqNum><ApprovedBy>" \
               + approvedBy + "</ApprovedBy><ApprovedDate>" + approvedDate + "</ApprovedDate><LastUpdateBy>" + \
               lastUpdateBy + "</LastUpdateBy><LastUpdateDate>" + lastUpdateDate + \
               "</LastUpdateDate></requestXml></request></soapenv:Body></soapenv:Envelope> "
        return self.sendRequest(body)

    def updateFacilityServiceProviderData(self, facNum, clubCode, srvProviderId, providerNum, active, insertBy,
                                          insertDate, updateBy, updateDate):
        body = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soapenv:Envelope " \
               "xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\"><soapenv:Header " \
               "/><soapenv:Body><request><requestName>UpdateFacilityServiceProviderData</requestName><requestXml" \
               "><facnum>" + facNum + "</facnum><clubcode>" + clubCode + "</clubcode><SrvProviderId>" + srvProviderId \
               + "</SrvProviderId><ProviderNum>" + providerNum + "</ProviderNum><active>" + active + \
               "</active><insertBy>" + insertBy + "</insertBy><insertDate>" + insertDate + "</insertDate><updateBy>" \
               + updateBy + "</updateBy><updatedate>" + updateDate + \
               "</updatedate></requestXml></request></soapenv:Body></soapenv:Envelope>"
        return self.sendRequest(body)

    def updateFacilityServicesData(self, facNum, clubCode, facilityServicesId, serviceId, effDate, expDate, comments,
                                   active, insertBy, insertDate, updateBy, updateDate):
        body = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soapenv:Envelope " \
               "xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\"><soapenv:Header " \
               "/><soapenv:Body><request><requestName>UpdateFacilityServicesData</requestName><requestXml><facnum>" + \
               facNum + "</facnum><clubcode>" + clubCode + "</clubcode><FacilityServicesID>" + facilityServicesId + \
               "</FacilityServicesID><ServiceID>" + serviceId + "</ServiceID><effDate>" + effDate + \
               "</effDate><expDate></expDate><Comments>" + comments + "</Comments><active>" + active + \
               "</active><insertBy>" + insertBy + "</insertBy><insertDate>" + insertDate + "</insertDate><updateBy>" \
               + updateBy + "</updateBy><updateDate>" + updateDate + \
               "</updateDate></requestXml></request></soapenv:Body></soapenv:Envelope> "
        return self.sendRequest(body)

    def updateProgramsData(self, facNum, clubCode, programId, programTypeId, effDate, expDate, comments, active,
                           insertBy, insertDate, updateBy, updateDate):
        body = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soapenv:Envelope " \
               "xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\"><soapenv:Header " \
               "/><soapenv:Body><request><requestName>UpdateProgramsData</requestName><requestXml><facnum>" + facNum \
               + "</facnum><clubcode>" + clubCode + "</clubcode><ProgramID>" + programId + \
               "</ProgramID><ProgramTypeID>" + programTypeId + "</ProgramTypeID><effDate>" + effDate + \
               "</effDate><expDate>" + expDate + "</expDate><Comments>" + comments + "</Comments><active>" + active + \
               "</active><insertBy>" + insertBy + "</insertBy><insertDate>" + insertDate + "</insertDate><updateBy>" \
               + updateBy + "</updateBy><updateDate>" + updateDate + \
               "</updateDate></requestXml></request></soapenv:Body></soapenv:Envelope> "
        return self.sendRequest(body)

    def updateSurveySoftwaresData(self, facNum, clubCode, softwareSurveyNum, repairSoftwareId, repairSoftwareVersion,
                                  repairSoftwarePurchaseY, repairSoftwarePurchaseAmt, repairSoftwareMonthlyFee,
                                  repairSoftwareOnetimeFee, shopMgmtSoftwareName, shopMgmtSoftwareVersion,
                                  shopMgmtSoftwarePurcharY, shopMgmtSoftwarePurcharAmt, shopMgmtSoftwareMonthlyFee,
                                  shopMgmtSoftwareOnetimeFee, surveyCompleteDate, insertBy, insertDate, updateBy,
                                  updateDate):
        body = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soapenv:Envelope " \
               "xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\"><soapenv:Header " \
               "/><soapenv:Body><request><requestName>UpdateSurveySoftwaresData</requestName><requestXml><facnum>" + \
               facNum + "</facnum><clubcode>" + clubCode + "</clubcode><SoftwareSurveyNum>" + softwareSurveyNum + \
               "</SoftwareSurveyNum><RepairSoftwareID>" + repairSoftwareId + \
               "</RepairSoftwareID><RepairSoftwareVersion>" + repairSoftwareVersion + \
               "</RepairSoftwareVersion><RepairSoftwarePurchaseYr>" + repairSoftwarePurchaseY + \
               "</RepairSoftwarePurchaseYr><RepairSoftwarePurchaseAmt>" + repairSoftwarePurchaseAmt + \
               "</RepairSoftwarePurchaseAmt><RepairSoftwareMonthlyFee>" + repairSoftwareMonthlyFee + \
               "</RepairSoftwareMonthlyFee><RepairSoftwareOnetimeFee>" + repairSoftwareOnetimeFee + \
               "</RepairSoftwareOnetimeFee><ShopMgmtSoftwareName>" + shopMgmtSoftwareName + \
               "</ShopMgmtSoftwareName><ShopMgmtSoftwareVersion>" + shopMgmtSoftwareVersion + \
               "</ShopMgmtSoftwareVersion><ShopMgmtSoftwarePurcharYr>" + shopMgmtSoftwarePurcharY + \
               "</ShopMgmtSoftwarePurcharYr><ShopMgmtSoftwarePurcharAmt>" + shopMgmtSoftwarePurcharAmt + \
               "</ShopMgmtSoftwarePurcharAmt><ShopMgmtSoftwareMonthlyFee>" + shopMgmtSoftwareMonthlyFee + \
               "</ShopMgmtSoftwareMonthlyFee><ShopMgmtSoftwareOnetimeFee>" + shopMgmtSoftwareOnetimeFee + \
               "</ShopMgmtSoftwareOnetimeFee><SurveyCompleteDate>" + surveyCompleteDate + \
               "</SurveyCompleteDate><insertBy>" + insertBy + "</insertBy><insertDate>" + insertDate + \
               "</insertDate><updateBy>" + updateBy + "</updateBy><updateDate>" + updateDate + \
               "</updateDate></requestXml></request></soapenv:Body></soapenv:Envelope> "
        return self.sendRequest(body)

    def updateVisitationDetailsData(self, facNum, clubCode, staffTraining, qualityControl, aarSigns,
                                    certificateOfApproval, memberBenefitPoster, insertBy, insertDate, updateBy,
                                    updateDate):
        body = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soapenv:Envelope " \
               "xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\"><soapenv:Header " \
               "/><soapenv:Body><request><requestName>UpdateVisitationDetailsData</requestName><requestXml><facnum>" \
               + facNum + "</facnum><clubcode>" + clubCode + "</clubcode><StaffTraining>" + staffTraining + \
               "</StaffTraining><QualityControl>" + qualityControl + "</QualityControl><AARSigns>" + aarSigns + \
               "</AARSigns><CertificateOfApproval>" + certificateOfApproval + \
               "</CertificateOfApproval><MemberBenefitPoster>" + memberBenefitPoster + \
               "</MemberBenefitPoster><insertBy>" + insertBy + "</insertBy><insertDate>" + insertDate + \
               "</insertDate><updateBy>" + updateBy + "</updateBy><updateDate>" + updateDate + \
               "</updateDate></requestXml></request></soapenv:Body></soapenv:Envelope> "
        return self.sendRequest(body)

    def updateFacilityVehicles(self, facnum, clubcode, vehicleId, insertBy, insertDate):
        body = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soapenv:Envelope " \
               "xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\"><soapenv:Header " \
               "/><soapenv:Body><request><requestName>UpdateFacVehicles</requestName><requestXml><facnum>" + facnum \
               + "</facnum><clubcode>" + clubcode + "</clubcode><VehicleID>" + vehicleId + "</VehicleID><insertBy>" + insertBy \
               + "</insertBy><insertDate>" + insertDate + "</insertDate></requestXml></request></soapenv:Body></soapenv" \
                                                          ":Envelope> "
        return self.sendRequest(body)

    def updatePersonnelCertification(self, facnum, clubcode, personnelId, certId, certificationTypeId,
                                     certificationDate, expirationDate, certDesc, insertBy, insertDate, updateBy,
                                     updateDate, active):
        body = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soapenv:Envelope " \
               "xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\"><soapenv:Header " \
               "/><soapenv:Body><request><requestName>UpdatePersonnelCertification</requestName><requestXml><facnum>" \
               + facnum + "</facnum><clubcode>" + clubcode + "</clubcode><PersonnelID>" + personnelId + \
               "</PersonnelID><CertID>" + certId + "</CertID><CertificationTypeId>" + certificationTypeId + \
               "</CertificationTypeId><CertificationDate>" + certificationDate + \
               "</CertificationDate><ExpirationDate>" + expirationDate + "</ExpirationDate><CertDesc>" + certDesc + \
               "</CertDesc><insertBy>" + insertBy + "</insertBy><insertDate>" + insertDate + \
               "</insertDate><updateBy>" + updateBy + "</updateBy><updateDate>" + updateDate + \
               "</updateDate><active>" + active + "</active></requestXml></request></soapenv:Body></soapenv:Envelope> "
        return self.sendRequest(body)

    def updateFacilityPersonnelSignerData(self, facnum, clubcode, personnelId, addr1, addr2, city, st, zip, zip4, phone,
                                          email, contractStartDate, contractEndDate, insertBy, insertDate, updateBy,
                                          updateDate, active):
        body = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soapenv:Envelope " \
               "xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\"><soapenv:Header " \
               "/><soapenv:Body><request><requestName>UpdateFacilityPersonnelSignerData</requestName>" + \
               "<requestXml><facnum>" + facnum + "</facnum><clubcode>" + clubcode + "</clubcode><PersonnelID>" + \
               personnelId + "</PersonnelID><Addr1>" + addr1 + "</Addr1><Addr2>" + addr2 + "</Addr2><CITY>" + city + \
               "</CITY><ST>" + st + "</ST><ZIP>" + zip + "</ZIP><ZIP4>" + zip4 + "</ZIP4><email>" + email + \
               "</email><Phone>" + phone + "</Phone><insertBy>" + insertBy + "</insertBy><ContractStartDate>" + \
               contractStartDate + "</ContractStartDate><ContractEndDate>" + contractEndDate + "</ContractEndDate>" + \
               "<insertDate>" + insertDate + "</insertDate><updateBy>" + updateBy + "</updateBy><updateDate>" + \
               updateDate + "</updateDate><active>" + active + \
               "</active></requestXml></request></soapenv:Body></soapenv:Envelope> "
        return self.sendRequest(body)

    def updateVehicleServices(self, facnum, clubcode, vehiclesTypeId, scopeServiceId, insertBy):
        body = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soapenv:Envelope " \
               "xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\"><soapenv:Header " \
               "/><soapenv:Body><request><requestName>UpdateVehicleServices</requestName><requestXml><facnum>" + \
               facnum + "</facnum><clubcode>" + clubcode + "</clubcode><VehiclesTypeID>" + vehiclesTypeId + \
               "</VehiclesTypeID><ScopeServiceID>" + scopeServiceId + "</ScopeServiceID><insertBy>" + insertBy + \
               "</insertBy></requestXml></request></soapenv:Body></soapenv:Envelope> "
        return self.sendRequest(body)

    def updateAARPortalTracking(self, facnum, clubcode, facId, trackingId, portalInspectionDate, loggedIntoPortal,
                                numberUnacknowledgedTows, inProgressTows, inProgressWalkIns,
                                insertBy, insertDate, updateBy, updateDate, active):
        body = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soapenv:Envelope " \
               "xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\"><soapenv:Header " \
               "/><soapenv:Body><request><requestName>UpdateAARPortalTracking</requestName><requestXml><facnum>" + \
               facnum + "</facnum><clubcode>" + clubcode + "</clubcode><FACID>"+facId+"</FACID><TrackingID>" + trackingId + \
               "</TrackingID><PortalInspectionDate>" + portalInspectionDate + \
               "</PortalInspectionDate><LoggedIntoPortal>" + loggedIntoPortal + \
               "</LoggedIntoPortal><NumberUnacknowledgedTows>" + numberUnacknowledgedTows + \
               "</NumberUnacknowledgedTows><InProgressTows>" + inProgressTows + \
               "</InProgressTows><InProgressWalkIns>" + inProgressWalkIns + "</InProgressWalkIns><insertBy>" + \
               insertBy + "</insertBy><insertDate>" + insertDate + "</insertDate><updateBy>" + updateBy + \
               "</updateBy><updateDate>" + updateDate + "</updateDate><active>" + active + \
               "</active></requestXml></request></soapenv:Body></soapenv:Envelope> "
        return self.sendRequest(body)

    def updateVehicles(self, facnum, clubcode, vehicleid, insertDate, insertBy):
        body = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soapenv:Envelope " \
               "xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\"><soapenv:Header " \
               "/><soapenv:Body><request><requestName>UpdateFacVehicles</requestName><requestXml><facnum>" + facnum + \
               "</facnum><clubcode>" + clubcode + "</clubcode><VehicleID>" + vehicleid + "</VehicleID><insertDate>" + \
               insertDate + "</insertDate><insertBy>" + insertBy + \
               "</insertBy></requestXml></request></soapenv:Body></soapenv:Envelope> "
        return self.sendRequest(body)

    def getFacilityData(self, facnum, clubcode):
        body = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soapenv:Envelope " \
               "xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\"><soapenv:Header " \
               "/><soapenv:Body><request><requestName>GetFacilityData</requestName><requestXml><facnum>"+facnum+"</facnum" \
               "><clubcode>"+clubcode+"</clubcode></requestXml></request></soapenv:Body></soapenv:Envelope> "
        return self.sendRequest(body)

    def updateFacilityInfo(self, facNum, clubCode, businessName, busTypeId, entityName, assignToId, officeId,
                                          taxIdNumber, facilityRepairOrderCount, facilityAnnualInspectionMonth,
                                          inspectionCycle, timeZoneId, svcAvailability, facilityTypeId,
                                          automotiveRepairNumber, automotiveRepairExpDate, contractCurrentDate,
                                          contractInitialDate, billingMonth, billingAmount, internetAccess, webSite,
                                          terminationDate, terminationId, terminationComments, insertBy, insertDate,
                                          updateBy, updateDate, active, achParticipant, insuranceExpDate,
                                          contractTypeId):
        body = ""