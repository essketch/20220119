from flask_restful import Resource
from server.model import Users, LectureUser, Lectures
from server import db

class AdminDashboard(Resource):

    def get(self):
        users_count = Users.query\
            .filter(Users.email != 'retired')\
            .count()
        
        java_user_list = Users.query\
            .filter(LectureUser.user_id == Users.id)\
            .filter(LectureUser.lecture_id == Lectures.id)\
            .filter(Lectures.title == '자바')\
            .all()
        
        java_amount = db.session.query(Lectures.title, db.func.sum(Lectures.fee))\
            .filter(Lectures.id == LectureUser.lecture_id)\
            .filter(LectureUser.user_id == Users.id)\
            .filter(Lectures.title == '자바')\
            .all()

        print(java_amount)

        return {
            'code' : 200,
            'message' : '관리자용 각종 통계 api',
            'data' : {
                'live_user_count' : users_count
            }
        }