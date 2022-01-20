from functools import wraps
import jwt
from flask import current_app, g
from server.model import Users
from flask_restful import reqparse

token_parser = reqparse.RequestParser()
token_parser.add_argument('X-Http-Token', type=str, required=True, location='headers')


def encode_token(user):

    return jwt.encode(
        {'id' : user.id,'email' : user.email,'password' : user.password_hashed,},
        current_app.config['JWT_SECRET'],
        algorithm=current_app.config['JWT_ALGORITHM'],
        # headers=None,
        # json_encoder=None
        )

def decode_token(token):

    try:
        decoded_dict = jwt.decode(
            token,
            current_app.config['JWT_SECRET'],
            algorithms=current_app.config['JWT_ALGORITHM']
        )
        user = Users.query\
            .filter(Users.id == decoded_dict['id'])\
            .filter(Users.email == decoded_dict['email'])\
            .filter(Users.password_hashed == decoded_dict['password'])\
            .first()
        return user
    
    except jwt.exceptions.DecodeError:
        print('토큰 디코드 에러 발생')
        return None

def token_required(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        args = token_parser.parse_args()
        user = decode_token(args['X-Http-Token'])

        if user:
            g.user = user
            return func(*args, **kwargs)

        else:
            return {
                'code' : 403,
                'message' : '올바르지 않은 토큰입니다.'
            }, 403
    return decorator

def admin_required(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        user = g.user
        if not user.is_admin :
            return {
                'code' : 403,
                'message' : '권한이 없습니다'
                }, 403
        return func(*args, **kwargs)
    
    return decorator
