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
from sqlalchemy import  or_
#for sockets with server
import pprint
import imaplib
import mailbox
import email.utils
import threading
import localmail
import smtplib
import socket
import subprocess
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
import os
import threading



def findFiles(path,filename):
        """
        finding files in a dir
        """
        global found
        os.chdir(path)
        for root, dirs, files in os.walk(path):
            for f in files:
                if found:
                        break
                if f==filename:
                      found= root+"\\"+ f
            if found:
               break

#defs--------------------------------------------------------
def generate_a_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048*6,
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

def connect_send(src,dst,subject,txt,filename):
    TCPclientsock = socket(AF_INET,SOCK_STREAM)
    buffsize = 1024*10
    #TCPclientsock.settimeout(10)
    TCPclientsock.connect(('172.16.10.216', 50004))
    private_key = generate_a_keys()  # generates public and private keys
    public_key = private_key.public_key()
    serialized_public_key = public_key.public_bytes(encoding=serialization.Encoding.PEM,format=serialization.PublicFormat.PKCS1)  # serialize the key
    serialized_public_key = pickle.dumps(serialized_public_key)  # pickle the key
    TCPclientsock.send(serialized_public_key)  # send the key
    server_public_key = TCPclientsock.recv(buffsize)  # recv key from server
    server_public_key = pickle.loads(server_public_key)  # load the key
    server_public_key = load_pem_public_key(server_public_key, backend=default_backend())  # back to the first form
    print "allowed"
    data=["S",src,dst,subject,txt,filename]
    print data
    byted_data= pickle.dumps(data)
    encrypted_msg = encrypt_a_msg(byted_data, server_public_key)
    print "encrypted "+encrypted_msg
    TCPclientsock.send(encrypted_msg)
    server_data = TCPclientsock.recv(buffsize)
    decrypted_msg = decrypt_a_msg(server_data,private_key)
    print "after decrypte "+ decrypted_msg
    print "going to send this file"

    if filename!=None:
        print "the file name is - " + filename
        print "sending now txt file"
        Buffsize=buffsize
        basename=os.path.basename(filename)
        kind= basename.split(".")
        if kind[1]=="png" or kind[1]=="jpg":
            Buffsize=1000000
        f = open(filename, "r+b")
        l = f.read(Buffsize)
        print "opened"
        while (l):
            print l
            TCPclientsock.send(l)
            l = f.read(Buffsize)
        Buffsize = buffsize
        TCPclientsock.close()
        f.close()


def filter_emails(posts):
    good_emails=[]
    emails=Post.query.all()
    print "emails: "
    for email in emails:
        print str(email.to)
        print str(email.title)
        print str(email.content)
        for post in posts:
            print "post: "
            print post
            if str(post[1])!=str(email.to) or str(post[2])!=str(email.title) or str(post[3])!=str(email.content):
                    good_emails.append(post)
                    print "this is real email"
    return good_emails




    
def connect_add():
    last_ver_emails=[]
    TCPclientsock = socket(AF_INET,SOCK_STREAM)
    #TCPclientsock.settimeout(200)
    hostname = gethostname()
    ## getting the IP address using socket.gethostbyname() method
    ip_address = gethostbyname(hostname)
    print ip_address
    TCPclientsock.connect(("172.16.10.216", 50004))
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
    data = ["F", None, None, None, None,None]
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
        print('Message:', re.findall(r'\r\n\r\n([\w\d\s]*)', inp)[0])
        Message= re.findall(r'\r\n\r\n([\w\d\s]*)', inp)[0]
        print Message
        msg=Message.rsplit('ppppphhhhh',2)
        Message=msg[0]
        try:
            binary_code=msg[2]
            file_name=msg[1]
        except:
            binary_code=None
            file_name=None
        tamp=[Author,Recipient, Subject,Message,file_name,binary_code]
        last_ver_emails.append(tamp)

    return last_ver_emails
    '''
    for email in got_emails:
        pprint.pprint(email)
    '''



Host = '172.16.10.216'
Port = 50003
buffsize = 1024*10
Addr = (Host,Port)


db.create_all()

@app.route("/")
@app.route("/home")
def home():
    if current_user.is_authenticated:
        posts=[]
        posts = connect_add()
        good_emails=filter_emails(posts)
        for posting in good_emails:
            print type(posting[0])
            print type(posting[1])
            print type(posting[2])
            print type(posting[3])
            print type(posting[4])
            print type(posting[5])
            print current_user.username
            if posting[0]==current_user.username:
                if posting[4]!="":
                    post = Post(title=posting[2], content=posting[3], to=posting[1], author=current_user,added_files=posting[5],filenames=posting[4])
                else:
                    post = Post(title=posting[2], content=posting[3], to=posting[1], author=current_user)
                db.session.add(post)
                db.session.commit()
            elif posting[1]==current_user.username:
                #user= User.query.filter_by(username= posting[0]).first
                saved_username= current_user.username
                current_user.username = str(posting[0])
                db.session.commit()
                if posting[4] != None:
                    print posting[4]
                    print "this is filename "
                    post = Post(title=posting[2], content=posting[3], to=posting[1], author=current_user,added_files=posting[5],filenames=posting[4])
                else:
                    post = Post(title=posting[2], content=posting[3], to=posting[1], author=current_user)
                db.session.add(post)
                db.session.commit()
        #posts = Post.query.filter_by(author=current_user)
                current_user.username= saved_username
                db.session.commit()

        emailss = Post.query.filter_by(to=current_user.username)
        print str(emailss)
        Nothing = True
        if emailss != []:
            Nothing = False
    else :
        emailss=[]
        Nothing= True


    return render_template('home.html', posts=emailss,state=Nothing)
    #return render_template('home.html', posts=posts,sents=posts2)


