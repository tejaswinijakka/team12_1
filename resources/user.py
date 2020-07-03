from flask_restful import Resource,reqparse
from db import query
from flask import jsonify
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token,jwt_required
from resources.admin import WriteStatus
#import sys
#sys.path.append('C:\Users\Sridhar\Desktop\team12')
#import admin

class User():
    def __init__(self,EmailId,Passw):
        self.EmailId=EmailId
        self.Passw=Passw
        

    @classmethod
    def getUserByEmailId(cls,EmailId):
        result=query(f"""SELECT EmailId,Passw FROM team12.registration WHERE EmailId='{EmailId}'""",return_json=False)
        if len(result)>0: return User(result[0]["EmailId"],result[0]['Passw'])
        return None
    
class Users(Resource):
    @jwt_required
    def get(self):
        parser=reqparse.RequestParser()
        parser.add_argument('EmailId', type=str, required=True, help='EmailId Cannot be blank')
        data= parser.parse_args()
        
        #try:
        
        return query(f"""Select * from team12.registration where EmailId='{data["EmailId"]}'""")
        #except:
            #return {"message": "There was an error connecting to user table"}, 200

class UserRegistration(Resource):
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('First_Name',type=str,required=True,help="First_Name cannot be  blank!")
        parser.add_argument('Last_Name',type=str,required=True,help="Last_Name cannot be  blank!")
        parser.add_argument('EmailId',type=str,required=True,help="EmailId cannot be  blank!")
        parser.add_argument('Passw',type=str,required=True,help="Password cannot be  blank!")
        parser.add_argument('Aadhar_Passport_No',type=str,required=True,help="Aadhar or Passport Number cannot be  blank!")
        parser.add_argument('Phone_No',type=str,required=True,help="Phone Number cannot be  blank!")
        parser.add_argument('Graduated_College',type=str,required=True,help="Graduated College cannot be  blank!")
        parser.add_argument('Dept_Qualified',type=str,required=True,help="Deptartment Qualified cannot be  blank!")
        parser.add_argument('Qualification',type=str,required=True,help="Qualification cannot be  blank!")
        parser.add_argument('CGPA',type=str,required=True,help="CGPA cannot be  blank!")
        parser.add_argument('achievements',type=str,required=True,help="Achievements cannot be  blank!")
        parser.add_argument('College_Batch',type=str,required=True,help="College_Batch cannot be  blank!")
        parser.add_argument('Previous_office',type=str)
        parser.add_argument('previous_position',type=str)
        parser.add_argument('years_of_service',type=str)
        parser.add_argument('Gender',type=str,required=True,help="Gender cannot be  blank!")
        parser.add_argument('DOB',type=str,required=True,help="DOB cannot be  blank!")
        parser.add_argument('Current_address',type=str,required=True,help="Current address cannot be  blank!")
        parser.add_argument('permanent_address',type=str,required=True,help="Permanent address cannot be  blank!")
        data = parser.parse_args()
        try:
            x=query(f"""SELECT * FROM team12.registration WHERE EmailId='{data['EmailId']}'""",return_json=False)
            if len(x)>0: return {"message":"A registration with that Email already exists."}
        except:
            return {"message":"There was an error inserting into emp table."}
        #if(data['Previous_office']!=None and data['previous_position']!=None and data['years_of_service']!=None):
        try:
            query(f"""INSERT INTO team12.registration VALUES('{data['First_Name']}',
                                                                 '{data['Last_Name']}',
                                                                 '{data["EmailId"]}',
                                                                 '{data['Passw']}',
                                                                 '{data['Aadhar_Passport_No']}',
                                                                 '{data['Phone_No']}',
                                                                 '{data['Graduated_College']}',
                                                                 '{data['Dept_Qualified']}',
                                                                 '{data['Qualification']}',
                                                                 '{data['CGPA']}',
                                                                 '{data['achievements']}',
                                                                 '{data['College_Batch']}',
                                                                 '{data['Previous_office']}',
                                                                 '{data['previous_position']}',
                                                                 '{data['years_of_service']}',
                                                                 '{data['Gender']}',
                                                                 '{data['DOB']}',
                                                                 '{data['Current_address']}',
                                                                 '{data['permanent_address']}')""")
            
            
        except:
            return {"message":"There was an error inserting into emp table."},400
        return {"message":"Successfully Inserted."},201
        '''else:
            #try:
            query(f"""INSERT INTO team12.registration VALUES('{data['First_Name']}',
                                                                 '{data['Last_Name']}',
                                                                 '{data["EmailId"]}',
                                                                 '{data['Passw']}',
                                                                 '{data['Aadhar_Passport_No']}',
                                                                 '{data['Phone_No']}',
                                                                 '{data['Graduated_College']}',
                                                                 '{data['Dept_Qualified']}',
                                                                 '{data['Qualification']}',
                                                                 '{data['CGPA']}',
                                                                 '{data['achievements']}',
                                                                 '{data['College_Batch']}',
                                                                 '{data['Gender']}',
                                                                 '{data['DOB']}',
                                                                 '{data['Current_address']}',
                                                                 '{data['permanent_address']}')""")
            #except:
            return {"message":"There was an error inserting into emp table."},500
            return {"message":"Successfully Inserted."},201'''

