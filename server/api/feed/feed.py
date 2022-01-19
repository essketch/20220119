
from flask_restful import Resource, reqparse
from flask_restful_swagger_2 import swagger
from server import db
from server.model import Feeds, Users, FeedImages
from werkzeug.datastructures import FileStorage
import boto3
from flask import current_app, g
import time
import os
import hashlib
from server.api.utils import token_required



post_parser = reqparse.RequestParser()
post_parser.add_argument('lecture_id', type=int, required=True, location='form')
post_parser.add_argument('content', type=str, required=True, location='form')
post_parser.add_argument('feed_images', type=FileStorage, required=False, location='files', action='append')


class Feed(Resource):
    @swagger.doc({
        'tags' : ['feed'],
        'description' : '게시글 등록',
        'parameters' : [
            {
            'name' : 'X-Http-Token',
            'description' : '작성자, 토큰으로',
            'in' : 'header',
            'type' : 'string',
            'required' : True
            },
            {
            'name' : 'lecture_id',
            'description' : '강의',
            'in' : 'formData',
            'type' : 'integer',
            'required' : True
            },
            {
            'name' : 'content',
            'description' : '글 내용',
            'in' : 'formData',
            'type' : 'string',
            'required' : True
            },
            {
            'name' : 'feed_images',
            'description' : '게시글 첨부 사진',
            'in' : 'formData',
            'type' : 'file',
            'required' : False
            },

        ],
        'responses': {

            '200' : {
                'description' : '게시글 등록 성공'
            },

            '400' : {
                'description' : '게시글 등록 실패'
            }
        }
    })

    @token_required
    def post(self):
        """게시글 등록""" 

        args = post_parser.parse_args()
        user = g.user
        new_feed = Feeds()
        new_feed.user_id = user.id
        new_feed.lecture_id = args['lecture_id']
        new_feed.content = args['content']

        db.session.add(new_feed)
        db.session.commit()

        if args['feed_images']:
            upload_user = user

            aws_s3 = boto3.resource('s3',\
                aws_access_key_id=current_app.config['AWS_ACCESS_KEY_ID'],\
                aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY'])

            for image in args['feed_images']:
                _, file_extension = os.path.splitext(image.filename)
                encrypted_user_email = hashlib.md5(upload_user.email.encode('utf8')).hexdigest()
                now_number = round(time.time()*10000)
                s3_file_name = f"images/feed_images/MySNS_{encrypted_user_email}{now_number}{file_extension}"
                image_body = image.stream.read()
                aws_s3.\
                    Bucket(current_app.config['AWS_S3_BUCKET_NAME']).\
                    put_object(Key=s3_file_name, Body=image_body)
                aws_s3.\
                    ObjectAcl(current_app.config['AWS_S3_BUCKET_NAME'], s3_file_name).\
                    put(ACL='public-read')
                
                feed_img = FeedImages()
                feed_img.feed_id = new_feed.id
                feed_img.img_url = s3_file_name
                db.session.add(feed_img)
            db.session.commit()

        return {
            'code' : 200,
            'message' : '게시글 등록 성공',
            'data' : {
                'feed' : new_feed.get_data_object()
            }
        }
    
    @swagger.doc({
        'tags' : ['feed'],
        'description' : '게시글 목록 조회',
        'parameters' : [

        ],
        'responses': {

            '200' : {
                'description' : '게시글 조회 성공'
            },

            '400' : {
                'description' : '게시글 조회 실패'
            }
        }
    })
    def get(self) :
        """게시글 최신순 조회"""
        feed_data_arr = Feeds.query.order_by(Feeds.created_at.desc()).all()
        feeds = [row.get_data_object() for row in feed_data_arr]


        return {
            'code' : 200,
            'message' : '모든 게시글 조회',
            'data' : {
                'feeds' : feeds
            }
        }