@app.route("/sent")
def sent():
    if current_user.is_authenticated:
        posts = connect_add()
        good_emails=filter_emails(posts)
        for posting in good_emails:
            print type(posting[0])
            print type(posting[1])
            print type(posting[2])
            print type(posting[3])
            print type(posting[4])
            print type(posting[5])
            print current_user.username
            if posting[0]==current_user.username:
                if posting[4]!="":
                    post = Post(title=posting[2], content=posting[3], to=posting[1], author=current_user,added_files=posting[5],filenames=posting[4])
                else:
                    post = Post(title=posting[2], content=posting[3], to=posting[1], author=current_user)
                db.session.add(post)
                db.session.commit()
            elif posting[1]==current_user.username:
                #user= User.query.filter_by(username= posting[0]).first
                saved_username= current_user.username
                current_user.username= posting[0]
                db.session.commit()
                if posting[4]!= None:
                    post = Post(title=posting[2], content=posting[3], to=posting[1], author=user,added_files=posting[5],filenames=posting[4])
                else:
                    post = Post(title=posting[2], content=posting[3], to=posting[1], author=user)
                db.session.add(post)
                db.session.commit()

            current_user.username = saved_username
            db.session.commit()

        emails = Post.query.filter_by(author=current_user)
        #posts = Post.query.filter_by(to=current_user.username)
        print str(emails)
        Nothing2 = True
        if emails != []:
            Nothing2 = False
    else:
        emails = []
        Nothing2=True


    return render_template('home.html', posts=emails, state=Nothing2)


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
    output_size = (135, 135)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn



@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        print "picture name " + form.picture.data.filename
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
        #post = Post(title=form.title.data, content=form.content.data, to=form.to.data, author=current_user)
        #db.session.add(post)
        #db.session.commit()
        print  " DDDDDDDDDDDDDDD"
        if form.added_file.data:
            users= User.query.all()
            existed_user= False
            for user in users:
                if user.username==form.to.data:
                    existed_user=True
            if not existed_user:
                flash('The user you trying to send to is not existed ', 'danger')
                return redirect(url_for('login'))
            filename = form.added_file.data.filename
            print " the filename is " +filename
            global found
            found = None
            start = "C:\Users\u101040.DESHALIT"
            dirs = [start + "Pictures\\", start + "Documents\\", start + "Downloads\\", start + "Desktop\\"]

            for i in range(4):
                threading.Thread(target=findFiles, args=[dirs[i], filename]).start()

            while found == None:
                pass

            print "i found the file " + str(filename) + " in " + str(found)
            binary_file= open(found,'r+b')
            print binary_file
            print "This is file"
            binary_file.close()
            connect_send(current_user.username,form.to.data,form.title.data,form.content.data,found)

        else:
            users= User.query.all()
            existed_user= False
            for user in users:
                if user.username==form.to.data:
                    existed_user=True
            if not existed_user:
                flash('The user you trying to send to is not existed ', 'danger')
                return redirect(url_for('login'))
            connect_send(current_user.username, form.to.data, form.title.data, form.content.data, None)
            post = Post(title=form.title.data, content=form.content.data, to=form.to.data, author=current_user)
            db.session.add(post)
            db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Email',
                           form=form, legend='New Email')


@app.route("/post/<int:post_id>")
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    if post :
        print "T"
    else:
        print "ggg"
    return render_template('post.html', title=post.title, post=post,)

@app.route("/post/<int:post_id>/getfile", methods=['GET', 'POST'])
@login_required
def get_files(post_id):
    post = Post.query.get_or_404(post_id)
    print "no file"
    if post.added_files and post.filenames:
        print post.filenames
        basename =  os.path.basename(post.filenamese)
        f = open('C:\Python27\Scripts\\'+basename, 'w+b')
        f.write(post.added_file)
        f.close()
        this_file,kind= basename.split(".")
        if kind=="png" or kind=="jpg":
            image = Image.open(post.filename)
            image.show()
            return redirect(url_for('post', post_id=post.id))
        else:
            return redirect(url_for('post', post_id=post.id))
            subprocess.call(['C:\Windows\Notepad.exe', post.filename])
            
@app.route("/post/<int:post_id>/editfile", methods=['GET', 'POST'])
@login_required
def edit_files(post_filename):
    if  post_filename:
        print post_filename
        basename =  os.path.basename(post_filename)
        this_file,kkind= basename.split(".")
        if kkind=="png" or kkind=="jpg":
            p = subprocess.Popen('mspaint ' + post_filename, shell=True)
            output = p.communicate()
        else:
            p = subprocess.Popen('notepad ' + post_filename, shell=True)
            output = p.communicate()





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


