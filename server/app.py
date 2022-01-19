from flask import Flask
from flask_restful_swagger_2 import Api
from flask_swagger_ui import get_swaggerui_blueprint
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(f'server.config.{config_name}')
    db.init_app(app)

    api = Api(app, api_spec_url='/api/spec', title='my_server spec', api_version='0.1', catch_all_404s=True)

    from server.api.user import User, UserProfileImage, UserEmailFind, UserPasswordFind
    from server.api.lecture import Lecture, LectureDetail
    from server.api.feed import Feed
    from server.api.feed import FeedReply
    api.add_resource(User, '/user')
    api.add_resource(UserProfileImage, '/user/profile')
    api.add_resource(UserEmailFind, '/user/find/email')
    api.add_resource(UserPasswordFind, '/user/find/password')
    api.add_resource(Lecture,'/lecture')
    api.add_resource(LectureDetail, '/lecture/<int:lecture_id>')
    api.add_resource(Feed, '/feed')
    api.add_resource(FeedReply, '/feed/<int:feed_id>/reply')

    swagger_ui = get_swaggerui_blueprint('/api/docs', '/api/spec.json', config={'app_name' : 'my sns service'})
    app.register_blueprint(swagger_ui, url_prefix='/api/docs')

    return app

