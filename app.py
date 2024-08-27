from flask import Flask, render_template, url_for, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import socket
from flask_mail import Mail, Message
import random
import os

def generate_otp(length=4):
    otp = ''.join([str(random.randint(0, 9)) for _ in range(length)])
    return otp

app = Flask(__name__)
mail = Mail(app)
app.secret_key = "your secret key"
app.config['SECRET_KEY'] = 'skdjhfskjdhf skdfjh sdkjfh'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'homeloanmanagementsystemhmls@gmail.com'
app.config['MAIL_PASSWORD'] = 'Homeloan'
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False

mail = Mail(app)


db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    Email = db.Column(db.String(50), unique= True, nullable= False)
    password_hash = db.Column(db.String(150), nullable= False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash, password)




@app.route('/', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(Email=email).first()
        if user and user.check_password(password):
            session['username'] = email 
            return redirect(url_for('stepverification', usr=email))
        else:
            return render_template("index.html", error="Invalid credentials.")
    return render_template("index.html")



@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/password')
def password():
    return render_template('password.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            return render_template("signup.html", error="Please provide both email and password.")

        user = User.query.filter_by(Email=email).first()
        if user:
            return render_template("signup.html", error="User already exists!")
        else:
            new_user = User(Email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = email
            return redirect(url_for('dashboard'))

    return render_template('signup.html')


@app.route('/stepverification/<usr>', methods=['GET', 'POST'])
def stepverification(usr):
    if request.method == "POST":
        entered_otp = request.form.get("otp")
        if entered_otp == session.get('otp'):
            return redirect(url_for('dashboard'))
        else:
            return render_template('stepverification.html', usr=usr, error="Invalid OTP.")
    
    otp = generate_otp()
    session['otp'] = otp

    # Send the OTP via email
    msg = Message('Your OTP Code', sender='homeloanmanagementsystemhmls@gmail.com', recipients=[usr])
    msg.body = f'Your OTP code is {otp}. Please enter it to verify your account.'
    mail.send(msg)

    return render_template('stepverification.html', usr=usr)

@app.route('/dashboard')
def dashboard():
    if "username" in session:
        return render_template("dashboard.html", username=session['username'])
    return redirect(url_for('login'))

@app.route("/logout")
def logout():
    session.pop('username', None)
    return render_template("index.html")

@app.route("/result", methods= ['POST', 'GET'])
def result():
    if request.method == "POST":
        email = request.form.get("Email")
        subject = request.form.get("Subject")
        msg = Message(subject, sender='homeloanmanagementsystemhmls@gmail.com', recipients=[email])
        msg.body = "Cool email bro"
        mail.send(msg)
        return render_template("result.html", result="Success!")
    else:
        return render_template("result.html", result="Failure.")
    
@app.route("/comparison")
def comparison():
    return render_template('comparison.html')

@app.route("/ammortisation")
def ammortisation():
    return render_template('ammortisation.html')

@app.route("/share")
def share():
    return render_template('share.html')    


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
