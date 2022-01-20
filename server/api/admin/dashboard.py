from flask_restful import Resource
from server.model import Users, LectureUser, Lectures
from server import db
import datetime

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


        gender_user_count_list = db.session.query(Users.gender, db.func.count(Users.id))\
            .filter(Users.retired_at == None)\
            .group_by(Users.gender)\
            .all()
        gender_user_counts = [{'gender' : row[0], 'user_count' : int(row[1])} for row in gender_user_count_list]

        now = datetime.datetime.utcnow()
        diff_days = datetime.timedelta(days= -10)
        ten_days_ago = now + diff_days

        amount_by_date_list = db.session.query()\
            .filter(Lectures.id == LectureUser.lecture_id)\
            .filter(LectureUser.created_at > ten_days_ago)\
            .group_by(db.func.date(LectureUser.created_at))\
            .all()
        
        date_amounts = []

        for i in range(0, 11):
            amount_dict = {
                'date' : ten_days_ago.strftime('%Y-%m-%d'),
                'amount' : 0
            }
            date_amounts.append(amount_dict)
            ten_days_ago =+ datetime.timedelta(days=1)

        # for row in amount_by_date_list:
        #     amount_dict={
        #         'data' : str(row[0]),
        #         'amount' : int(row[1])
        #     }

    
        return {
            'code' : 200,
            'message' : '관리자용 각종 통계 api',
            'data' : {
                'live_user_count' : users_count,
                'lecture_amount' : amount_list,
                'gender_amount' : gender_user_counts,
                'date_amounts' : date_amounts
            }
        }