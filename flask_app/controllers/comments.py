from flask_app import app
from flask import redirect, request, session
from flask_app.models import comment


# *creates a new like (many to many)
@app.route('/create_comment', methods=['POST'])
def create_comment():
    if 'user_id' not in session:
        return redirect('/registration')
    data = {
        'post_id': request.form['post_id'],
        'comment': request.form['comment'],
        'user_id': session['user_id']
    }
    comment.Comment.create_comment(data)
    return redirect('/show_all')