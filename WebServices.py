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


@app.route('/')
def hello_world():
    return '{:}'


@app.route('/getPersonnelTypes')
def getPersonnelTeypes():
    facilityId = str(request.args.get('facilityId'))
    return queryDb("select distinct(personnelTypeName), a.PersonnelTypeID  from tblPersonnelType$ a, tblPersonnel$ b where a.PersonnelTypeID = b.PersonnelTypeID and FacID = "+facilityId)


@app.route('/getPersonnelsDetails')
def getPersonnelDetails():
    facilityId = str(request.args.get('facilityId'))
    personnelTypeId = str(request.args.get('personnelTypeId'))

    return queryDb("select * from tblPersonnel$ where facid = "+facilityId+ " and personnelTypeId = "+personnelTypeId)

@app.route('/getScopeOfServicDetails')
def getScopeOfService():
    facilityId = str(request.args.get('facilityId'))
    return queryDb("select * from tblScopeofService$ where FACID = "+facilityId)

@app.route('/getVehicleServicesForFacility')
def getVehicleServicesForFacility():
    facilityId = str(request.args.get('facilityId'))
    return queryDb("select * from tblScopeofServiceType$ a, tblVehicleServices$ b where a.ScopeServiceID = b.ScopeServiceID and a.active = 1 and FACID = "+facilityId)
#
# @app.route('/getFacilities')
# def getfacilities():
#     return s


@app.route('/<path:path>')
def catch_all(path):
    return '[]'


if __name__ == '__main__':
    app.run()
