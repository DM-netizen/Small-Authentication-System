from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField
from wtforms.validators import InputRequired, Email, Length, NumberRange, Optional
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Iwilldothis'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/user/OneDrive/Documents/Small-Authentication-System/database.db'
Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer,  primary_key=True)
    phn = db.Column(db.Integer,  unique=True)
    username = db.Column(db.String(15) , unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class ForgotForm(FlaskForm):
    email = StringField('email' , validators=[InputRequired(), Email(message='Invalid Email'), Length(max=50)])
    phn = IntegerField('Phone Number', validators=[InputRequired(), NumberRange(min=1000000000, max=9999999999, message='Phone number must be of 10 digits')])
    password = StringField('Password', validators = [InputRequired(), Length(min=8, max=80)])

# class ChangeForm(FlaskForm):
#     password = StringField('Password', validators = [InputRequired(), Length(min=8, max=80)])


class LoginForm(FlaskForm):
    username = StringField('Username', validators = [Length(min=4, max=15)])
    password = StringField('Password', validators = [Length(min=8, max=80)])
    remember = BooleanField('Remember me')
    forgot_password = BooleanField('Forgot your password? Click Here')

class RegisterForm(FlaskForm):
    email = StringField('Email' , validators=[InputRequired(), Email(message='Invalid Email'), Length(max=50)])
    username = StringField('Username', validators = [InputRequired(), Length(min=4, max=15)])
    password = StringField('Password', validators = [InputRequired(), Length(min=8, max=80)])
    phn = IntegerField('Phone Number', validators=[InputRequired(), NumberRange(min=1000000000, max=9999999999, message='Phone number must be of 10 digits')])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login' , methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.forgot_password.data == True:
        form.username.validators = [Optional()]
        form.password.validators = [Optional()]
    else:
        form.username.validators = [InputRequired()]
        form.password.validators = [InputRequired()]
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if form.forgot_password.data == True:
            return redirect(url_for('forgot'))
        elif user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember = form.remember.data)
                return redirect(url_for("dashboard"))
            else:
                flash(f"Wrong credentials!","info")
                return redirect(url_for('login'))
    return render_template('login.html' , form=form)

@app.route('/forgot', methods=['GET','POST'])
def forgot():
    form = ForgotForm()
    if form.validate_on_submit():
        user = User.query.filter_by(phn = form.phn.data).first()
        print(user.email)
        print(form.email.data)
        if user.email == form.email.data:
            new_hashed_password = generate_password_hash(form.password.data, method="pbkdf2:sha256")
            user = User.query.filter_by(phn = user.phn).first()
            user.password = new_hashed_password        
            db.session.commit()
            flash (f"Please login again!","info")
            return redirect(url_for('login')) 
        else:
            flash(f"Wrong Email entered!")
            return redirect(url_for('forgot'))
    return render_template('forgot.html', form=form)

@app.route('/signup' , methods=['GET','POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method="pbkdf2:sha256")
        new_user = User(username = form.username.data, email = form.email.data, phn = form.phn.data, password = hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash("New user has been created!")
        login_user(new_user)
        return redirect(url_for("dashboard"))
    return render_template('signup.html' , form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html' , name= current_user.username)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)