from flask import Flask, render_template, request, session, redirect, url_for
from dotenv import load_dotenv
import psycopg2
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ['AQUATRACK_SECRET_KEY']

# Database connection details
db_host = os.environ['AQUATRACK_DB_HOST']
db_port = os.environ['AQUATRACK_DB_PORT']
db_username = os.environ['AQUATRACK_DB_USERNAME']
db_password = os.environ['AQUATRACK_DB_PASSWORD']
db_name = os.environ['AQUATRACK_DB_NAME']

# Function to establish a database connection
def connect_to_db():
    conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        user=db_username,
        password=db_password,
        database=db_name
    )
    return conn

# Function to validate user credentials against the database
def validate_credentials(username, password):
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user is not None

# Function to convert water consumption to liters
def convert_to_liters(water_consumption):
    if water_consumption >= 1000:
        return f'{water_consumption / 1000:.3f}L'
    else:
        return f'{water_consumption}ml'

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if validate_credentials(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    else:
        return "Invalid username or password"

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        username = session['username']
        conn = connect_to_db()
        cursor = conn.cursor()
        query = "SELECT water_consumption FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        water_consumption = cursor.fetchone()[0]
        cursor.close()
        conn.close()

        return render_template('dashboard.html', convert_to_liters=convert_to_liters, water_consumption=water_consumption)
    else:
        return redirect(url_for('index'))


@app.route('/add_water', methods=['POST'])
def add_water():
    if 'username' in session:
        username = session['username']
        amount = int(request.form['amount'])
        conn = connect_to_db()
        cursor = conn.cursor()
        update_query = "UPDATE users SET water_consumption = water_consumption + %s WHERE username = %s"
        cursor.execute(update_query, (amount, username))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('index'))

@app.route('/remove_water', methods=['POST'])
def remove_water():
    if 'username' in session:
        username = session['username']
        amount = int(request.form['amount'])
        conn = connect_to_db()
        cursor = conn.cursor()

        # Retrieve current water consumption
        query = "SELECT water_consumption FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        water_consumption = cursor.fetchone()[0]

        # Check if removing the specified amount would result in a negative value
        if amount <= water_consumption:
            # Update the water consumption
            update_query = "UPDATE users SET water_consumption = water_consumption - %s WHERE username = %s"
            cursor.execute(update_query, (amount, username))
            conn.commit()
        else:
            # Set an error message if the removal amount is greater than the current water consumption
            message = "Invalid amount. You cannot remove more water than you have consumed."
            return render_template('dashboard.html', convert_to_liters=convert_to_liters, water_consumption=water_consumption, message=message)

        cursor.close()
        conn.close()
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('index'))

@app.route('/reset_water', methods=['POST'])
def reset_water():
    if 'username' in session:
        username = session['username']
        conn = connect_to_db()
        cursor = conn.cursor()

        # Reset the water consumption to 0
        update_query = "UPDATE users SET water_consumption = 0 WHERE username = %s"
        cursor.execute(update_query, (username,))
        conn.commit()

        cursor.close()
        conn.close()
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('index'))

@app.route('/disconnect', methods=['POST'])
def disconnect():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
