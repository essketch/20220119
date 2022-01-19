from flask import g
from flask_restful import Resource, reqparse
from flask_restful_swagger_2 import swagger
from server.model import Users
from server import db
from server.api.utils import encode_token, token_required
import datetime

#파라미터 받기
get_parser = reqparse.RequestParser()
get_parser.add_argument('email', type=str, required=True, location='args')
get_parser.add_argument('name', type=str, required=True, location='args')

post_parser = reqparse.RequestParser()
post_parser.add_argument('email', type=str, required=True, location='form')
post_parser.add_argument('password', type=str, required=True, location='form')

put_parser = reqparse.RequestParser()
put_parser.add_argument('email', type=str, required=True, location='form')
put_parser.add_argument('password', type=str, required=True, location='form')
put_parser.add_argument('name', type=str, required=True, location='form')
put_parser.add_argument('phone', type=str, required=True, location='form')

delete_parser = reqparse.RequestParser()
delete_parser.add_argument('user_id', type=int, required=True, location='args')

patch_parser = reqparse.RequestParser()
patch_parser.add_argument('user_id', type=int, required=True, location='form')
patch_parser.add_argument('field', type=str, required=True, location='form')
patch_parser.add_argument('value', type=str, required=True, location='form')


class User(Resource):

    @swagger.doc({
        'tags' : ['user'],
        'description' : '사용자 정보 조회',
        'parameters' : [
            {
                'name' : 'email',
                'description' : '검색할 이메일',
                'in' : 'query',
                'type' : 'string',
                'required' : True
            },
            {
                'name' : 'name',
                'description' : '부분 일치 검색',
                'in' : 'query',
                'type' : 'string',
                'required' : True
            }
        ],
        'responses' : {
            '200' : {
                'description' : '사용자 정보 조회 성공'
            },
            '400' : {
                'description' : '사용자 정보 조회 실패'
            }
        }
    })
    def get(self):
        """사용자 정보 조회"""
        args = get_parser.parse_args()
        user_by_email = Users.query.filter(Users.email == args['email']).first()
        if args ['email']:
            if user_by_email:
                return {
                    'code': 200,
                    'message' : '사용자 이메일 검색 성공',
                    'data' : {
                        'user' : user_by_email.get_data_object()
                    }
                }
            else:
                return {
                    'code' : 400,
                    'message' : '검색 결과가 없습니다.'
                }, 400

    
        if args['name']:
            users_by_name = Users.query.filter(Users.name.like(f"%{args['name']}%")).all()
            searched_users_list = [user.get_data_object(need_feeds=True) for user in users_by_name]
            return {
                {
                'code' : 200,
                'message' : '사용자 이름 검색 성공',
                'data' : {
                    'users' : searched_users_list
                    }
                }
            }
        return {
            'code' : 400,
            'message' : '검색 결과가 없습니다.'
        }, 400

    @swagger.doc({
        'tags' : ['user'],
        'description' : '로그인',
        'parameters' : [
            {
            'name' : 'email',
            'description' : '로그인용 이메일',
            'in' : 'formData',
            'type' : 'string',
            'required' : True
            },
            {
            'name' : 'password',
            'description' : '로그인용 비밀번호',
            'in' : 'formData',
            'type' : 'string',
            'required' : True
            },
        ],
        'responses' : {
            '200' : {
                'description' : '로그인 성공'
            },
            '400' : {
                'description' : '로그인 실패'
            }
        }
    })
    def post(self):
        """로그인""" 
        args = post_parser.parse_args()

        #filter는 성능에 영향을 주지 않음
        login_user = Users.query\
            .filter(Users.email == args['email'])\
            .first()
        
        if login_user == None:
            return{
                'code' : 400,
                'message' : '잘못된 이메일입니다.',
            }, 400

        
        if login_user.verify_password(args['password']):
            return {
                'code' : 200,
                'message' : '로그인 성공',
                'data' : {
                    'user' : login_user.get_data_object(),
                    'token' : encode_token(login_user)
                }
            }
        else:
            return {
                'code' : 400,
                'message' : '비밀번호가 틀렸습니다.',
            }, 400
 
    @swagger.doc({
        'tags' : ['user'],
        'description' : '회원가입',
        'parameters' : [
            {
            'name' : 'email',
            'description' : '회원가입용 이메일',
            'in' : 'formData',
            'type' : 'string',
            'required' : True
            },
            {
            'name' : 'password',
            'description' : '회원가입용 비밀번호',
            'in' : 'formData',
            'type' : 'string',
            'required' : True
            },
            {
            'name' : 'name',
            'description' : '회원가입용 이름',
            'in' : 'formData',
            'type' : 'string',
            'required' : True
            },
            {
            'name' : 'phone',
            'description' : '회원가입용 연락처',
            'in' : 'formData',
            'type' : 'string',
            'required' : True
            },
        ],
        'responses' : {
            '200' : {
                'description' : '회원가입 성공'
            },
            '400' : {
                'description' : '회원가입 실패'
            }
        }
    })
    def put(self):
        """회원가입"""
        args = put_parser.parse_args()

        already_email_user = Users.query\
            .filter(Users.email == args['email'])\
            .first()
        
        if already_email_user:
            return {
                'code' : 400,
                'message' : '중복된 이메일입니다.'
            }, 400
        
        already_phone_user = Users.query\
            .filter(Users.phone == args['phone'])\
            .first()
        
        if already_phone_user:
            return {
                'code' : 400,
                'message' : '이미 가입한 번호입니다.'
            }, 400

        new_user = Users()
        new_user.email = args['email']
        new_user.password = args['password']
        new_user.name = args['name']
        new_user.phone = args['phone']

        db.session.add(new_user)
        db.session.commit()

        return {
            "code" : 200,
            'message' : '회원가입 성공',
            'data' : {
                'user' : new_user.get_data_object(),
                'token' : encode_token(new_user)
            }
        }

    @swagger.doc({
        'tags' : ['user'],
        'description' : '회원 탈퇴',
        'parameters' : [
            {
                'name' : 'X-Http-Token',
                'description' : '인증 토큰',
                'in' : 'header',
                'type' : 'string',
                'required' : True
            },
        ],
        'responses': {

            '200' : {
                'description' : '탈퇴 성공'
            },

            '400' : {
                'description' : '탈퇴 실패'
            }
        }
    })
    @token_required
    def delete(self):
        """회원 탈퇴"""
        args = delete_parser.parse_args()
        
        delete_user = g.user
        
        delete_user.name = '탈퇴회원'
        delete_user.email = 'retired'
        delete_user.password = 'retired'
        delete_user.phone = 'retired'
        delete_user.retired_at = datetime.datetime.utcnow()
        db.session.add(delete_user)
        db.session.commit()

        return {
            'code' : 200,
            'message' : '회원 탈퇴 성공'
        }
    
    @swagger.doc({
        'tags' : ['user'],
        'description' : '회원 정보 수정',
        'parameters' : [
            {
            'name' : 'user_id',
            'description' : '수정할 사용자 번호',
            'in' : 'formData',
            'type' : 'integer',
            'required' : True
            },
            {
            'name' : 'field',
            'description' : '수정할 항목',
            'in' : 'formData',
            'type' : 'string',
            'enum' : ['name', 'phone'],
            'required' : True
            },
            {
            'name' : 'value',
            'description' : '수정할 값',
            'in' : 'formData',
            'type' : 'string',
            'required' : True
            },

        ],
        'responses': {

            '200' : {
                'description' : '회원 정보 수정 성공'
            },

            '400' : {
                'description' : '회원 정보 수정 실패'
            }
        }
    })
    def patch(self):
        """사용자 정보 변경"""
        args = patch_parser.parse_args()
        edit_user = Users.query.filter(Users.id == args['user_id']).first()
        
        if not edit_user:
            return{
                'code' : 400,
                'message' : '해당 사용자는 존재하지 않습니다'
            }, 400


        if args['field']== 'name' :
            edit_user.name = args['value']
            db.session.add(edit_user)
            db.session.commit()

            return {
                'code' : 200,
                'message' : '이름 변경에 성공했습니다'
            }

        elif args['field'] == 'phone' :
            edit_user.phone = args['value']
            db.session.add(edit_user)
            db.session.commit()
            return {
                'code' : 200,
                'message' : '연락처 변경에 성공했습니다'
            }

        return {
            '임시' : '회원정보 일부 수정'
        }