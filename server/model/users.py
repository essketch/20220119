from server import db
class Users(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, default ='email 미입력') #실질 기본값
    password = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(20))
    birth_year = db.Column(db.Integer, nullable=False, default=1995)
    profile_img_url = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    retired_at = db.Column(db.DateTime)

    my_feeds = db.relationship('Feeds', backref='writer')

    def get_data_object(self, need_feeds=False):
        data = {
            'id' : self.id,
            'email' : self.email,
            'name' : self.name,
            'phone' : self.phone,
            'birth_year' : self.birth_year,
            'profile_img_url' : f"https://python202201kbj.s3.ap-northeast-2.amazonaws.com/{self.profile_img_url}" if self.profile_img_url else None,
            'created_at' : str(self.created_at),
            'retired_at' : str(self.retired_at) if self.retired_at else None,
        }

        if need_feeds:
            data['my_feeds'] = [feed.get_data_object(need_writer=False) for feed in self.my_feeds]

        return data