from flask_restful import Resource,reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token,jwt_required
from db import query

class AddVacantRoles(Resource):
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('vacant_roll_id',type=str,required=True,help="Vacant Roll ID cannot be blank.")
        parser.add_argument('Dept_name',type=str,required=True,help="Department name cannot be blank.")
        parser.add_argument('Position_vacant',type=str,required=True,help="Position Vacant cannot be blank.")
        parser.add_argument('Required_quali',type=str,required=True,help="Required Qualification cannot be blank.")
        parser.add_argument('percentage',type=str,required=True,help="Percentage cannot be blank.")
        data=parser.parse_args()
        try:
            x=query(f"""SELECT * FROM team12.vacant_roles WHERE Application_id='{data['vacant_roll_id']}'""",return_json=False)
            if len(x)>0: return {"message":"A Vacant Role ID already exists with your given Vacant Role ID."},400
        except:
            return {"message":"There was an error inserting into vacant Roles table."},500
        try:
            query(f"""INSERT INTO team12.vacant_roles VALUES('{data['vacant_roll_id']}',
                                                                 '{data['Dept_name']}',
                                                                 '{data['Position_vacant']}',
                                                                 '{data['Required_quali']}',
                                                                 '{data['percentage']}')""")
            
            
        except:
            return {"message":"There was an error inserting into Vacant Roles table."},500
        return {"message":"Successfully Inserted."},201

class SeeApplication(Resource):
    def get(Resource):
        try:
            return query(f"""Select * from team12.app_details""")
        except:
            return {"message": "There was an error connecting to Application details table"}, 200

class WriteStatus(Resource):
    def post(Resource):
        parser=reqparse.RequestParser()
        parser.add_argument('Application_id',type=int,required=True,help="Application Details can not be blank.")
        parser.add_argument('id_Status',type=str,required=True,help="Status name cannot be blank.")
        data=parser.parse_args()
        try:
            x=query(f"""SELECT * FROM team12.status_table WHERE Application_id={data['Application_id']}""",return_json=False)
            if len(x)>0: 
                query(f"""UPDATE status_table SET id_Status='{data['id_Status']}'WHERE Application_id={data['Application_id']}""")
        #except:
            #return {"message":"There was an error inserting into Write Status table."},500
        #try:
            else:
                query(f"""INSERT INTO team12.status_table VALUES({data['Application_id']},
                                                                 '{data['id_Status']}')""")
            
            
        except:
            return {"message":"There was an error inserting into Write Status table."},500
        return {"message":"Successfully Inserted."},201

class Recruited_Faculty(Resource):
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('EmailId',type=str,required=True,help="EmailId can not be blank.")
        parser.add_argument('Roll_id',type=str,required=True,help="Role ID cannot be blank.")
        data=parser.parse_args()
        try:
            x=query(f"""SELECT * FROM team12.recruited_faculty WHERE EmailId='{data["EmailId"]}'""",return_json=False)
            if len(x)>0: return {"message":"Faculty with that EmailId already exists"}, 400
            
        except:
            return{"message":"There was an error inserting into Recruited Faculty table"}, 500
        try:
            query(f"""INSERT INTO team12.recruited_faculty VALUES('{data["EmailId"]}',
                                                                 '{data['Roll_id']}')""")
            query(f"""DELETE FROM status_table WHERE Application_id IN (SELECT Application_id FROM app_details WHERE EmailId IN ('{data["EmailId"]}'))""")
            query(f"""DELETE FROM app_details WHERE EmailId IN ('{data["EmailId"]}')""")
        except:
            return{"message":"There was an error inserting into Recruited Faculty table"}, 500
        return{"message":"Successfully Inserted"}, 200

'''class DeleteApplication(Resource):
    def delete(self):
        parser=reqparse.RequestParser()
        parser.add_argument('EmailId',type=str,required=True,help="EmailId can not be blank.")
        data=parser.parse_args()
        try:'''
