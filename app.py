from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)
app.secret_key = 'top-secret'

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
        notifications = request.form.get('notificatons') == "yes"

        if not name or not email or not password or not acctype:
            error = "Please fill in all the required fields."
            return render_template('signUp.html')
        
        return render_template(
            'successCreation.html',
            name = name,
            email = email,
            password = password,
            acctype = acctype,
            notifications = notifications
        )
    
    return render_template('signUp.html')