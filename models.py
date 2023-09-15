from flask_login import UserMixin, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login = LoginManager()


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(50))
    password_hash = db.Column(db.String(300))


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Category(db.Model):
    cat_id = db.Column(db.Integer, primary_key=True)
    cat_name = db.Column(db.String(50), nullable=False)
    blogModel = db.relationship('Blog', backref='Category', lazy=True)


class Blog(db.Model):
    blog_id = db.Column(db.Integer, primary_key=True)
    auth_id = db.Column(db.Integer, db.ForeignKey(Users.id), nullable=False)
    cat_id = db.Column(db.Integer, db.ForeignKey(Category.cat_id))
    blog_date = db.Column(db.DateTime)
    blog_text = db.Column(db.Text, nullable=False)
    blog_rating = db.Column(db.Integer, default=0)
    blog_count = db.Column(db.Integer, default=0)


class Comments(db.Model):
    com_id = db.Column(db.Integer, primary_key=True)
    blog_id = db.Column(db.Integer, db.ForeignKey(Blog.blog_id))
    user_id = db.Column(db.Integer, db.ForeignKey(Users.id))
    comment = db.Column(db.Text)
    rating = db.Column(db.Integer)
    com_date = db.Column(db.DateTime)



@login.user_loader
def load_user(id):
    return Users.query.get(int(id))
