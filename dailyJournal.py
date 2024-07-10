import sqlite3
from datetime import datetime

import google.generativeai as genai
import sqlite3
import os

genai.configure(api_key=os.environ["API_KEY"])
model = genai.GenerativeModel('gemini-pro')


def create_connection(db_file):
	"""Create a database connection to the SQLite database."""
	conn = None
	try:
		conn = sqlite3.connect(db_file)
		return conn
	except sqlite3.Error as e:
		print(e)
	return conn


def create_table(conn):
	"""Create a table to store journal entries if it doesn't exist."""
	try:
		cursor = conn.cursor()
		cursor.execute("""
            CREATE TABLE IF NOT EXISTS journal_entries (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                entry_date TEXT NOT NULL,
                entry_text TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """)
		conn.commit()
	except sqlite3.Error as e:
		print(e)


def write_entry(conn, user_id, entry_text):
	"""Write a journal entry to the database."""
	entry_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	try:
		cursor = conn.cursor()
		cursor.execute(
		    """
            INSERT INTO journal_entries (user_id, entry_date, entry_text)
            VALUES (?, ?, ?)
        """, (user_id, entry_date, entry_text))
		conn.commit()
	except sqlite3.Error as e:
		print(e)


def read_entries(conn, user_id):
	"""Read all journal entries for a specific user from the database."""
	try:
		cursor = conn.cursor()
		cursor.execute(
		    "SELECT entry_date, entry_text FROM journal_entries WHERE user_id=?",
		    (user_id, ))
		rows = cursor.fetchall()
		for row in rows:
			print(f"Date: {row[0]}\nEntry: {row[1]}\n")
	except sqlite3.Error as e:
		print(e)


def main():
	database = "databases/users.db"
	conn = create_connection(database)
	if conn is not None:
		create_table(conn)
	else:
		print("Error: Could not create database connection.")

	user_id = 1  # You can set the user_id dynamically based on authentication

	while True:
		print("\nDaily Journal Menu:")
		print("1. Write Journal Entry")
		print("2. Read Previous Entries")
		print("3. Exit")
		choice = input("Enter your choice: ")

		if choice == '1':
			entry_text = input("Enter your journal entry for today: ")
			try:
				response = model.generate_content(
				    f"If {entry_text} is considered bad or vulgur, output the word 'flagged'. If not, out the word 'pass'."
				)
				print(response.text)
			except:
				print("flagged")
			write_entry(conn, user_id, entry_text)

			print("Journal entry added successfully.")
		elif choice == '2':
			print("Previous Entries:")
			read_entries(conn, user_id)
		elif choice == '3':
			print("Exiting...")
			conn.close()
			break
		else:
			print("Invalid choice. Please enter a valid option.")


if __name__ == "__main__":
	main()
