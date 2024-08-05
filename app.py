from flask import Flask, render_template, url_for, request, redirect, flash, session 
from classes import Account
from datetime import timedelta
import socket



app = Flask(__name__)
app.config['SECRET_KEY'] = 'skdjhfskjdhf skdfjh sdkjfh'

class User: 
    def __init__(self, id, username, password):
        self.id= id
        self.username = username
        self.password = password

    def __repr(self):
        return f'<User: {self.username}>'
    
users = []
users.append(User(id=1, username='Anthony', password='password'))



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']

        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('profile'))
        
        return redirect(url_for('login'))

    return render_template('index.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/stepverification')
def stepvarification():
    return render_template('stepverification.html')

if __name__ == "__main__":
    app.run(debug=True)
