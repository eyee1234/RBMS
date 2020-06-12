import flask
from application import db
from werkzeug.security import generate_password_hash,check_password_hash

class User(db.Document):
    userId      = db.IntField(unique=True)
    first_name  = db.StringField(max_length=50)
    last_name   = db.StringField(max_length=50)
    email       = db.StringField(max_length=30,unique=True)
    password    = db.StringField()
    roleId      = db.StringField(unique=True)
    timestamps  = db.DateTimeField()

    def set_password(self,password):
        self.password=generate_password_hash(password)
    
    def get_password(self,password):
        return check_password_hash(self.password,password)

