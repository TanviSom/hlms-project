from flask import Flask, render_template, url_for, request, redirect, session
from flask_mysqldb import MySQL
from classes import Account
from datetime import timedelta
import socket

app = Flask(__name__)
app.config['SECRET_KEY'] = 'skdjhfskjdhf skdfjh sdkjfh'

# MySQL configure
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_ID'] = ''
app.config['MYSQL_DB'] = 'flask_users'

mysql = MySQL(app)

class User: 
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'
    
users = []
users.append(User(id=1, username='Anthony', password='password'))

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        pwd = request.form['password']
        print(f"Username: {username}")
        return redirect(url_for('stepverification', usr=username))
    else:
        return render_template("index.html")

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/stepverification/<usr>', methods=['GET', 'POST'])
def stepverification(usr):
    return render_template('stepverification.html', usr=usr)

if __name__ == "__main__":
    app.run(debug=True)
