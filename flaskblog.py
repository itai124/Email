from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user,LoginManager, UserMixin
import redis

class User(UserMixin):
    def __init__(self, name, id, active=True):
        self.name = name
        self.id = id
        self.active = active

    def is_active(self):
        try:
            password=r.get(form.username.data)
            print password
            print form.password.data
            if(password==form.password.data):
                flash('You have been logged in!', 'success')
                return self.active
        except:
            return self.

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True






app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
LoginManager(app)
r = redis.Redis(host='localhost', port=6379, db=0)
posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


@login_manager.user_loader
def load_user(id):
     # 1. Fetch against the database a user by `id` 
     # 2. Create a new object of `User` class and return it.
     u = r.query.get(id)
    return User(u.name,u.id,u.active)

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Account created for - '+ form.username.data , 'success')
        r.set(form.username.data,form.password.data)
        print r.get(form.username.data)
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        print "try"
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        try:
            password=r.get(form.username.data)
            print password
            print form.password.data
            if(password==form.password.data):
                print "0"
                user = [,]
                print "1"
                user= form.username.data
                print "2"
                user.password= form.password.data
                print "3"
                login_user(user, remember=form.remember.data)
                print "4"
                flash('You have been logged in!', 'success')
                return redirect(url_for('home'))
            else:
                print "y"
                flash('Login Unsuccessful. Please check username and password', 'danger')
            #return render_template('login.html', title='Login', form=form)
        except:
                print "y"
                flash('Login Unsuccessful. Please check username and password', 'danger')
                #return render_template('login.html', title='Login', form=form)
    return render_template('login.html', title='Login', form=form) 
            
                


if (__name__)=='__main__':
    app.run(debug=True)
