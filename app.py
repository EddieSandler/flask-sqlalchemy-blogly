"""Blogly application."""

from flask import Flask, request, render_template, redirect,flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User,Post,Tag,PostTag

app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = "dudeitsasecret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def get_users():
    return redirect('/users')


@app.route('/users/')
def show_users():
    users = User.query.order_by(User.last_name,User.first_name).all()
    return render_template('users.html', users=users)


@app.route('/users/new/')
def show_new_form():
    return render_template('new_user_form.html')


@app.route('/users/new/', methods=['POST'])
def process_form():
    new_user=User(
    first_name = request.form["first-name"],
    last_name = request.form["last-name"],
    image_url = request.form["image"]or None

    )
    db.session.add(new_user)
    db.session.commit()
    return redirect('/users/')


@app.route('/users/<int:user_id>/', methods=["GET", "POST"])
def show_user_details(user_id):
    user = User.query.get_or_404(user_id)
    user.posts = Post.query.filter_by(user_id=user_id).all()
    return render_template('user_details.html', user=user,posts=user.posts)


@app.route('/users/<user_id>/edit', methods=['GET', 'POST'])
def show_user_edit_form(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':


        first_name = request.form["first-name"]
        last_name = request.form["last-name"]
        image_url = request.form["image"]

        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if image_url:
            user.image_url = image_url

        db.session.add(user)
        db.session.commit()
        return redirect('/users/')

    return render_template('edit_user_form.html', user=user)


@app.route('/users/<user_id>/delete', methods=['GET', 'POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users/<user_id>')



@app.route('/users/<user_id>/posts/new',methods=['GET'])
def show_post_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('new_post_form.html',user=user)

@app.route('/users/<user_id>/posts/new',methods=['POST'])
def process_post_form(user_id):
    new_post =Post(title=request.form["title"],
                   content = request.form["content"],
                   user_id=user_id)

    db.session.add(new_post)
    db.session.commit()
    flash(f"{new_post} added")
    return redirect(f'/users/{user_id}/')

@app.route('/posts/<post_id>/',methods=['GET'])
def show_post_details(post_id):
    post = Post.query.get_or_404(post_id)

    print(post.id)

    return render_template('post_details.html',post=post)


@app.route('/posts/<post_id>/edit',methods=['GET'])
def show_post_edit_form(post_id):
    post = Post.query.get_or_404(post_id)

    return render_template('edit_post_form.html',post=post)

@app.route('/posts/<post_id>/edit',methods=['POST'])
def update_post_edit_form(post_id):
    post = Post.query.get_or_404(post_id)
    title = request.form["title"]
    content = request.form["content"]

    if title:
        post.title=title
    if content:
        post.content=content

    db.session.add(post)
    db.session.commit()

    return redirect('/')







@app.route('/posts/<post_id>/delete/', methods=['GET','POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash(f'{post} deleted')
    return redirect(f'/users/')


