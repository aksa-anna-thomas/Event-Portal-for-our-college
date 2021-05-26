# main python file

from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Email, Length
from wtforms import StringField, PasswordField, BooleanField
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SecretNo123!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
Bootstrap(app)
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80), username)


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')


class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(),Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])


@app.route('/')
def welcome():
    return render_template("Welcome.html")


@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if user.password == form.password.data:
                return redirect(url_for('dashboard'))
        return '<h1>Invalid Username or Password</h1>'

    return render_template("Login.html",form=form)


@app.route('/signup', methods=['GET','POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'
        new_user=User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(new_user)
        db.commit()

        return '<h1>New User has been created!Yeah</h1>'

    return render_template("Register.html",form=form)


@app.route('/profile')
def profile():
    return render_template("Profile.html")


@app.route('/dashboard')
def dashboard():
    return render_template('Dashboard.html')


if __name__ == '__main__':
    app.run(debug = True)

