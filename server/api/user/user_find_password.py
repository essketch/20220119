from urllib import response
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
        
        
        
        send_content = f"""
        안녕하세요. MySNS입니다.
        비밀번호 안내 드립니다.
        회원님의 비밀번호는 {user.password}입니다.
        """
        
        mailgun_url = 'https://api.mailgun.net/v3/mg.gudoc.in/messages'
        email_data = {
            'from' : 'system@gudoc.in',
            'to' : user.email,
            'subject' : '[MySNS 비밀번호 안내] 비밀번호 찾기 메일입니다',
            'text' : send_content
        }
        response = requests.post(
            url = mailgun_url,
            data = email_data,
            auth = ('api', current_app.config['MAILGUN_API_KEY'])
        )
        
        respJson = response.json()
        print(respJson)
        
            
        return {
            'code' : 200,
            'message' : '비밀번호를 이메일로 전송했습니다'
        }