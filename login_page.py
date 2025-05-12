from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import hashlib

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Important for session management

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hash_password(password)

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, hashed_password)).fetchone()
        conn.close()

        if user:
            session['username'] = user['username']
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid username or password'

    return render_template('login.html', error=error)

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hash_password(password)

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

        if user is None:
            conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        else:
            error = "Username already exists."
    return render_template('register.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)