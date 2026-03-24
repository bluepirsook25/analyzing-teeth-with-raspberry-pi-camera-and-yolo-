"""
website/app.py  ──  Flask booking website
Run from the dental_pc/ root:
    cd website && python app.py
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from flask import Flask, render_template, request, redirect, url_for, session
import pymysql
import config

app = Flask(__name__)
app.secret_key = config.FLASK_SECRET


def _get_db():
    return pymysql.connect(
        host=config.DB_HOST,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor,
    )


# ── Routes ────────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        if username == config.VALID_USER and password == config.VALID_PASS:
            session['user'] = username
            return redirect(url_for('dentists'))
        error = "Invalid username or date of birth."
    return render_template('login.html', error=error)


@app.route('/dentists')
def dentists():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('doctors.html')


@app.route('/book', methods=['POST'])
def book():
    if 'user' not in session:
        return redirect(url_for('login'))
    dentist = request.form.get('dentist', 'Unknown')
    date    = request.form.get('date', '')
    try:
        conn   = _get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO appointments (dentist_name, appointment_time) VALUES (%s, %s)",
            (dentist, date),
        )
        conn.commit()
        conn.close()
    except Exception as exc:
        return f"<h2>DB Error: {exc}</h2>", 500

    return render_template('confirmation.html', dentist=dentist, date=date)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