class UserLogin(Resource):
    
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('EmailId',type=str,required=True,help="EmailID cannot be blank.")
        parser.add_argument('Passw',type=str,required=True,help="Password cannot be blank.")
        data=parser.parse_args()
        user=User.getUserByEmailId(data['EmailId'])
        if user and safe_str_cmp(user.Passw,data['Passw']):
            access_token=create_access_token(identity=user.EmailId,expires_delta=False)
            return {'access_token':access_token},200
        return {"message":"Invalid Credentials!"},400

class ApplicationDetails(Resource):
    @jwt_required
    def post(self):
        parser=reqparse.RequestParser()
        #parser.add_argument('Application_id',type=int,required=True,help="Application ID cannot be blank.")
        parser.add_argument('EmailId',type=str,required=True,help="EmailID cannot be blank.")
        parser.add_argument('preferred_subj',type=str,required=True,help="Preferred Subject cannot be blank.")
        parser.add_argument('Roll_id',type=str,required=True,help="Job Roll ID cannot be blank.")
        parser.add_argument('Research_details',type=str,required=True,help="Research Details cannot be blank.")
        #parser.add_argument('EmailId',type=str,required=True,help="EmailID cannot be blank.")
        data=parser.parse_args()
        try:
            #t=query(f"""SELECT EmailId from team12.app_details WHERE EmailId =
                    #(SELECT EmailId from team12.declined)and Roll_id=
                    #(SELECT Roll_id from team12.declined)""",return_json=False)
        
            s=query(f"""SELECT COUNT(EmailId) FROM team12.app_details WHERE EmailId='{data["EmailId"]}'""",return_json=False)
            print(s)
            if(s[0]['COUNT(EmailId)']>=1 and s[0]['COUNT(EmailId)']<3):
                r=query(f"""SELECT COUNT(Roll_id) FROM team12.app_details where Roll_id='{data['Roll_id']}'""",return_json=False)
                if(r[0]['COUNT(Roll_id)']==1):
                    t=query(f"""SELECT id_Status FROM status_table WHERE Application_id=
                            (SELECT Application_id FROM app_details WHERE EmailId = '{data["EmailId"]}'
                                                                        and Roll_id ='{data["Roll_id"]}')""",return_json=False)
                    print(t)
                    if(len(t)>0):
                        if(t[0]['id_Status']=='DECLINED' or t[0]['id_Status']=='Declined' or t[0]['id_Status']=='declined'or t[0]['id_Status']=='REJECTED'or t[0]['id_Status']=='Rejected'or t[0]['id_Status']=='rejected'):
                            return{"message":"YOU HAVE BEEN DECLINED FOR THE CORRESPONDING ROLE ID. YOU CANNOT APPLY FOR THAT ROLE AGAIN"}
                        else:
                            try:
                                query(f"""INSERT INTO team12.app_details(EmailId,preferred_subj,Roll_id,Research_details)
                                        VALUES('{data["EmailId"]}',
                                        '{data['preferred_subj']}',
                                        '{data['Roll_id']}',
                                        '{data['Research_details']}')""")
                                query(f"""INSERT INTO team12.app_details1(EmailId1,preferred_subj1,Roll_id1,Research_details1)
                                        VALUES('{data["EmailId"]}',
                                        '{data['preferred_subj']}',
                                        '{data['Roll_id']}',
                                        '{data['Research_details']}')""")
                            except:
                                return {"message":"There was an error inserting into the table"}
                            return{"message":"Successfully inserted"},200
                    else:
                        try:
                            query(f"""INSERT INTO team12.app_details(EmailId,preferred_subj,Roll_id,Research_details)
                                        VALUES('{data["EmailId"]}',
                                        '{data['preferred_subj']}',
                                        '{data['Roll_id']}',
                                        '{data['Research_details']}')""")
                            query(f"""INSERT INTO team12.app_details1(EmailId1,preferred_subj1,Roll_id1,Research_details1)
                                        VALUES('{data["EmailId"]}',
                                        '{data['preferred_subj']}',
                                        '{data['Roll_id']}',
                                        '{data['Research_details']}')""")
                        except:
                            return {"message":"There was an error inserting into the table"}
                        return{"message":"Successfully inserted"},200

                elif(r[0]['COUNT(Roll_id)']>1):
                    t=query(f"""SELECT id_Status FROM status_table WHERE Application_id IN
                            (SELECT Application_id FROM app_details WHERE EmailId = '{data["EmailId"]}'
                                                                        and Roll_id ='{data["Roll_id"]}')""",return_json=False)
                    print(t)
                    if(len(t)>0):
                        if(t[0]['id_Status']=='DECLINED' or t[0]['id_Status']=='Declined' or t[0]['id_Status']=='declined'):
                            return{"message":"YOU HAVE BEEN DECLINED FOR THE CORRESPONDING ROLE ID. YOU CANNOT APPLY FOR THAT ROLE AGAIN"}
                        else:
                            try:
                                query(f"""INSERT INTO team12.app_details(EmailId,preferred_subj,Roll_id,Research_details)
                                        VALUES('{data["EmailId"]}',
                                        '{data['preferred_subj']}',
                                        '{data['Roll_id']}',
                                        '{data['Research_details']}')""")
                                query(f"""INSERT INTO team12.app_details1(EmailId1,preferred_subj1,Roll_id1,Research_details1)
                                        VALUES('{data["EmailId"]}',
                                        '{data['preferred_subj']}',
                                        '{data['Roll_id']}',
                                        '{data['Research_details']}')""")
                            except:
                                return {"message":"There was an error inserting into the table"}
                            return{"message":"Successfully inserted"},200
                    else:
                        try:
                            query(f"""INSERT INTO team12.app_details(EmailId,preferred_subj,Roll_id,Research_details)
                                VALUES('{data["EmailId"]}',
                                        '{data['preferred_subj']}',
                                        '{data['Roll_id']}',
                                        '{data['Research_details']}')""")
                            query(f"""INSERT INTO team12.app_details1(EmailId1,preferred_subj1,Roll_id1,Research_details1)
                                        VALUES('{data["EmailId"]}',
                                        '{data['preferred_subj']}',
                                        '{data['Roll_id']}',
                                        '{data['Research_details']}')""")
                        except:
                            return {"message":"There was an error inserting into the table"}
                        return{"message":"Successfully inserted"},200
                        
                    #print(t)
                    #if(t[0]['EmailId']=='EmailId'):return{"message":"YOU HAVE BEEN DECLINED FOR THE CORRESPONDING ROLE ID. YOU CANNOT APPLY FOR THAT ROLE AGAIN"}
            elif(s[0]['COUNT(EmailId)']==0):
                try:
                    query(f"""INSERT INTO team12.app_details(EmailId,preferred_subj,Roll_id,Research_details)
                                VALUES('{data["EmailId"]}',
                                        '{data['preferred_subj']}',
                                        '{data['Roll_id']}',
                                        '{data['Research_details']}')""")
                    query(f"""INSERT INTO team12.app_details1(EmailId1,preferred_subj1,Roll_id1,Research_details1)
                                        VALUES('{data["EmailId"]}',
                                        '{data['preferred_subj']}',
                                        '{data['Roll_id']}',
                                        '{data['Research_details']}')""")
                    #query(f"""INSERT INTO team12.status_table VALUES({data['Application_id']},'Recieved')""")
                except:
                    return {"message":"There was an error inserting into the table"}
                return{"message":"Successfully inserted"},200

        except:
            return{"message":"There was an error connecting to the Tables."}
        q=query(f"""SELECT COUNT(EmailId) FROM team12.app_details WHERE EmailId='{data["EmailId"]}'""",return_json=False)
        print(q)
        if(q[0]['COUNT(EmailId)']<3):
            #try:
            #x=query(f"""SELECT * FROM team12.app_details WHERE Application_id={data['Application_id']}""",return_json=False)
            #if len(x)>0: return {"message":"An application with that Application ID already exists."},400
            try:
                query(f"""INSERT INTO app_details(EmailId,preferred_subj,Roll_id,Research_details)
                                VALUES('{data["EmailId"]}','{data['preferred_subj']}','{data['Roll_id']}','{data['Research_details']}')""")
                query(f"""INSERT INTO team12.app_details1(EmailId1,preferred_subj1,Roll_id1,Research_details1)
                                        VALUES('{data["EmailId"]}',
                                        '{data['preferred_subj']}',
                                        '{data['Roll_id']}',
                                        '{data['Research_details']}')""")
                #query(f"""INSERT INTO team12.status_table(Application_id,id_Status)""")
                return{"message":"Successfully inserted"},200
            except:
                return {"message": "An error occurred while inserting into Application details."}
                #except:
                #return {"message":"There was an error inserting into table."},500
        else:
            return {"message":"You can fill the application form only thrice."}

