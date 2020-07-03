from flask import Flask,jsonify
import pymysql
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.user import Users,UserRegistration,UserLogin,ApplicationDetails,SeeVacantRoles,SeeStatus,SeeMyAppDetails,UpdateStatus
from resources.admin import AddVacantRoles,WriteStatus,SeeApplication,Recruited_Faculty,ViewVacancies,CheckRecruitedFaculty,DeclinedMembers
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['PROPAGATE_EXCEPTIONS']=True
app.config['PREFERRED_URL_SCHEME']='https'
app.config['JWT_SECRET_KEY']='facultyrecritmentapikey'
api = Api(app)
jwt = JWTManager(app)

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'error': 'authorization_required',
        "description": "Request does not contain an access token."
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'error': 'invalid_token',
        'message': 'Signature verification failed.'
    }), 401

api.add_resource(Users,'/user')
api.add_resource(UserRegistration,'/userreg')
api.add_resource(UserLogin,'/userlogin')
api.add_resource(AddVacantRoles,'/addvacantroles')
api.add_resource(ApplicationDetails,'/appdetails')
api.add_resource(SeeVacantRoles,'/seevacantroles')
api.add_resource(WriteStatus,'/writestatus')
api.add_resource(SeeApplication,'/seedetails')
api.add_resource(Recruited_Faculty,'/recruited')
api.add_resource(SeeStatus,'/seestatus')
api.add_resource(CheckRecruitedFaculty,'/checkfaculty')
api.add_resource(SeeMyAppDetails,'/mydetails')
api.add_resource(ViewVacancies,'/seevacanciesadmin')
api.add_resource(DeclinedMembers,'/enterdeclined')
#api.add_resource(Notification,'/notification')
api.add_resource(UpdateStatus,'/updatestatus')

if __name__=='__main__':
    app.run()