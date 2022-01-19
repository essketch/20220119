import requests
from flask_restful import Resource, reqparse
from flask_restful_swagger_2 import swagger
from flask import current_app, g
from server.model import Users
from server import db

get_parser = reqparse.RequestParser()
get_parser.add_argument('email', type = str , required = True, location = 'args')
get_parser.add_argument('name', type = str , required = True, location = 'args')
get_parser.add_argument('phone', type = str , required = True, location = 'args')

class UserPasswordFind(Resource):
    @swagger.doc({
        'tags' : ['user'],
        'description' : '비밀번호 찾기',
        'parameters' : [
            {
                'name' : 'email',
                'description' : '사용중인 이메일',
                'in' : 'query',
                'type' : 'string',
                'required' : True
            },
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
                'description' : '비밀번호가 이메일로 전송되었습니다'
            },
            '400' : {
                'description' : '입력값이 틀렸습니다'
            }
        }
    })

    def get(self):
        """비밀번호 찾기 (이메일 전송)"""
        args = get_parser.parse_args()
        user = Users.query\
            .filter(Users.email == args['email'])\
            .first()
        
        if user is None:
            return {
                'code' : 400,
                'message' : '해당 이메일이 없습니다'
            }, 400
        
        input_phone = args['phone'].replace('-', '')
        user_phone = user.phone.replace('-', '')
        
        if input_phone != user_phone or args['name'] != user.name:
            return{
                'code' : 400,
                'message' : '개인 정보가 맞지 않습니다'
            }, 400
            
        return {
            'code' : 200,
            'message' : '비밀번호를 이메일로 전송했습니다'
        }