class SeeVacantRoles(Resource):
    @jwt_required
    def get(self):
        #parser=reqparse.RequestParser()
        #parser.add_argument('vacant_roll_id', type=str, required=True, help='Vacant Role Id Cannot be blank')
        #data= parser.parse_args()
        try:
        
            return query(f"""Select vacant_roll_id as 'Role ID' ,Position_vacant as 'Role',Required_quali as 'Prerequisites',Dept_name as 'Department' from team12.vacant_roles""")
        except:
            return {"message": "There was an error connecting to Vacant roles table"}, 200

class SeeMyAppDetails(Resource):
    @jwt_required
    def get(self):
        parser=reqparse.RequestParser()
        parser.add_argument('EmailId', type=str, required=True, help='EmailId Cannot be blank')
        data= parser.parse_args()
        try:
            #q=query(f"""SELECT COUNT(EmailId) FROM team12.app_details WHERE EmailId='{data["EmailId"]}'""",return_json=False)
            #if(q[0]['COUNT(EmailId)']>1):
                #return query(f"""SELECT * FROM app_details WHERE EmailId IN '{data["EmailId"]}'""")
            #else:
            return query(f"""SELECT Application_id as 'Application ID',Roll_id as 'Role ID'  FROM app_details WHERE EmailId = '{data["EmailId"]}'""")
        except:
            return{"message":"Could not connect to Application Details Table"}

