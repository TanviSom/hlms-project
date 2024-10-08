from flask import Flask, render_template, url_for, request, redirect, session, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import random
from flask_mail import Mail, Message


app = Flask(__name__)
app.secret_key = "your secret key"
app.config['SECRET_KEY'] = 'skdjhfskjdhf skdfjh sdkjfh'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'homeloanmanagementsystemhmls@gmail.com'
app.config['MAIL_PASSWORD'] = 'Homeloan'
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False

mail = Mail(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


def generate_otp(length=4):
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])

class LoanDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Link to User
    loan_amount = db.Column(db.Float, nullable=False)
    tenure = db.Column(db.Integer, nullable=False)
    tenure_type = db.Column(db.String(10), nullable=False)  # 'months' or 'years'
    interest_rate = db.Column(db.Float, nullable=False)

    user = db.relationship('User', backref='loans')


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    phone_number = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@app.route('/', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['username'] = email
            return redirect(url_for('stepverification', usr=email))
        else:
            return render_template("index.html", error="Invalid credentials.")
    return render_template("index.html")


@app.route('/profile', methods=["GET", "POST"])
def profile():
    # Check if the user is logged in
    if "username" not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in

    user = User.query.filter_by(email=session['username']).first()
    
    if not user:
        session.pop('username', None)
        return redirect(url_for('login'))  # Additional check to handle missing user

    if request.method == "POST":
        # Extract form data
        new_email = request.form.get('email', user.email)

        # Check if the new email is already in use by another user
        if new_email != user.email and User.query.filter_by(email=new_email).first():
            flash('Email is already in use by another account.', 'danger')
            return redirect(url_for('profile'))

        # Update user details
        user.first_name = request.form.get('first_name', user.first_name)
        user.last_name = request.form.get('last_name', user.last_name)
        user.email = new_email
        user.phone_number = request.form.get('phone_number', user.phone_number)

        # Save changes
        db.session.commit()
        flash('Profile updated successfully.', 'success')
        return redirect(url_for('profile'))

    full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()
    return render_template('profile.html', user=user, username=full_name)

@app.route('/password', methods=['GET', 'POST'])
def password():
    if "username" not in session:
        return redirect(url_for('login'))

    user = User.query.filter_by(email=session['username']).first()
    
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_new_password = request.form['confirm_new_password']

        if not user.check_password(current_password):
            flash('Current password is incorrect.', 'danger')
            return redirect(url_for('password'))

        if new_password != confirm_new_password:
            flash('New passwords do not match.', 'danger')
            return redirect(url_for('password'))

        user.set_password(new_password)
        db.session.commit()
        flash('Password updated successfully.', 'success')
        return redirect(url_for('dashboard'))

    full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()
    return render_template('password.html', username=full_name)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').lower()

    # Define the available pages and their names
    pages = {
        'dashboard': 'dashboard',
        'profile': 'profile',
        'password': 'password',
        'logout': 'logout',
        'comparison': 'comparison',
        'amortisation': 'ammortisation',
        'share': 'share'
    }

    # Search logic: redirect to the matching page
    for page_name, endpoint in pages.items():
        if query in page_name:
            return redirect(url_for(endpoint))

    # If no match is found, render a search results page or show a message
    flash('No matching pages found.', 'info')
    return redirect(url_for('dashboard'))  # Default redirect, can be adjusted as needed




@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get the form data
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        
        # Split the name into first and last names
        name_parts = name.split(' ', 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ''
        
        # Create new user instance with the correct email field
        new_user = User(first_name=first_name, last_name=last_name, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('dashboard'))
    
    return render_template('signup.html')


@app.route('/stepverification/<usr>', methods=['GET', 'POST'])
def stepverification(usr):
    return render_template('stepverification.html', usr=usr)


@app.route('/dashboard', methods=["GET", "POST"])
def dashboard():
    if "username" not in session:
        return redirect(url_for('login'))  # If user is not logged in, redirect to login

    user = User.query.filter_by(email=session['username']).first()

    if not user:
        session.pop('username', None)
        return redirect(url_for('login'))  # Handle case where user does not exist in DB

    loan_details = LoanDetails.query.filter_by(user_id=user.id).first()

    if request.method == "POST":
        # Retrieve form data
        loan_amount = request.form.get('loan_amount')
        tenure = request.form.get('tenure')
        tenure_type = request.form.get('tenure_type')
        interest_rate = request.form.get('interest_rate')

        # Validate and convert form data
        try:
            loan_amount = float(loan_amount)
        except ValueError:
            flash('Loan amount must be a number.', 'danger')
            return render_template("dashboard.html", user=user, loan_details=loan_details)

        try:
            tenure = int(tenure)
        except ValueError:
            flash('Tenure must be an integer.', 'danger')
            return render_template("dashboard.html", user=user, loan_details=loan_details)

        try:
            interest_rate = float(interest_rate)
        except ValueError:
            flash('Interest rate must be a valid number.', 'danger')
            return render_template("dashboard.html", user=user, loan_details=loan_details)

        # Save or update loan details in the database
        if loan_details:
            # Update existing loan details
            loan_details.loan_amount = loan_amount
            loan_details.tenure = tenure
            loan_details.tenure_type = tenure_type
            loan_details.interest_rate = interest_rate
        else:
            # Create new loan details entry
            loan_details = LoanDetails(
                user_id=user.id,
                loan_amount=loan_amount,
                tenure=tenure,
                tenure_type=tenure_type,
                interest_rate=interest_rate
            )
            db.session.add(loan_details)

        db.session.commit()
        flash('Loan details saved successfully.', 'success')

    # Fetch updated loan details to display in the dashboard
    loan_details = LoanDetails.query.filter_by(user_id=user.id).first()

    return render_template("dashboard.html", user=user, loan_details=loan_details)

@app.route("/logout")
def logout():
    session.pop('username', None)
    return render_template("index.html")


@app.route("/result", methods=['POST', 'GET'])
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

BANK_RATES = {
    "Commonwealth Bank": 3.5,
    "AMP Bank": 4.0,
    "ANZ": 3.8,
    "NAB": 3.7,
    "Bank of Queensland": 3.4,
    "Suncorp Bank": 3.9,
    "Bankwest": 3.6,
    "Bendigo Bank": 4.1,
    "Macquarie Bank": 3.9,
    "Westpac": 3.8
}



@app.route('/comparison', methods=['GET', 'POST'])
def comparison():
    selected_banks = []
    bank_rates = []
    monthly_payments = []
    best_bank_index = None

    if request.method == 'POST':
        loan_amount = float(request.form.get('loan_amount', 0))
        tenure_years = int(request.form.get('tenure', 0))
        tenure_months = tenure_years * 12

        for i in range(4):
            bank_name = request.form.get(f'bank{i}')
            if bank_name:
                rate = BANK_RATES.get(bank_name, 0)
                if loan_amount > 0 and tenure_months > 0 and rate > 0:
                    selected_banks.append(bank_name)
                    bank_rates.append(rate)
                    monthly_payment = calculate_monthly_payment(loan_amount, rate, tenure_months)
                    monthly_payments.append(monthly_payment)
                else:
                    selected_banks.append(None)
                    bank_rates.append(None)
                    monthly_payments.append(None)

        if monthly_payments and any(monthly_payments):
            best_bank_index = monthly_payments.index(min(filter(None, monthly_payments)))

    return render_template('comparison.html', selected_banks=selected_banks, bank_rates=bank_rates, monthly_payments=monthly_payments, best_bank_index=best_bank_index)

def calculate_monthly_payment(loan_amount, annual_rate, tenure_months):
    if tenure_months == 0:
        return 0  # or handle this case as you see fit
    
    monthly_rate = annual_rate / 12 / 100
    if monthly_rate == 0:  # To avoid division by zero
        return loan_amount / tenure_months
    
    return (loan_amount * monthly_rate) / (1 - (1 + monthly_rate) ** -tenure_months)


@app.route("/ammortisation", methods=["GET", "POST"])
def ammortisation():
    if request.method == "POST":
        loan_amount = float(request.form.get("loan_amount"))
        annual_rate = float(request.form.get("interest_rate"))
        tenure_months = int(request.form.get("loan_tenure"))

        # Monthly interest rate
        monthly_rate = annual_rate / 12 / 100
        # EMI formula: [P * r * (1+r)^n] / [(1+r)^n – 1]
        emi = loan_amount * monthly_rate * ((1 + monthly_rate) ** tenure_months) / ((1 + monthly_rate) ** tenure_months - 1)

        balance = loan_amount
        data = []

        for i in range(1, tenure_months + 1):
            interest = balance * monthly_rate
            principal = emi - interest
            balance -= principal
            data.append((i, f"${emi:,.2f}", f"${interest:,.2f}", f"${principal:,.2f}", f"${balance:,.2f}"))

        headings = ("Payment Number", "Payment Amount", "Interest Paid", "Principal Paid", "Remaining Balance")

        # Summary Data
        total_payment = emi * tenure_months
        total_interest = total_payment - loan_amount
        return render_template('ammortisation.html', headings=headings, data=data, emi=f"${emi:,.2f}",
                               total_interest=f"${total_interest:,.2f}", total_amount=f"${total_payment:,.2f}")

    # Default data for GET requests
    return render_template('ammortisation.html', headings=[], data=[])


@app.route("/share")
def share():
    return render_template('share.html')


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

