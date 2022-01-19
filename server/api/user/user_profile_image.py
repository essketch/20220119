from flask_restful import Resource, reqparse
from flask_restful_swagger_2 import swagger
from werkzeug.datastructures import FileStorage
import boto3
from flask import current_app, g
import time
import os
import hashlib
from server.model import Users
from server import db
from server.api.utils import token_required

put_parser = reqparse.RequestParser()
put_parser.add_argument('profile_image', type=FileStorage, required=True, location='files', action = 'append')
put_parser.add_argument('user_id', type = int , required = True, location = 'form')
class UserProfileImage(Resource):
    @swagger.doc({
        'tags' : ['user'],
        'description' : '프로필 사진 등록',
        'parameters' : [
            {
                'name' : 'X-Http-Token',
                'description' : '인증 토큰',
                'in' : 'header',
                'type' : 'string',
                'required' : True
            },
            {
                'name' : 'profile_image',
                'description' : '프로필 사진',
                'in' : 'formData',
                'type' : 'file',
                'required' : True
            }
        ],
        'responses' : {
            '200' : {
                'description' : '프로필 사진 등록 성공'
            },
            '400' : {
                'description' : '프로필 사진 등록 실패'
            }
        }
    })
    
    @token_required
    def put(self):
        """프로필 사진 등록"""
        args = put_parser.parse_args()
        upload_user = g.user

        aws_s3 = boto3.resource('s3',\
            aws_access_key_id=current_app.config['AWS_ACCESS_KEY_ID'],\
            aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY'])
        
        for file in args['profile_image']:
            #파일 이름 재가공
            user_email = upload_user.email
            now = round(time.time() *10000)
            new_file_name=f"MySNS_{hashlib.md5(user_email.encode('utf8')).hexdigest()}{now}"
            #확장자 추출
            _, file_extension = os.path.splitext(file.filename)
            new_file_name = f"{new_file_name}{file_extension}" 
            #올라갈 경로
            s3_file_path = f'images/profile_imgs/{new_file_name}' 
            #올려줄 파일
            file_body=file.stream.read() 
            #업로드
            aws_s3.Bucket(current_app.config['AWS_S3_BUCKET_NAME']).put_object(Key=s3_file_path, Body=file_body)
            #퍼블릭 허용
            aws_s3.ObjectAcl(current_app.config['AWS_S3_BUCKET_NAME'], s3_file_path).put(ACL='public-read')
            
            upload_user.profile_img_url = s3_file_path
            db.session.add(upload_user)
            db.session.commit()


        return {
            'code' : 200,
            'message' : '사용자 프로필 사진 변경',
            'data' : {
                'user' : upload_user.get_data_object()
            }
        }