class SeeStatus(Resource):
    #@jwt_required
    def get(self):
        parser=reqparse.RequestParser()
        parser.add_argument('EmailId', type=str, required=True, help='Email Id Cannot be blank')
        #parser.add_argument('Roll_id',type=str,required=True,help='Role ID cannot be blank')
        data = parser.parse_args()
        '''try:
            
            query(f"""drop view v1""")
            query(f"""drop view v2""")
        except:
            return{"message":"couldnt drop the views"}
        try:
            q=( query(f"""SELECT vacant_roll_id as 'Role ID', Dept_name as 'DEPARTMENT',Position_Vacant as 'POSITION' FROM vacant_roles 
                            WHERE vacant_roll_id= (SELECT Roll_id FROM app_details WHERE Application_id=
                            (SELECT Application_id FROM status_table WHERE Application_id= {data['Application_id']}))""",return_json=False),
                query(f"""SELECT id_status as 'STATUS' FROM status_table WHERE Application_id = {data['Application_id']} """,return_json=False))
            return jsonify(q)
            return query(f"""SELECT id_status as 'STATUS' FROM status_table WHERE Application_id = {data['Application_id']} """)
            q = query(f"""SELECT * FROM app_details NATURAL JOIN status_table WHERE EmailId = '{data["EmailId"]}'""")
            query(f"""create view v1 as select Application_id,Roll_id from team12.app_details where EmailId='{data["EmailId"]}'""")
        except:
            return {"message":"There was an error creating view v1"}
        #return {"message":"V1 successfully created"}
        try:
            query(f"""create view v2 as select Application_id,Roll_id,Dept_name,Position_vacant FROM v1 INNER JOIN vacant_roles ON  v1.Roll_id=vacant_roles.vacant_roll_id""")
        except:
            return {"message":"There was an error creating v2"}
        #return{"message":"V2 successfully created"}
        try:
            return query(f"""SELECT v2.Application_id,Roll_id,Dept_name,Position_vacant,id_Status FROM v2 INNER JOIN status_table ON  v2.Application_id= status_table.Application_id""")
            #return query(f"""select EmailId from team12.app_details where EmailId='{data["EmailId"]}'""")
        except:
            return{"message":"There was an error connecting to the views"}'''
        try:
            return query(f"""select a.Application_id1,Roll_id1,Dept_name1,Position_vacant1,id_Status,prev_status from app_details1 a  inner join status_table s on  a.Application_id1=s.Application_id inner join vacant_roles1 v on a.Roll_id1 = v.vacant_roll_id1 where EmailId1='{data["EmailId"]}'""")

        except:
            return{"message":"There was an error connecting to tables"}

