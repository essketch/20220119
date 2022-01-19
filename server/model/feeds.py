from server import db
from server.model import feed_images

class Feeds(db.Model):
    __tablename__ = 'feeds'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    lecture_id = db.Column(db.Integer, db.ForeignKey('lectures.id'))
    content = db.Column(db.TEXT, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    
    feed_images = db.relationship('FeedImages', backref='feed')
    feed_replies = db.relationship('FeedReplies', backref='feed')

    def get_data_object(self, need_writer=True, need_replies=False):
        data = {
            'id' : self.id,
            'user_id' : self.user_id,
            'lecture_id' : self.lecture_id,
            'content' : self.content,
            'created_at' : str(self.created_at),
            'images' : [fi.get_data_object() for fi in self.feed_images]
        }
        if need_replies:
            data['replies'] = [reply.get_data_object() for reply in self.feed_replies]
            
        if need_writer:
            data['writer'] = self.writer.get_data_object()
        
        data['lecture'] = self.lecture.get_data_object()

        return data