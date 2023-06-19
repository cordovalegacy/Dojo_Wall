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
@app.route('/like_show/<int:id>')
def like_show(id):
    if 'user_id' not in session:
        return redirect('/registration')
    data = {
        'show_id': id,
        'user_id':session['user_id']
    }
    Show.like_show(data)
    return redirect('/show_all')

# !Render (authenticated)

# *shows create show page 
@app.route('/create_post_page')
def create_show_page():
    if 'user_id' not in session:
        return redirect('/registration')
    logged_user = session['user_name']
    return render_template('create_post_page.html', logged_user = logged_user)

# *shows a single show's details
@app.route('/single_show_page/<int:id>')
def single_show_page(id):
    if 'user_id' not in session:
        return redirect('/registration')
    data = {
        'id': id
    }
    return render_template('single_show_page.html', single_show_data=Show.display_single_show(data))

# *shows the edit show page
@app.route('/edit_show_page/<int:id>')
def edit_show_page(id):
    if 'user_id' not in session:
        return redirect('/registration')
    data = {
        'id': id
    }
    return render_template('edit_show_page.html', single_show_data=Show.display_single_show(data))

# !Update (authenticated)

# *updates a show
@app.route('/edit/show', methods=['POST'])
def edit_show():
    if 'user_id' not in session:
        return redirect('/registration')
    id = request.form['id']
    edit_show_data = {
        'id': request.form['id'],
        'title': request.form['title'],
        'network': request.form['network'],
        'release_date': request.form['release_date'],
        'description': request.form['description'],
        'likes': None,
    }
    if not Show.validate_show(request.form):
        return redirect(f'/edit_show_page/{id}')
    Show.edit_show(edit_show_data)
    return redirect('/show_all')

# !Delete (auntenticated)

# *deletes a show
@app.route('/delete_one_show/<int:id>')
def delete_one_show(id):
    if 'user_id' not in session:
        return redirect('/registration')
    data = {
        'id': id
    }
    Show.delete_show(data)
    return redirect('/show_all')

# *dislike button, deletes from joining table.. (many to many)
@app.route('/dislike_show/<int:id>')
def dislike_show(id):
    if 'user_id' not in session:
        return redirect('/registration')
    data = {
        'show_id': id,
        'user_id': session['user_id']
    }
    Show.dislike_show(data)
    return redirect("/show_all")

# !Unused but may need
# *shows liked shows (did not use... but part of Robert Ponce Many to Many Lecture)
# @app.route('/show_liked_show/<int:id>')
# def show_liked_show(id):
#     if 'user_id' not in session:
#         return redirect('/registration')
#     data = {
#         'user_id': session['user_id'],
#         'show_id': id
#     }
#     Show.users_like_shows(data)
#     return redirect('/show_all')


