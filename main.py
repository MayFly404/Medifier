from flask import Flask, render_template, request, redirect, url_for, session
from db import *
from ai import *
from dailyJournal import *
import sqlite3
import os
import datetime


app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']

api_key = os.environ["API_KEY"]
model = configure_generative_model(api_key)

def authenticate_user():
	if 'user_id' not in session:
		return redirect(url_for('login'))

@app.route('/')
def index():
	is_doctor = session.get('is_doctor')
	return render_template('index.html', is_doctor=is_doctor)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']

    
    
		conn = sqlite3.connect('databases/users.db')
		c = conn.cursor()
		c.execute("SELECT * FROM users WHERE email = ?", (email,))
		user = c.fetchone()
		conn.close()

		if user and user[2] == password:
			session['user_id'] = True
			session['username'] = user[1]
			session['email'] = user[3]
			return redirect(url_for('dashboard'))
		else:
			return "Invalid email or password. Please try again."
	return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
		is_doctor = 1 if 'doctorCheck' in request.form else 0

		try:
			conn = sqlite3.connect('databases/users.db')
			c = conn.cursor()
			c.execute("INSERT INTO users (username, password, email, is_doctor) VALUES (?, ?, ?, ?)", (username, password, email, is_doctor))
			conn.commit()
			conn.close()

			if is_doctor:
				return redirect(url_for('doctor_signup'))
			else:
				return redirect(url_for('login'))
		except Exception as e:
			print(e)
			return "Error occurred while signing up."
	return render_template('signup.html')

@app.route('/logout')
def logout():
	session.pop('user_id', None)
	return redirect(url_for('index'))

def save_ticket(email, age, degree, specialty, description):
	conn = sqlite3.connect('databases/doctor.db')
	cursor = conn.cursor()
	cursor.execute(
		"INSERT INTO doctor (email, age, degree, specialty, description) VALUES (?, ?, ?, ?, ?)",
		(email, age, degree, specialty, description))
	conn.commit()
	cursor.close()
	conn.close()

@app.route('/doctor_signup', methods=['GET', 'POST'])
def doctor_signup():
	if request.method == 'POST':
		email = session['email']
		age = request.form['age']
		degree = request.form['degree']
		specialty = request.form['specialty']
		description = request.form['description']

		save_ticket(email, age, degree, specialty, description)

		session['is_doctor'] = True

		return redirect(url_for('doctor_dashboard'))

	return render_template('doctorsignup.html', description='')

@app.route('/dashboard')
def dashboard():
	authenticate_user()
	username = session.get('username')
	email = session.get('email')  # Fetch the user ID

	try:
		# Connect to the appointments database
		conn = sqlite3.connect('databases/appointments.db')
		c = conn.cursor()

		# Fetch all appointments for the logged-in user
		c.execute("SELECT * FROM appointments")
		appointments = c.fetchall()

		# Fetch doctors list from the database or any other source
		doctors = []  
		# Connect to the doctor database
		conn1 = sqlite3.connect('databases/doctor.db')
		c1 = conn1.cursor()
		c1.execute("SELECT * FROM doctor")  
		doctors = c1.fetchall()

		# Close both connections
		conn.close()
		conn1.close()

		return render_template('dashboard.html', username=username, email=email, appointments=appointments, doctors=doctors)
	except Exception as e:
		print(e)
		return "Error occurred while fetching user appointments."

@app.route('/process_ticket', methods=['POST'])
def process_ticket():
	if request.method == 'POST':
		symptoms = request.form['symptoms']
		symptoms_response = generate_symptoms_response(model, symptoms)
		doctor_note = generate_appointment(model, symptoms_response)
		doctor_type = generate_doctor(model, symptoms_response)

		doctors = []  # Fetch doctors list from the database or any other source
		# Fetch all doctors from the database
		conn = sqlite3.connect('databases/doctor.db')
		c = conn.cursor()
		c.execute("SELECT * FROM doctor")
		doctors = c.fetchall()
		conn.close()

		# Convert doctor_note to string
		doctor_note_str = str(doctor_note)

		# Insert the generated doctor note into the appointments table
		conn = sqlite3.connect('databases/appointments.db')
		c = conn.cursor()
		c.execute("INSERT INTO appointments (notes) VALUES (?)", (doctor_note.text,))
		conn.commit()
		conn.close()

		return render_template('symptoms_response.html', symptoms_response=symptoms_response.text, doctor_note=doctor_note.text, doctor_type=doctor_type.text, doctors=doctors)

@app.route('/set_appointment', methods=['POST'])
def set_appointment():
	if request.method == 'POST':
		notes = request.form['doctor_note']
		doctor_id = request.form['doctor_id']
		appointment_time = request.form['appointment_time']

		try:
			# Connect to the appointments database
			conn = sqlite3.connect('databases/appointments.db')
			c = conn.cursor()

			# Insert the appointment details into the appointments table
			c.execute("INSERT INTO appointments (time, notes, email) VALUES (?, ?, ?)",
					  (appointment_time, notes, doctor_id))

			conn.commit()  # Commit the transaction
			conn.close()   # Close the connection

			return redirect(url_for('appointment_confirmation'))
		except Exception as e:
			print(e)
			return "Error occurred while setting appointment."

	return 'Method Not Allowed'

@app.route('/appointment_confirmation')
def appointment_confirmation():
	return render_template('appointment_confirmation.html')

@app.route('/doctor_dashboard')
def doctor_dashboard():
	email = session.get('email')
	username = session.get('username')
	is_doctor = session.get('is_doctor')

	print(email, username, is_doctor)

	if is_doctor:
		conn = sqlite3.connect('databases/appointments.db')
		c = conn.cursor()

		c.execute("SELECT time, notes FROM appointments")
		entries = c.fetchall()
		conn.close()

		for entry in entries:
			print(entry)
		
		return render_template('doctor_dashboard.html', username=username, email=email, appointments=entries)
	else:
		return redirect(url_for('login'))




if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80)