'''class Notification(Resource):
    @jwt_required
    def get(self):
        parser=reqparse.RequestParser()
        parser.add_argument('EmailId', type=str, required=True, help='EmailId Cannot be blank')
        data = parser.parse_args()
        #try:
        #q1 = query(f"""SELECT id_Status from team12.status_table where Application_id in
                      #(Select Application_id1 from app_details1 where EmailId1 = '{data["EmailId"]}')""")
        #q2 = query(f"""SELECT i from team12.status_table1 where Application_id2 in 
                      #(Select Application_id1 from app_details1 where EmailId1 = '{data["EmailId"]}')""")
        #print(len(q1))
        #if(q1[0]['id_Status']!=q2[0]['id_Status2']):
        
        return query(f"""UPDATE status_table SET prev_status= 
                     (SELECT id_Status from team12.status_table where Application_id=
                      (Select Application_id1 from app_details1 where EmailId1 = '{data["EmailId"]}'))
                      WHERE Application_id2=
                       (Select Application_id1 from app_details1 where EmailId1 = '{data["EmailId"]}')""")
                
                
            #return {"message":"NOTIFICATION"}
        #except:
            #return{"message":"There is an error connecting to the Write Status."}'''

class UpdateStatus(Resource):
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('Application_id', type=int, required=True, help='Application ID Cannot be blank')
        #parser.add_argument('id_Status',type=str,required=True,help='Status cannot be blank')
        data=parser.parse_args()
        try:
            query(f"""UPDATE status_table SET prev_status = id_Status where Application_id={data['Application_id']}""")
        except:
            return{"message":"There was an error connecting to the status table"}
        return{"message":"Successfully updated"}