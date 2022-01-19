from flask_restful import Resource
from server.model import Lectures
from flask_restful_swagger_2 import swagger

class LectureDetail(Resource):

    @swagger.doc({
        'tags' : ['lecture'],
        'description' : '특정 강의 상세 보기',
        'parameters' : [
            {
                'name' : 'lecture_id',
                'description' : '강의 번호',
                'in' : 'path',
                'type' : 'integer',
                'required' : True
            },
        ],
        'responses' : {
            '200' : {
                'description' : '강의 상세 조회'
            }
        }
    })
    def get(self, lecture_id):
        """강의 상세 보기"""
        lecture_row = Lectures.query.filter(Lectures.id == lecture_id).first()

        if lecture_row is None :
            return {
                'code' : 400,
                'message' : '해당 강의는 존재하지 않습니다.'
            }, 400

        return {
            'code' : 200,
            'message' : f'{lecture_id}번 강의 상세 조회',
            'data' : {
                'lecture' : lecture_row.get_data_object(need_teacher_info=True)
            }
        }