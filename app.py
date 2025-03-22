from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, session
from flask_bcrypt import Bcrypt
import mysql.connector
from functools import wraps
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'supersecretkey')  # Change this to a secure secret key
bcrypt = Bcrypt(app)

# ✅ Connect to MySQL Database using environment variables
db = mysql.connector.connect(
    host=os.environ.get('DB_HOST', 'localhost'),
    user=os.environ.get('DB_USER', 'root'),
    password=os.environ.get('DB_PASSWORD', 'prachi'),
    database=os.environ.get('DB_NAME', 'dashboard_db')
)

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        
        if user and bcrypt.check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        cursor = db.cursor(dictionary=True)
        
        # Check if email already exists
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            flash('Email already registered', 'danger')
            cursor.close()
            return render_template('signup.html')
        
        # Hash password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        # Insert new user
        cursor.execute("""
            INSERT INTO users (username, email, password)
            VALUES (%s, %s, %s)
        """, (username, email, hashed_password))
        
        db.commit()
        cursor.close()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    return render_template('index.html')  # ✅ Serves the HTML page

@app.route('/profile')
@login_required
def profile():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE id = %s", (session['user_id'],))
    user = cursor.fetchone()
    cursor.close()
    return render_template('profile.html', user=user)

@app.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    username = request.form.get('username')
    bio = request.form.get('bio')
    
    cursor = db.cursor()
    cursor.execute("""
        UPDATE users 
        SET username = %s, bio = %s 
        WHERE id = %s
    """, (username, bio, session['user_id']))
    db.commit()
    cursor.close()
    
    session['username'] = username
    flash('Profile updated successfully!', 'success')
    return redirect(url_for('profile'))

@app.route('/update_password', methods=['POST'])
@login_required
def update_password():
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT password FROM users WHERE id = %s", (session['user_id'],))
    user = cursor.fetchone()
    
    if not bcrypt.check_password_hash(user['password'], current_password):
        flash('Current password is incorrect', 'danger')
        return redirect(url_for('profile'))
    
    if new_password != confirm_password:
        flash('New passwords do not match', 'danger')
        return redirect(url_for('profile'))
    
    hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
    cursor.execute("UPDATE users SET password = %s WHERE id = %s", (hashed_password, session['user_id']))
    db.commit()
    cursor.close()
    
    flash('Password updated successfully!', 'success')
    return redirect(url_for('profile'))

@app.route('/update_preferences', methods=['POST'])
@login_required
def update_preferences():
    default_theme = request.form.get('default_theme')
    
    cursor = db.cursor()
    cursor.execute("UPDATE users SET default_theme = %s WHERE id = %s", (default_theme, session['user_id']))
    db.commit()
    cursor.close()
    
    flash('Preferences updated successfully!', 'success')
    return redirect(url_for('profile'))

@app.route('/get-data')
@login_required
def get_data():
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT end_year, intensity, sector, likelihood, country, pestle,
               relevance, topic, region, insight, title, source 
        FROM insights
    """)
    data = cursor.fetchall()
    # Debug: Print first few records' source values
    print("First 5 source values:", [row.get('source', '') for row in data[:5]])
    cursor.close()
    return jsonify(data)  # ✅ Sends JSON data


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
