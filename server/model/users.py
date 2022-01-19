from server import db
import datetime
import hashlib

class Users(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, default ='email 미입력') #실질 기본값
    password_hashed = db.Column(db.String(32), nullable=False)
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
    
    @property
    def password(self):
        raise AttributeError('password 변수는 쓰기 전용입니다. 조회는 불가합니다.')
    
    @password.setter
    def password(self, input_password):
        self.password_hashed = self.generate_password_hash(input_password)
    
    def generate_password_hash(self, input_password):
        return hashlib.md5(input_password.encode('utf8')).hexdigest()
    
    def verify_password(self, input_password):
        hashed_input_pw = self.generate_password_hash(input_password)
        return self.password_hashed == hashed_input_pw