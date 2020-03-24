#for flask
import os
import StringIO
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from _init_ import app, db, bcrypt
from forms import RegistrationForm, LoginForm , UpdateAccountForm, PostForm
from flask import render_template, url_for, flash, redirect, request
from _init_ import app, db, bcrypt
from forms import RegistrationForm, LoginForm
from models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
#for sockets with server
import pprint
import imaplib
import mailbox
import email.utils
import threading
import localmail
import smtplib
import socket
from socket import *
#for encrypt
import  pickle
import ssl
from email.mime.text import MIMEText
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.serialization import load_pem_public_key
#
import re


#defs--------------------------------------------------------
def generate_a_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048*3,
        backend=default_backend())
    return private_key

def generate_key():
    key = Fernet.generate_key()
    return key

def encrypt_a_msg(message, public_key):
    encrypted = public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted

def decrypt_a_msg(encrypted, private_key):
    original = private_key.decrypt(
        encrypted,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return original

def connect_send(src,dst,subject,txt):
    TCPclientsock = socket(AF_INET,SOCK_STREAM)
    buffsize = 1024*100
    #TCPclientsock.settimeout(10)
    TCPclientsock.connect(('10.100.102.7', 50003))
    private_key = generate_a_keys()  # generates public and private keys
    public_key = private_key.public_key()
    serialized_public_key = public_key.public_bytes(encoding=serialization.Encoding.PEM,format=serialization.PublicFormat.PKCS1)  # serialize the key
    serialized_public_key = pickle.dumps(serialized_public_key)  # pickle the key
    TCPclientsock.send(serialized_public_key)  # send the key
    server_public_key = TCPclientsock.recv(buffsize)  # recv key from server
    server_public_key = pickle.loads(server_public_key)  # load the key
    server_public_key = load_pem_public_key(server_public_key, backend=default_backend())  # back to the first form
    print "allowed"
    data=["S",src,dst,subject,txt]
    byted_data= pickle.dumps(data)
    encrypted_msg = encrypt_a_msg(byted_data, server_public_key)
    print "encrypted "+encrypted_msg
    TCPclientsock.send(encrypted_msg)
    server_data = TCPclientsock.recv(buffsize)
    decrypted_msg = decrypt_a_msg(server_data,private_key)
    print "after decrypte "+ decrypted_msg
    
def connect_add():
    last_ver_emails=[]
    TCPclientsock = socket(AF_INET,SOCK_STREAM)
    #TCPclientsock.settimeout(200)
    TCPclientsock.connect(('10.100.102.7', 50003))
    buffsize = 1024 * 100
    private_key = generate_a_keys()  # generates public and private keys
    public_key = private_key.public_key()
    serialized_public_key = public_key.public_bytes(encoding=serialization.Encoding.PEM,format=serialization.PublicFormat.PKCS1)  # serialize the key
    serialized_public_key = pickle.dumps(serialized_public_key)  # pickle the key
    TCPclientsock.send(serialized_public_key)  # send the key
    server_public_key = TCPclientsock.recv(buffsize)  # recv key from server
    server_public_key = pickle.loads(server_public_key)  # load the key
    server_public_key = load_pem_public_key(server_public_key, backend=default_backend())  # back to the first form
    print "allowed"
#------------------------------------------------------
    data = ["F", None, None, None, None]
    byted_data = pickle.dumps(data)
    encrypted_msg = encrypt_a_msg(byted_data, server_public_key)
    print "encrypted " + encrypted_msg
    TCPclientsock.send(encrypted_msg)
    server_data = TCPclientsock.recv(buffsize)
    decrypted_msg = decrypt_a_msg(server_data, private_key)
    got_emails = pickle.loads(decrypted_msg)
    print "after decrtpytiom:"
    print  got_emails
    for email in got_emails:
        pprint.pprint(email)
        inp =email
        print('Author:', re.findall(r'Author- <(.+?)>', inp)[0])
        Author= re.findall(r'Author- <(.+?)>', inp)[0]
        print('Recipient:', re.findall(r'Recipient- <(.+?)>', inp)[0])
        Recipient= re.findall(r'Recipient- <(.+?)>', inp)[0]
        print('Subject:', re.findall(r'Subject: (.+?)\r\n', inp)[0])
        Subject= re.findall(r'Subject: (.+?)\r\n', inp)[0]
        print('Message:', re.findall(r'(?:.(?!\r\n))+$', inp)[0])
        Message = re.findall(r'(?:.(?!\r\n))+$', inp)[0]
        tamp=[Author,Recipient, Subject,Message]
        last_ver_emails.append(tamp)

    return last_ver_emails
    '''
    for email in got_emails:
        pprint.pprint(email)
    '''




Host = '10.100.102.7'
Port = 50003
buffsize = 1024*9
Addr = (Host,Port)


db.create_all()

@app.route("/")
@app.route("/home")
def home():
    if current_user.is_authenticated:
        posts = connect_add()
        print posts
        for posting in posts:
            print type(posting[0])
            print type(posting[1])
            print type(posting[2])
            print type(posting[3])
            print current_user.username
            if posting[0]==current_user.username:
                post = Post(title=posting[2], content=posting[3], to=posting[1], author=current_user)
                db.session.add(post)
                db.session.commit()
        posts = Post.query.filter_by(author=current_user)
    else :
        posts=[]
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
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)



@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)



@app.route("/logout")
def logout():
    logout_user()
    posts=[]
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex= os.urandom(8).encode('hex')
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn



@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        print form.to.data
        print type(form.to.data)
        post = Post(title=form.title.data, content=form.content.data, to=form.to.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        connect_send(current_user.username,form.to.data,form.title.data,form.content.data)
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Email',
                           form=form, legend='New Email')


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    if post :
        print "T"
    else:
        print "ggg"
    return render_template('post.html', title=post.title, post=post,)

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.to= form.to.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.to.data = post.to
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Email')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
        print "()"
    db.session.delete(post)
    db.session.commit()
    flash('Your Email has been deleted!', 'success')
    return redirect(url_for('home'))


