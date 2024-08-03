
# Medifier

In the Cincihacks Hackathon of 2024, our team wanted a solution to the congestion of hospitals around the world. Using nothing but our computers, blood, sweat, tears, coffee, redbull, flask, and css; we were able to champion the competition.


# Table of Contents

 - [What we are](#what-we-are)
 -  [Inspiration](#inspiration)
 - [Database](#database)
 - [Back End Stacks](#back-end-stacks)
 - [Front End Stacks](#front-end-stacks)
 - [Features](#features)

# What we are

Medifier is an AI powered medical help website that helps you potentially identify your issue, write a detailed description, list action that could be taken, and medicine. All this information would be saved, and you can schedule with a licensed doctor who will receive the information. For clarification, the AI does not diagnose you.

# Inspiration
We had read much about the hospital congestion problem. In the US, you need to wait hours  in the ER waiting room  in major cities. You could have a serious injury, but many people ahead of you are trying to see a doctor for minor issues. In the UK, there was a shortage of over 100,000 doctors during the covid era. Medifier would be able to help those with minor issues, and give priority to those who desperately need medical attention.

# Database
We had three overall .db files running on sqlite. Here is an example of how our tables would be created:
```python
#db.py

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

```

# Back End Stacks

### List of Stacks (not too impressive):
 - Flask
 - SQLite3 (i wish we used postgreSQL 😔)

<br><br>

We utilized python as our flask backend server. For our ai, we used Gemini 2.5's API. Since the main.py file is too large, the ai.py file that will be referenced.

Since we have did a good job of naming and commenting, the code should be readable, and identifying the functions should not be too difficult.

```python

# Imports from ai.py
import google.generativeai as genai
import sqlite3
import os

# global variables
genai.configure(api_key=os.environ["API_KEY"]) # replit secret api key
model = genai.GenerativeModel('gemini-pro')



def configure_generative_model(api_key):
	genai.configure(api_key=api_key)
	return genai.GenerativeModel('gemini-pro')

def generate_symptoms_response(model, symptoms):
	return model.generate_content(
		f"Given the following symptoms: {symptoms}. What are some possible medications that could be used to relieve these symptoms? If the user does not explicitly say that the symptoms are dire or anything along those lines, respond normally. If the symptoms are too dire, please tell me to contact a doctor or call the emergency number (911 in the United States). Then please tell me if the medication is safe to take. Answer as if writing a paragraph, seperate with commas, use colon, etc."
	)

def generate_appointment(model, symptoms):
	return model.generate_content(
		f"Given the following symptoms: {symptoms}. Please write a note that the doctor would read. keep it 5 sentences including possible medicaions."
	)

def generate_doctor(model, symptoms):
	return model.generate_content(
		f"Given the following symptoms: {symptoms}. Please, in one word only, no more or less, say the doctor specialty that this patient should see. An example response would be: 'General'"
	)

def generate_yes_no_response(model, yes_or_no):
	return model.generate_content(
		f"Given the following, '{yes_or_no}', do you believe I was saying yes or no? If no, please output 'no'. If yes, please output 'yes'. Saying 'y' automatically says yes, if 'n' automatically says no."
	)

def generate_appointment_scheduling_response(model, yes_no_response, symptoms, doctor_name, doctor_specializations, appointment_timings, appointment_locations):
	if yes_no_response.text == "yes":
		return model.generate_content(
			f"If I say yes, please ask which timings work for me based off the available appointments. IF I says no, then say 'I understand. If you ever change your mind, please input your symptoms and schedule an appointment.' I said {yes_no_response.text}. The doctors are {doctor_name} and their respective specializations are as follow, {doctor_specializations}. Please only list the doctors with the specializations that more directly follow the symptoms, {symptoms}. The respective appointment timings are {appointment_timings}, their respective locations is {appointment_locations}. Number ONLY the doctors whose specialization help the patient the most and also list their specialization as well, with timings and location, in numerical order in a single line. Start off saying something along the lines of 'here are all the doctors that are available for you based off your symptoms'"
		)
	else:
		return "I understand. If you ever change your mind, please input your symptoms and schedule an appointment."

def generate_confirmation_response(model, appoint_sched_response, user_sched):
	return model.generate_content(
		f"Given the following appointment timings, '{appoint_sched_response.text}', and I said '{user_sched}' create a confirmation message that the appointment was successfully scheduled."
	)

def generate_list_response(confirm_response):
	return model.generate_content(
		f"Given {confirm_response}, create a python list of the name, the time, and the location and output it."
	)

```

As shown above, each function uses `model` as a parameter, and returns `model.generate_content(...)` Shout out to google for their good documentation.

# Front End Stacks

Unlike the backend, the frontend was much easier because it did not break on us ten minutes before presentation. Without any extra yap, here are the stacks we used for our frontend:

### Stacks Used:
 - Jinja
 - Bootstrap
 - Ajax
 - PopperJS
 
 I know what you must be thinking, "why isn't there vue.js or react?" I didn't know how, and I like to compensate with my [kind of] amazing python code.

To demonstrate how we used our stacks, the prime example would be **templates/base.html** because it create a block using Jinja, and creates all the pretty designs in bootstrap.

```html
<body>
	<div class="container-flex">
		<nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
			<div class="container-fluid ms-3 me-3">
				<img style="width: 50px" src="{{ url_for('static', filename='img/MedifierLogo2.png') }}">
				<a style="text-decoration:none; font-size:20px; color:white" class="navbar-brand, days-one-regular" href="#">Medifier</a>
				<button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
					<span class="navbar-toggler-icon"></span>
				</button>
				<div style="margin-left:15px;" class="collapse navbar-collapse" id="navbarSupportedContent">
					<ul class="navbar-nav me-auto mb-3 mb-lg-0">       				<li class="nav-item">
						<a class="nav-link" aria-current="page" href="{{ url_for('index') }}">Home</a>
						</li>
						<li class="nav-item">
							<a class="nav-link" href="{% if is_doctor %}{{ url_for('doctor_dashboard') }}{% else %}{{ url_for('dashboard') }}{% endif %}">Dashboard</a>
						</li>
					</ul>
					<ul class="navbar-nav ms-auto mb-2 mb-lg-0"> {% if session['user_id'] %}
							<li class="nav-item">
								<a class="nav-link" href="{{ url_for('logout') }}">Logout</a>
							</li>
							{% else %}
							<li class="nav-item">
								<a class="nav-link" href="{{ url_for('login') }}">Login</a>
							</li>
							<li class="nav-item">
								<a class="nav-link" href="{{ url_for('signup') }}">Signup</a>
							</li>
							{% endif %}
					</ul>
					<span class="navbar-text">
					</span>
				</div>
			</div>
		</nav>
    	</div>
  		</nav>
  <link href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <link href="https://getbootstrap.com/docs/5.2/assets/css/docs.css" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js"></script>
		<br>

		{% block content %}
      
    {% endblock %}
 
<-- Uneeded Demo Code -->
</body>
```

You can see that we imported the same libraries multiple times near the end, that was because we were in a rush to finish before the 24 hours ended; not to mention we were sleep deprived. When looking at the navigation bar (which is all I really included) you can see the bootstrap being put to use. After it, you can see ``{% block content %}`` and `` {% endblock %}`` which is our Jinja code sharing all our designs to the other templates.

# Features
To try this out for yourself, clone our GitHub repo on [replit.com](replit.com) and put in your own API keys and secrets to try out our innovative medifier program! Thank you for sticking with us to the end, have a great day.
<br>
~ documented by Wissam Nusair

