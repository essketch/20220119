import requests
from flask_restful import Resource, reqparse
from flask_restful_swagger_2 import swagger
from flask import current_app, g
from server.model import Users
from server import db

get_parser = reqparse.RequestParser()
get_parser.add_argument('name', type = str , required = True, location = 'args')
get_parser.add_argument('phone', type = str , required = True, location = 'args')

class UserFind(Resource):
    @swagger.doc({
        'tags' : ['user'],
        'description' : '이메일 찾기 문자 전송',
        'parameters' : [
            {
                'name' : 'name',
                'description' : '사용중인 이름',
                'in' : 'query',
                'type' : 'string',
                'required' : True
            },
            {
                'name' : 'phone',
                'description' : '사용중인 전화번호',
                'in' : 'query',
                'type' : 'string',
                'required' : True
            }
        ],
        'responses' : {
            '200' : {
                'description' : '이메일이 문자로 전송되었습니다'
            },
            '400' : {
                'description' : '입력값이 틀렸습니다'
            }
        }
    })

    def get(self):
        """이메일 찾기 문자 전송"""
        args = get_parser.parse_args()
        user = Users.query\
            .filter(Users.name == args['name'])\
            .filter(Users.phone == args['phone'])\
            .first()
        
        if user is None:
            return {
                'code' : 400,
                'message' : '입력값이 틀렸습니다.'
            }, 400
        

        url = 'https://apis.aligo.in/send/'
        
        

        return {
            'code' : 200,
            'message' : '이메일 찾기 - 문자 전송 완료',
        }