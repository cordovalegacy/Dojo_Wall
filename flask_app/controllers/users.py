from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.post import Post
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# !Create

# *create registered user (remember to authenticate routes)
# ADD BRCYPT AND USER ID IN SESSION FOR PROPER LOG/REG
# ADD FORM VALIDATION: STATICMETHOD IN MODEL AND RE-UP FORM IN TEMPLATE
@app.route('/register', methods=['POST'])
def register():
    if not User.validate(request.form):
        return redirect('/registration')
    user_data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(user_data)
    name = user_data['first_name']
    session['user_id'] = id
    session['user_name'] = name
    return redirect('/show_all')

# *logs user in and validates
@app.route('/login', methods = ['POST'])
def login():
    logged_user = User.get_one_user_by_email(request.form)
    if not logged_user:
        flash("Invalid Email Address/Password", 'Login')
        return redirect('/registration')
    if not bcrypt.check_password_hash(logged_user.password, request.form['password']):
        return redirect('/')
    session['user_id'] = logged_user.id
    session['user_name'] = logged_user.first_name
    return redirect('/show_all')

# !Render (authenticated)

# *redirect to registration/login page
@app.route('/')
def index():
    return redirect('/registration')

# *show registration/login page
@app.route('/registration')
def create_user_page():
    return render_template('registration.html')

# *home page 
@app.route('/show_all')
def show_all():
    if 'user_id' not in session:
        return redirect('/registration')
    posts = Post.get_all_posts_with_user()
    return render_template('home_page.html', posts = posts, user = {'id': session['user_id']})

# !Clear Session

# *log user out
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/registration')

