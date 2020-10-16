from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flaskapp import db, login_manager, app
from flask_login import UserMixin



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False )
    email = db.Column(db.String(30), unique=True, nullable=False )
    password = db.Column(db.String(60), nullable=False )
    image_file = db.Column(db.String(20), nullable = False, default='default.png')
    posts = db.relationship('Post', backref='author', lazy=True)


    def get_reset_token(self, exit_sec=3600):
        s = Serializer(app.config['SECRET_KEY'], exit_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8') 

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False )
    content = db.Column(db.Text, nullable=False )
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.pub_date}')"

