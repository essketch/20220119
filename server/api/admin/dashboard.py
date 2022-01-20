from flask_restful import Resource
from server.model import Users, LectureUser, Lectures
from server import db

class AdminDashboard(Resource):

    def get(self):
        users_count = Users.query\
            .filter(Users.email != 'retired')\
            .count()
        
        lecture_fee_amount = db.session.query(Lectures.title, db.func.sum(Lectures.fee))\
            .filter(Lectures.id == LectureUser.lecture_id)\
            .filter(LectureUser.user_id == Users.id)\
            .group_by(Lectures.id)\
            .all()


        amount_list = [{'lecture_title' : row[0], 'amount' : int(row[1])} for row in lecture_fee_amount]

        return {
            'code' : 200,
            'message' : '관리자용 각종 통계 api',
            'data' : {
                'live_user_count' : users_count,
                'lecture_amount' : amount_list
            }
        }