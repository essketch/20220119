from flask import current_app, g
from flask_restful import Resource, reqparse
from flask_restful_swagger_2 import swagger

from server import db
from server.model import FeedReplies

from server.api.utils import token_required

post_parser = reqparse.RequestParser()
post_parser.add_argument('feed_id', type=int, required=True, location='form')
post_parser.add_argument('content', type=str, required=True, location='form')

put_parser = reqparse.RequestParser()
put_parser.add_argument('feed_reply_id', type=int, required=True, location='form')
put_parser.add_argument('content', type=str, required=True, location='form')



class FeedReply(Resource):
    @swagger.doc({
        'tags' : ['feed/reply'],
        'description' : '댓글 등록',
        'parameters' : [
            {
            'name' : 'X-Http-Token',
            'description' : '작성자, 토큰으로',
            'in' : 'header',
            'type' : 'string',
            'required' : True
            },
            {
            'name' : 'feed_id',
            'description' : '글 번호',
            'in' : 'path',
            'type' : 'integer',
            'required' : True
            },
            {
            'name' : 'content',
            'description' : '댓글 내용',
            'in' : 'formData',
            'type' : 'string',
            'required' : True
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
    def post(self, feed_id):
        """댓글 등록""" 

        args = post_parser.parse_args()
        user = g.user
        new_reply = FeedReplies()
        new_reply.feed_id = args['feed_id']
        new_reply.user_id = user.id
        new_reply.content = args['content']
        
        db.session.add(new_reply)
        db.session.commit()

        return {
            'code' : 200,
            'message' : '댓글 등록 성공',
            'data' : {
                'feed_reply' : new_reply.get_data_object()
            }
        }
        
    #put, 댓글의 id 받아 수정처리, 본인이 쓴 댓글, 실제 수정, 타인 400, 댓글만 수정가능
    @swagger.doc({
        'tags' : ['feed/reply'],
        'description' : '댓글 수정',
        'parameters' : [
            {
            'name' : 'X-Http-Token',
            'description' : '사용자 토큰',
            'in' : 'header',
            'type' : 'string',
            'required' : True
            },
            {
            'name' : 'feed_reply_id',
            'description' : '댓글 번호',
            'in' : 'formData',
            'type' : 'integer',
            'required' : True
            },
            {
            'name' : 'content',
            'description' : '수정 댓글 내용',
            'in' : 'formData',
            'type' : 'string',
            'required' : True
            },
        ],
        'responses': {
            '200' : {
                'description' : '댓글 수정 성공'
            },
            '400' : {
                'description' : '댓글 수정 실패'
            }
        }
    })
    @token_required
    def put(self, feed_reply_id):
        """댓글 수정""" 

        # args = put_parser.parse_args()
        # user = g.user
        # new_reply = FeedReplies()
        # new_reply.feed_id = args['feed_id']
        # new_reply.user_id = user.id
        # new_reply.content = args['content']
        
        # db.session.add(new_reply)
        # db.session.commit()

        return {
            'code' : 200,
            'message' : '댓글 수정 성공',
            }
        }