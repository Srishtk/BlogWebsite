from flask import Flask, render_template, request, url_for, redirect,flash
from datetime import datetime
from flask_login import login_required, current_user, login_user, logout_user
from sqlalchemy import func

from models import Users, db, login, Comments, Blog, Category

app = Flask(__name__)
app.config['SECRET_KEY'] = "192b9bdd22ab9ed4d12e236c78afcb9acbf"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db.init_app(app)
login.init_app(app)

login.login_view = 'login'


def get_categories():
    global all_cat_num, all_cat_name
    all_cat_info = db.session.query(Category.cat_id, Category.cat_name).all()
    all_cat_num, all_cat_name = zip(*all_cat_info) if all_cat_info else ([], [])


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        if Users.query.filter_by(email=email).first():
            flash("This mail id already exists","error")
            return redirect('/register')
        user = Users(email=email, username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect('/')
    return render_template('register.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        user = Users.query.filter_by(email=email).first()
        if user is not None:
            password = request.form.get('password')
            if user.check_password(password):
                login_user(user)
                return redirect('/blogs')
            flash("Password incorrect","error")
            return redirect('/login')
        flash("mail id does not exists","error")
        return redirect('/login')
    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/blogs')
def blogs():
    if current_user.is_authenticated:
        return render_template('blogs.html')
    return redirect(url_for('read_blog'))


@app.route('/create_blog', methods=['POST', 'GET'])
@login_required
def create_blog():
    if request.method == 'POST':
        auth_id = current_user.id
        cat_id = request.form.get('cat_id')
        blog_date = datetime.now()
        blog_text = request.form.get('blog_text')
        blog_rating = 0
        blog_count = 0
        record = Blog(auth_id=auth_id, cat_id=cat_id, blog_date=blog_date, blog_text=blog_text, blog_rating=blog_rating,
                      blog_count=blog_count)
        db.session.add(record)
        db.session.commit()
        return redirect('/blogs')
    get_categories()
    return render_template('create_blog.html', category_names=all_cat_name, category_numbers=all_cat_num)


@app.route('/my_blog')
@login_required
def my_blog():
    get_categories()
    blog_list = Blog.query.filter_by(auth_id=current_user.id).all()
    return render_template('my_blog.html', category_names=all_cat_name, blog_list=blog_list)


@app.route('/modify_blog/<int:blog_id>/<string:cat_name>', methods=['POST', 'GET'])
@login_required
def modify_blog(blog_id, cat_name):
    blog = Blog.query.get(blog_id)
    if request.method == 'POST':
        if request.form['action'] == 'update':
            blog.blog_text = request.form.get('blog_text')
        else:
            Blog.query.filter_by(blog_id=blog_id).delete()
        db.session.commit()
        return redirect('/my_blog')
    return render_template('modify_blog.html', blog_id=blog_id, cat_name=cat_name, blog_text=blog.blog_text)


@app.route('/read_blog')
def read_blog():
    user_list = Users.query.all()
    blog_list = Blog.query.all()
    get_categories()
    return render_template('read_blog.html', user_list=user_list, blog_list=blog_list, category_names=all_cat_name)


@app.route('/blogDetail/<int:blog_id>/<string:cat_name>/<string:name>', methods=['POST', 'GET'])
@login_required
def blog_detail(blog_id, cat_name, name):
    blog = Blog.query.get(blog_id)
    record = Comments.query.filter_by(blog_id=blog.blog_id).filter_by(user_id=current_user.id).first()
    if request.method == 'GET':
        if current_user.id != blog.auth_id:
            blog.blog_count = blog.blog_count + 1
            db.session.commit()
        rating = db.session.query(func.avg(Comments.rating)).filter_by(blog_id=int(blog_id)).first()[0]
        if rating:
            rating=round(rating,2)
        blogdate=blog.blog_date
        blogdate=blogdate.date()
        if record is not None:
            return render_template('blog_detail.html', blog=blog, rating=rating, name=name, cat_name=cat_name,
                                   comment_text=record.comment, prev_rating=record.rating,blog_date=blogdate)
        else:
            return render_template('blog_detail.html', blog=blog, rating=rating, name=name, cat_name=cat_name,
                                   comment_text="", prev_rating="",blog_date=blogdate)

    rating = request.form.get('rating')
    comment = request.form.get('comment')
    blog_id = request.form.get('blog_id')
    old_comment = Comments.query.filter_by(blog_id=blog_id).filter_by(user_id=current_user.id).first()
    today = datetime.now()
    if old_comment is None:
        blog.blog_rating = blog.blog_rating + 1
        record = Comments(
            blog_id=blog_id,
            user_id=current_user.id,
            comment=comment,
            rating=rating,
            com_date=today
        )
        db.session.add(record)
    else:
        old_comment.rating = rating
        old_comment.comment = comment
    db.session.commit()
    return redirect(url_for('read_blog'))


@app.route('/add_category', methods=['GET', 'POST'])
def add_category():
    if current_user.is_authenticated:
        if request.method == 'POST':
            categ = request.form.get('categ')
            valid_categ = Category.query.filter_by(cat_name=categ).first()
            if valid_categ is None:
                record = Category(cat_name=categ)
                db.session.add(record)
                db.session.commit()
            return render_template('blogs.html')
        return render_template('add_category.html')
    return render_template('home.html')


if __name__ == "__main__":
    app.run(debug=True)
