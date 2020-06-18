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