from flask import render_template, url_for, jsonify, abort
from flask.helpers import flash
from flask_login.utils import login_required
from app import app
from app.forms import LoginForm, TodolistForm, ContactForm
from flask import redirect
from app.models import User,  Contact
from flask_login import login_user
from flask_login import current_user
from flask_login import logout_user
from flask import request
from werkzeug.urls import url_parse
from app.models import Todolist
from app.forms import RegistrationForm

import os
from app import db
from werkzeug.security import check_password_hash

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = current_user
    return render_template('todolist/home.html', title='Trang chủ',user=user)

@app.route('/')
@app.route('/blog')
@login_required
def blog():
    user = current_user
    return render_template('todolist/blog.html', title='Blogs',user=user)

@app.route('/')
@app.route('/home')
@login_required
def home():
    user = current_user
    return render_template('todolist/home.html', title='Home',user=user)

@app.route('/')
@app.route('/contact')
@login_required
def contact():
    user = current_user
    return render_template('todolist/contact.html', title='Contact',user=user)

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect('index')
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.username.data).first()
        if user is not None:
            password_ok = check_password_hash(user.password, form.password.data)
        
        if user is None or not password_ok:
            flash('Invalid username or password:' + form.password.data)
            return redirect('/login')
        
        flash('Login of user {}'.format(form.username.data))
        login_user(user)
        next_page = request.args.get('next')
        
        if next_page is not None:
            flash('Next page is: ' + next_page)
            if url_parse(next_page).netloc != '':
                flash('netloc: ' + url_parse(next_page).netloc)
                next_page = '/index'
        else:
            next_page = '/index'
        return redirect(next_page)
    return render_template('user/login.html', form = form )

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/index')
    form = RegistrationForm()
    if form.validate_on_submit():
            user_check = User.query.filter_by(username=form.username.data).first()
            if user_check is not None:
               user_ok =  user_check.username == form.username.data
               flash('Tên tài khoản đã tồn tại!!!')
               return redirect('/register')
            if user_check is None:
                user = User(username=form.username.data, password = form.password.data)
                db.session.add(user)
                db.session.commit()
                flash('Đăng kí thành công')
                return redirect('/login')
    return render_template('user/register.html', title='Register', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('index')

@app.route('/todolists')
@login_required
def todolist_list():
    appts = (db.session.query(Todolist)
             .filter_by(user_id=current_user.id)
             .order_by(Todolist.start.asc()).all())
    return render_template('todolist/index.html', appts=appts)

@app.route('/todolists/create/', methods=['GET', 'POST'])
@login_required
def todolist_create():
    form = TodolistForm()
    if form.validate_on_submit():
        appt = Todolist(user_id=current_user.id, title = form.title.data, start=form.start.data, end=form.end.data,location=form.location.data)
        db.session.add(appt)
        db.session.commit()
        return redirect(url_for('todolist_list'))
    return render_template('todolist/create.html', form=form)

@app.route('/todolists/contact/', methods=['GET', 'POST'])
@login_required
def todolist_contact():
    form = ContactForm()
    if form.validate_on_submit():
        appt = Contact(id=current_user.id, name = form.name.data,
                email=form.email.data, phone=form.phone.data,
                subject=form.subject.data, message=form.message.data)
        db.session.add(appt)
        db.session.commit()
        return redirect(url_for('todolist_list'))
    return render_template('todolist/contact.html', form=form) 

@app.route('/todolists/<int:todolist_id>/edit/', methods=['GET', 'POST'])
@login_required
def todolist_edit(todolist_id):
    appt = db.session.query(Todolist).get(todolist_id)
    form = TodolistForm()
    if request.method == 'GET':
        form.title.data = appt.title
        form.start.data = appt.start
        form.end.data = appt.end
        form.location.data = appt.location
    
    if form.validate_on_submit():
        appt.title = form.title.data
        appt.start = form.start.data
        appt.end = form.end.data
        appt.location = form.location.data
        db.session.add(appt)
        db.session.commit()
        return redirect(url_for('todolist_list', todolist_id=appt.id))
    return render_template('todolist/edit.html', form=form)


@app.route('/todolists/<int:todolist_id>/delete/', methods=['GET'])
@login_required
def todolist_delete(todolist_id):
    appt = db.session.query(Todolist).get(todolist_id)
    if appt is None:
        flash('todolists not found')
        return redirect('/todolists')
    if appt.user_id != current_user.id:
        flash('todolists')
        return redirect('/todolists')
    db.session.delete(appt)
    db.session.commit()
    return redirect('/todolists')


