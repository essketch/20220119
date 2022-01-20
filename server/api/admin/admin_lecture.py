from flask_restful import Resource
from flask import g
from flask_restful_swagger_2 import swagger
from server.model import Lectures
from server.api.utils import token_required, admin_required
from server import db
from flask_restful import reqparse

post_parser = reqparse.RequestParser()
post_parser.add_argument('title', type=str, required=True, location='form')
post_parser.add_argument('campus', type=str, required=True, location='form')
post_parser.add_argument('fee', type=int, required=True, location='form')

patch_parser = reqparse.RequestParser()
patch_parser.add_argument('lecture_id', type=int, required=True, location='form')
patch_parser.add_argument('field', type=str, required=True, location='form')
patch_parser.add_argument('value', type=str, required=True, location='form')


class AdminLecture(Resource):
    @swagger.doc({
        'tags' : ['admin'],
        'description' : '관리자 강의 과목 추가',
        'parameters' : [
            {
                'name' : 'X-Http-Token',
                'description' : '관리자 인증용 헤더',
                'in' : 'header',
                'type' : 'string',
                'required' : True, 
            },
            {
                'name' : 'title',
                'description' : '강의 제목',
                'in' : 'formData',
                'type' : 'string',
                'required' : True, 
            },
            {
                'name' : 'campus',
                'description' : '캠퍼스 이름',
                'in' : 'formData',
                'type' : 'string',
                'required' : True, 
            },
            {
                'name' : 'fee',
                'description' : '수강료',
                'in' : 'formData',
                'type' : 'integer',
                'required' : True, 
            },
        ],
        'responses' : {
            '200' : {
                'description' : '강의 등록 성공'
            }
        }
    })
    @token_required
    @admin_required
    def post(self):
        """관리자 강의 추가 등록"""

        args = post_parser.parse_args()

        lecture = Lectures()
        lecture.title = args['title']
        lecture.campus = args['campus']
        lecture.fee = args['fee']

        db.session.add(lecture)
        db.session.commit()


        return {
            'code' : 200,
            'message' : '강의 추가 등록 성공',
        }

    @swagger.doc({
        'tags' : ['admin'],
        'description' : '관리자 강의 정보 수정',
        'parameters' : [
            {
                'name' : 'X-Http-Token',
                'description' : '관리자 인증용 헤더',
                'in' : 'header',
                'type' : 'string',
                'required' : True, 
            },
            {
                'name' : 'lecture_id',
                'description' : '수정 강의',
                'in' : 'formData',
                'type' : 'integer',
                'required' : True, 
            },
            {
                'name' : 'field',
                'description' : '수정 항목',
                'in' : 'formData',
                'type' : 'string',
                'enum' : ['title', 'campus', 'fee', 'teacher_id'],
                'required' : True, 
            },
            {
                'name' : 'value',
                'description' : '수정 값',
                'in' : 'formData',
                'type' : 'string',
                'required' : True, 
            },
        ],
        'responses' : {
            '200' : {
                'description' : '강의 정보 수정 성공'
            }
        }
    })
    @token_required
    @admin_required
    def patch(self):
        """관리자 강의 정보 수정"""

        args = patch_parser.parse_args()

        lecture = Lectures.query.filter(Lectures.id == args['lecture_id']).first()

        if lecture == None:
            return {
                'code' : 400,
                'message' : '해당 강의는 존재하지 않습니다.'
            }, 400

        if args['field'] == 'title' :
            lecture.title = args['value']
        
        elif args['field'] == 'campus' :
            lecture.title = args['value']
        
        elif args['field'] == 'fee' :
            lecture.title = int(args['value'])

        elif args['field'] == 'teacher_id' :
            lecture.title = int(args['value'])
        
        else:
            return {
                'code' : 400,
                'message' : '올바르지 않은 값입니다.'
            }

        db.session.add(lecture)
        db.session.commit()


        return {
            'code' : 200,
            'message' : '강의 수정 성공',
        }