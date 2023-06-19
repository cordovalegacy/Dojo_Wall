from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.post import Post
from flask_app.models import user

# !Create (authenticated)

# *creates a new post
@app.route('/create/post', methods=['POST'])
def create_post():
    if 'user_id' not in session:
        return redirect('/registration')
    if not Post.validate_post(request.form):
        return redirect('/show_all')
    new_post_data = {
        'content': request.form['content'],
        'user_id': session['user_id']
    }
    Post.save_posts(new_post_data)
    return redirect('/show_all')

# *creates a new like (many to many)
@app.route('/create_comment', methods=['POST'])
def create_comment():
    if 'user_id' not in session:
        return redirect('/registration')
    data = {
        'post_id': request.form['post_id'],
        'comment': request.form['comment'],
        'user_id':session['user_id']
    }
    Post.create_comment(data)
    return redirect('/show_all')

# !Render (authenticated)

# !Update (authenticated)

# !Delete (auntenticated)

# *deletes a post
@app.route('/delete_one_post/<int:id>')
def delete_one_post(id):
    if 'user_id' not in session:
        return redirect('/registration')
    Post.delete_post({'id': id})
    return redirect('/show_all')

