import google.generativeai as genai
import sqlite3
import os

genai.configure(api_key=os.environ["API_KEY"])
model = genai.GenerativeModel('gemini-pro')

doctorName = ["Dr. James", "Dr. Jane", "Dr. John", "Dr. Emily"]
doctorSpecializations = ["Cardiology", "Neurology", "Oncology", "Psychiatry"]
doctorNotes = ["I have a fever", "I have a cough", "I have a sore throat"]
appointmentTimings = ["8:00 AM", "9:00 AM", "10:00 AM", "11:00 AM"]
appointmentLocations = ["Room 1", "Room 2", "Room 3", "Room 4"]


# ai_functions.py
import google.generativeai as genai
import os

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


"""
while True:
	try:
		symptoms = input("Please input your symptoms: ")
		# REMOVE THIS IF STATEMENT IN PROD
		if symptoms == "e":
			break
		symptomsResponse = model.generate_content(
		    f"Given the following symptoms: {symptoms}. What are some possible medications that could be used to relieve these symptoms? If the symptoms are too dire, please tell me to contact a doctor or call the emergency number (911 in the United States). Then please tell me if the medication is safe to take."
		)
		print(symptomsResponse.text)

		yes_or_no = input(
		    "Would you like to schedule a doctor appointment? (y/n): ")

		yesNoResponse = model.generate_content(
		    f"Given the following, '{yes_or_no}', do you believe I was saying yes or no? If no, please output 'no'. If yes, please output 'yes'. Saying 'y' automatically says yes, if 'n' automatically says no."
		)
		if yesNoResponse.text == "yes":
			appointSchedResponse = model.generate_content(
			    f"If I say yes, please ask which timings work for me based off the avaliable appointments. IF I says no, then say 'I understand. If you ever change your mind, please input your symptoms and schedule an appointment.' I said {yesNoResponse.text}. The doctors are {doctorName} and their respective specializations are as follow, {doctorSpecializations}. Please only list the doctors with the specializations that more directly follow the symptoms, {symptoms}. The respective appointment timings are {appointmentTimings}, their respective locations is {appointmentLocations}. Number ONLY the doctors whose specialization help the patient the most and also list their specialization as well, with timings and location, in numerical order in a single line. Start off saying something along the lines of 'here are all the doctors that are availible for you based off your symptoms'"
			)
			print(f"{appointSchedResponse.text}")
			userSched = input("Please input your preferred appointment time: ")
			confirmResponse = model.generate_content(
			    f"Given the following appointment timings, '{appointSchedResponse.text}', and I said '{userSched}' create a confirmation message that the appointment was successfully schedules."
			)
			print(f"{confirmResponse.text}")
			listDEVResponse = model.generate_content(
			    f"Given {confirmResponse}, create a python list of the name, the time, and the loction and output it."
			)
			print(f"{listDEVResponse.text}")
		else:
			print(
			    "I understand. If you ever change your mind, please input your symptoms and schedule an appointment."
			)
	except Exception as e:
		print("\nPlease input a valid response.\n")
"""
