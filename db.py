import sqlite3

def init_db_users():
	try:
		conn = sqlite3.connect('users.db')
		c = conn.cursor()

		c.execute('''CREATE TABLE IF NOT EXISTS users
					(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT, email TEXT, phone TEXT, is_doctor INTEGER, flagged INTEGER, entry_text TEXT, entry_date TEXT)''')

		conn.commit()
		conn.close()
	except Exception as e:
		print(e)

def init_db_appointments():
	try:
		conn = sqlite3.connect('appointments.db')
		c = conn.cursor()

		c.execute('''CREATE TABLE IF NOT EXISTS appointments
					(id INTEGER PRIMARY KEY AUTOINCREMENT, user INTEGER, date TEXT, time TEXT, location TEXT, notes TEXT, email TEXT)''')

		conn.commit()
		conn.close()
	except Exception as e:
		print(e)

def test():
	try:
		# Connect to the appointments database
		conn = sqlite3.connect('databases/appointments.db')
		c = conn.cursor()

		# Fetch all appointments from the appointments table
		c.execute("SELECT * FROM appointments")
		appointments = c.fetchall()

		# Print the appointments
		if not appointments:
			print("No appointments found.")
		else:
			print("Appointments:")
			for appointment in appointments:
				print(appointment)

		conn.close()
	except Exception as e:
		print("An error occurred:", e)

# Call the function to check appointments
init_db_appointments()


def init_db_doctor():
	try:
		conn = sqlite3.connect('doctor.db')
		c = conn.cursor()

		c.execute('''CREATE TABLE IF NOT EXISTS doctor
					(id INTEGER PRIMARY KEY AUTOINCREMENT,
					 email TEXT,
					 age INTEGER,
					 degree TEXT,
					 specialty TEXT,
					 description TEXT)''')

		conn.commit()
		conn.close()
	except Exception as e:
		print(e)

import sqlite3

def get_username_by_email(email):
	try:
		conn = sqlite3.connect('users.db')
		c = conn.cursor()

		# Execute a SELECT query to retrieve the username based on the email
		c.execute("SELECT username FROM users WHERE email=?", (email,))
		result = c.fetchone()  # Fetch the first result

		conn.close()

		if result:
			return result[0]  # Return the username if found
		else:
			return None  # Return None if no user found with the provided email
	except Exception as e:
		print(e)
		return None


