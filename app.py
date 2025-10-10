from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

app = Flask(__name__)

app.secret_key = 'top-secret'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///accountlists.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db =SQLAlchemy(app)

class Account(db.Model):
   id = db.Column(db.Integer, primary_key = True)
   name = db.Column(db.String(100), nullable = False)
   email = db.Column(db.String(100), nullable = False)
   password = db.Column(db.String(100), nullable = False)
   acc_type = db.Column(db.String(10), nullable = False)
   notifications = db.Column(db.Boolean, default = False)
   created_at = db.Column(db.DateTime, default = datetime.now(timezone.utc))

with app.app_context():
   db.create_all()

@app.route('/')
def index():
    return redirect(url_for('signup'))

@app.route('/signUp', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        acctype = request.form.get('acctype', '').strip()
        notifications = request.form.get('notifications') == "yes"
        
        if not name or not email or not password or not acctype:
            error = "Please fill in all the required fields."
            return render_template('signUp.html', error=error)
        
        try:
           new_account = Account(
              name = name,
              email = email,
              password = password,
              acc_type = acctype,
              notifications = notifications
           )
           db.session.add(new_account)
           db.session.commit()
        except Exception as e:
           db.session.rollback()
           error = "An error ocurred while saving your profile. Please try again."
           return render_template('signUp.html', error = error)

        return render_template(
            'successCreation.html',
            name = name,
            email = email,
            password = password,
            acctype = acctype,
            notifications = notifications
        )
    
    return render_template('signUp.html')

@app.route('/account', methods=['GET', 'POST'])
def account():
   
   if request.method == 'POST':
    return redirect(url_for('account')) 
    
   return render_template('account.html')

@app.route('/admin/accounts')
def admin_accounts():
    accounts = Account.query.all()
    return render_template('admin_accounts.html', accounts=accounts)