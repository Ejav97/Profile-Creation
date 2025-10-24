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
   email = db.Column(db.String(100), nullable = False, unique=True)
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
           error = "An error occurred while saving your profile. Please try again."
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

@app.route('/admin/delete_free_users', methods=['POST'])
def delete_free_users():
    try:
        num_deleted = Account.query.filter_by(acc_type='Free').delete()
        db.session.commit()
    except Exception as error:
        db.session.rollback()
        print(f"Error occurred while deleting free user accounts: {error}")
        return render_template('admin_accounts.html', error=error)

    return redirect(url_for('admin_accounts'))

@app.route('/admin/update_acc_type/<int:user_id>', methods=['POST'])
def update_acc_type(user_id):
    user = Account.query.get_or_404(user_id)
    new_type = request.form.get('acc_type', '').strip()

    if not new_type:
        return redirect(url_for('admin_accounts'))

    try:
        user.acc_type = new_type
        db.session.commit()
        print(f"Updated {user.email} to {new_type}")
    except Exception as e:
        db.session.rollback()
        print(f"Error updating account type: {e}")

    return redirect(url_for('admin_accounts'))
 
