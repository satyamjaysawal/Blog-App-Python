# routes.py
from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from models import db, Post
from forms import PostForm
from forms import CreatePostForm
from flask import flash

main = Blueprint('main', __name__)

@main.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.created_at.desc()).paginate(page=page, per_page=5)
    return render_template('posts.html', posts=posts)

@main.route('/post/<int:id>')
def post_detail(id):
    post = Post.query.get_or_404(id)
    return render_template('post_detail.html', post=post)

@main.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')  # Flash message
        return redirect(url_for('main.index'))
    return render_template('create_post.html', form=form)

@main.route('/post/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_post(id):
    post = Post.query.get_or_404(id)

    # Ensure that the current user is the author of the post
    if post.author != current_user:
        flash('You are not authorized to update this post.', 'danger')
        return redirect(url_for('main.index'))

    form = PostForm()

    # Handle form submission and update post details
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()

        flash('Your post has been updated successfully!', 'success')
        return redirect(url_for('main.post_detail', id=post.id))

    # Prepopulate form fields with existing post data
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content

    return render_template('edit_post.html', form=form, post=post)


@main.route('/post/<int:id>/delete', methods=['POST'])
@login_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    if post.author != current_user:
        return redirect(url_for('main.index'))
    
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('main.index'))




