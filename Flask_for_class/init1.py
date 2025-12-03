#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
import os
from dotenv import load_dotenv
from datetime import datetime # necessary for obtaining the current date and time
import hashlib # this is used in the md5 helper func
import random # this is used for the flight_num generation for inserting values into Flight
from functools import wraps # this is to use the protected thingy we learned from class

load_dotenv()

#Initialize the app from Flask
app = Flask(__name__)

# Ideally load these from environment variables
AIVEN_HOST = os.getenv("AIVEN_HOST")
AIVEN_PORT = int(os.getenv("AIVEN_PORT", "22766"))
AIVEN_USER = os.getenv("AIVEN_USER")
AIVEN_PASSWORD = os.getenv("AIVEN_PASSWORD")
AIVEN_DB = os.getenv("AIVEN_DB")
AIVEN_CA_PATH = os.getenv("AIVEN_CA_PATH")

conn = pymysql.connect(
	host=AIVEN_HOST,
	port=AIVEN_PORT,
	user=AIVEN_USER,
	password=AIVEN_PASSWORD,
	database=AIVEN_DB,
	charset='utf8mb4',
	cursorclass=pymysql.cursors.DictCursor,
    ssl={
        "ca": AIVEN_CA_PATH
		}
)


#Define a route to hello function
@app.route('/')
def hello():
	return render_template('index.html')


# CUSTOMER LOGIN AND REGISTRATION PAGES
#Define route for login
@app.route('/login')
def login():
	return render_template('login.html')


#Define route for register
@app.route('/register')
def register():
	return render_template('register.html')


# AIRLINE STAFF LOGIN AND REGISTRATION PAGES
# Defines route for airline staff registration page
@app.route('/airline_staff_registration')
def airlineReg():
	return render_template('airline_staff_registration.html')


# Defines route for the airline staff login page
@app.route('/airline_staff_login')
def airlineLog():
	return render_template('airline_staff_login.html')


# AUTHENTICATION PAGES FOR 
#Authenticates the login - customer login
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
	#grabs information from the forms
	username = request.form['email']
	password = request.form['password']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM Customer WHERE email = %s and password = %s'
	cursor.execute(query, (username, password))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		session['email'] = username
		return redirect(url_for('home'))
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('login.html', error=error)


#Authenticates the register - customer register
@app.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
	#grabs information from the forms

	fields = [
    "first_name", "last_name", "building_num",
    "street", "city", "state", "phone_number", "passport_num",
    "passport_expiration", "passport_country", "dob", "password"
	]
	customer_email = request.form['customer_email']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM Customer WHERE customer_email = %s'
	cursor.execute(query, (customer_email))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('register.html', error = error)
	else:
		ins = 'INSERT INTO Customer VALUES(%s, %s)'
		cursor.execute(ins, (username, password))
		conn.commit()
		cursor.close()
		return render_template('index.html')
	cursor.close()


# ========== AIRLINE STAFF RELATED FUNCTIONS ==========


# This is a decorator that will make the route only accessible to logged in users
# Make sure to import functools
def protected_route(route):
	@wraps(route)
	def wrapper(*args, **kwargs):
		if session.get('username'):
			return route(*args, **kwargs) # Direct to the actual function implementation
		else:
			return render_template('index.html') # Redirect to unauthorized page or whatever of your choice
	return wrapper


# authenticates the register - admin register
@app.route('/airlineRegAuth', methods=['GET', 'POST'])
def airlineRegAuth():
	#grabs information from the forms

	# username has to be checked if already exists
	admin_username = request.form['username']

	# airline_name has to be checked if exists
	airline_name = request.form['airline_name']

	# rest of the attributes
	password = request.form['password']
	first_name = request.form['first_name']
	last_name = request.form['last_name']
	dob = request.form['dob']
	airlinestaff_email = request.form['airlinestaff_email']

	#cursor used to send queries; general purpose connection with the db
	cursor = conn.cursor()

	# check if the username is already taken in Airline_Staff table
	query = 'SELECT * FROM Airline_Staff WHERE username = %s'
	cursor.execute(query, (admin_username))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row

	# check if the airline name is present in the Airline table
	query = 'SELECT * FROM Airline WHERE airline_name = %s'
	cursor.execute(query, (airline_name))
	
	data2 = cursor.fetchone()

	# execute next query
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('airline_staff_registration.html', error = error)
	elif(not data2):
		# this means the airline isn't present in the Airline table; return error
		error = "Enter a valid airline"
		return render_template('airline_staff_registration.html', error = error)
	else:
		# insert the appropriate values into the Airline_Staff table
		# insertions are in the order which tuple for the Airline_Staff table must be inserted

		# insert the values into the Airline_Staff table
		ins = 'INSERT INTO Airline_Staff VALUES(%s, %s, %s, %s, %s, %s, %s)'
		# password must be hashed before being inserted into the table
		cursor.execute(ins, (username, hashPass(password), first_name, last_name, dob, airlinestaff_email, airline_name))

		# close the cursor's connection and commit changes
		conn.commit()
		cursor.close()

		# send the user to the airline staff login page
		return render_template('airline_staff_login.html')


#Authenticates the login - customer login
@app.route('/airlineLogAuth', methods=['GET', 'POST'])
def airlineLogAuth():
	#grabs information from the forms
	username = request.form['username']
	password = hashPass(request.form['password'])

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM Airline_Staff WHERE username = %s and password = %s'
	cursor.execute(query, (username, password))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		session['username'] = username
		session['airline_name'] = data['airline_name']
		return redirect(url_for('airline_staff'))
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('airline_staff_login.html', error=error)


@app.route('/airline_staff')
@protected_route
def airline_staff():
	username = session['username']
	airline_name = session['airline_name']
	cursor = conn.cursor()
	# default for search flights:
	curr_date = getDateTime()
	query = 'select * from Flight where departure_date_time between %s and DATE_ADD(%s, INTERVAL 30 DAY) and airline_name = %s;'
	cursor.execute(query, (curr_date, curr_date, airline_name))

	flights = cursor.fetchall()

	# for the create flights feature, get the airplane ids for the drop down
	query = 'select * from Airplane where airline_name = %s;'
	cursor.execute(query, (airline_name))
	airplanes = cursor.fetchall()

	# add airplanes to session so that it persists until the airline_staff logs out
	session['airplanes'] = airplanes

	cursor.close()
	return render_template('airline_staff.html', username=username, flights=flights, airplanes=airplanes)


# Search for flights as an airline staff
@app.route('/searchFlights', methods=['GET', 'POST'])
@protected_route
def searchFlight():
	start_date = request.form['start_date']
	end_date = request.form['end_date']
	dept_code = request.form['dept_code']
	arr_code = request.form['arr_code']
	airline_name = session['airline_name']

	# cursor used to send queries; used to interface with the database!
	cursor = conn.cursor()

	# to shorten the cases, you can either have:
	# none (default)
	if (not start_date and not end_date and not dept_code and not arr_code):
		curr_date = getDateTime()
		query = 'select * from Flight where departure_date_time between %s and DATE_ADD(%s, INTERVAL 30 DAY) and airline_name = %s;'
		cursor.execute(query, (curr_date, curr_date, airline_name))

		flights = cursor.fetchall()
		cursor.close()
		return render_template('airline_staff.html', flights=flights, airplanes=session['airplanes'])
	# all
	elif (start_date and end_date and dept_code and arr_code):
		# use helper function to convert the times from form to appropriate type
		start_date = datetimelocalToDatetime(start_date)
		end_date = datetimelocalToDatetime(end_date)
		query = 'select * from Flight where departure_date_time between %s and %s and dept_airport = %s and arr_airport = %s and airline_name = %s;'
		cursor.execute(query, (start_date, end_date, dept_code, arr_code, airline_name))

		flights = cursor.fetchall()
		cursor.close()
		return render_template('airline_staff.html', flights=flights, airplanes=session['airplanes'])
	# only start or end dates
	elif (start_date and end_date and not dept_code and not arr_code):
		# use helper function to convert the times from form to appropriate type
		start_date = datetimelocalToDatetime(start_date)
		end_date = datetimelocalToDatetime(end_date)
		query = 'select * from Flight where departure_date_time between %s and %s and airline_name = %s;'
		cursor.execute(query, (start_date, end_date, airline_name))

		flights = cursor.fetchall()
		cursor.close()
		return render_template('airline_staff.html', flights=flights, airplanes=session['airplanes'])
	# only dept and arr airport codes
	elif (not start_date and not end_date and dept_code and arr_code):
		query = 'select * from Flight where dept_airport = %s and arr_airport = %s and airline_name = %s;'
		cursor.execute(query, (dept_code, arr_code, airline_name))

		flights = cursor.fetchall()
		cursor.close()
		return render_template('airline_staff.html', flights=flights, airplanes=session['airplanes'])
	else:
		error = 'You must choose a date range, departure and arrival airports, or both'
		cursor.close()
		return render_template('airline_staff.html', error=error, airplanes=session['airplanes'])


@app.route('/logout_admin')
def logout_admin():
	session.pop('username')
	session.pop('airline_name')
	session.pop('airplanes')
	return redirect('/')


# Search for flights as an airline staff
@app.route('/createFlight', methods=['GET', 'POST'])
@protected_route
def createFlight():
	# values which will be inserted into the db; are in basic order in which they will be inserted
	airplane_id = request.form.get('airplane_name')
	airline_name = session['airline_name']
	flight_num = randomNumberSize20()
	departure_date_time = request.form['departure_date_time']
	arrival_date_time = request.form['arrival_date_time']
	dept_airport = request.form['dept_airport']
	arr_airport = request.form['arr_airport']
	flight_price = request.form['flight_price']
	flight_status = 'on-time' # this will be the default status for a flight; can later be changed once inserted

	# checks if drop down menu value was selected or not
	if (not airplane_id):
		return render_template('airline_staff.html', error2 = error2, airplanes=session['airplanes'])

	cursor = conn.cursor()

	query = 'insert into Flight values (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
	cursor.execute(query, (airplane_id, airline_name, flight_num, departure_date_time, arrival_date_time, dept_airport, arr_airport, flight_price, flight_status))

	conn.commit()
	cursor.close()

	return redirect(url_for('airline_staff'))


# Add an airplane to the airline you work for
@app.route('/addAirplane', methods=['GET', 'POST'])
@protected_route
def addAirplane():
	airline_name = session['airline_name']
	num_of_seats = request.form['num_of_seats']
	manufacture_comp = request.form['manufacture_comp']
	age = request.form['age']
	airplane_id = request.form['airplane_id']

	cursor = conn.cursor()
	# check if not already in database
	query = 'select * from Airplane where airline_name = %s and airplane_id = %s;'
	cursor.execute(query, (airline_name, airplane_id))

	data = cursor.fetchone()
	if(data):
		error = 'Airplane with the same id already exists'
		cursor.close()
		return render_template('airline_staff.html', error3=error)
	else:
		# insert into Airplane
		query = 'insert into Airplane values (%s, %s, %s, %s, %s)'
		cursor.execute(query, (num_of_seats, manufacture_comp, age, airplane_id, airline_name))

		# commit changes
		conn.commit()
		

		# update the value of session['airplanes']:
		query = 'select * from Airplane where airline_name = %s;'
		cursor.execute(query, (airline_name))
		session['airplanes'] = cursor.fetchall()

		cursor.close()
		# reload the page so that new data may be added
		return redirect(url_for('airline_staff'))


# Toggle the status of a flight which the toggle button was pressed for
@app.route("/toggle_status", methods=['GET', 'POST'])
@protected_route
def toggle_status():
	airline_name = session['airline_name']
	flight_num = request.form['flight_num']
	departure_date_time = request.form['departure_date_time']

	cursor = conn.cursor()

	# fetch current status
	query = 'select * from Flight where flight_num = %s and departure_date_time = %s and airline_name = %s;'
	cursor.execute(query, (flight_num, departure_date_time, airline_name))
	# result will be one row, since we used primary key as query arguments
	data = cursor.fetchone()

	# get the current status which the flight is
	current_status = (data)['flight_status'].lower()

	# depending on what the status is currently, change it to something new
	new_status = "on-time" if current_status == "delayed" else "delayed"

	# update the flight status to the new status value
	query = 'update Flight set flight_status = %s where flight_num = %s and departure_date_time = %s and airline_name = %s;'
	cursor.execute(query, (new_status, flight_num, departure_date_time, airline_name))

	conn.commit()
	cursor.close()

	# load the whole page again; this time will reflect our changes
	return redirect(url_for('airline_staff'))


# TODO: Implement the 'View flight ratings' functionality
'''
	This doesn't have to be too complex, just do what the project guidelines specify
	Specifications:
	* airline staff will be able to see each flight's avg ratings AND
	* all the comments and ratings of that flight given by the customers

	Initial idea:
	Seeing each flight is already controlled by the 'search flights' functionality.

	Maybe, much like I did with the toggle, something may be incorporated so that
	all flights may be able to be clicked (once the admin finds the flight they're looking
	for), then that flight would show its average ratings (easy to calculate with a simple query),
	and all its comments with ratings attached next to them.

	It would look something like this:
	search flights:
	(search bar etc.)
	table
	-- | -- | ....... | toggle  | view ratings
	-- | -- | ....... | on-time | ratings

	once the 'ratings' button would be touched, to make it easier on myself, I could make
	a 'ratings' table pop up (jinja is good for this) below the 'flights' table, and
	it would look something like this:

	average rating: 4.5
	reviews:
	rating | comment
	3.4    | lorem ipsum
	4.3    | blah blah blah
	... etc.

	I think this is a pretty good idea, even though it is very barebones and doesn't
	look pretty at all, it gets the job done.
'''
@app.route('/view_ratings', methods=['GET', 'POST'])
@protected_route
def view_ratings():
	airline_name = session['airline_name']
	flight_num = request.form['flight_num']
	departure_date_time = request.form['departure_date_time']

	cursor = conn.cursor()
	# for both, remember to deal with the case that no info is returned
	# get the avg ratings
	# get all the ratings related to the flight
	query = 'select rate, comment from Review where airline_name = %s and flight_num = %s and departure_date_time = %s;'
	# # TODO TODO TODO TODO FOR TESTING PURPOSES ONLY TODO TODO TODO TODO
	# airline_name = 'Air France'
	# flight_num = '61983286426849401608'
	# departure_date_time = '2025-12-01 04:21:00'
	cursor.execute(query, (airline_name, flight_num, departure_date_time))
	
	reviews = cursor.fetchall()

	query = 'select sum(rate) / count(rate) as average_rating from Review where airline_name = %s and flight_num = %s and departure_date_time = %s;'
	cursor.execute(query, (airline_name, flight_num, departure_date_time))

	average_rating = (cursor.fetchone())['average_rating']
	
	cursor.close()
	return render_template('airline_staff.html', reviews = reviews, average_rating = average_rating)



# Helper functions
# Get the current date and time in the appropriate format
def getDateTime():
	now = datetime.now()
	return now.strftime("%Y-%m-%d %H:%M:%S")


# Switch the datetime-local format to the appropriate format
def datetimelocalToDatetime(datetimelocal):
	# datetimelocal is from request.form[]
	# parse the datetime-local format
	dt = datetime.fromisoformat(datetimelocal)

	# format it to "YYYY-MM-DD HH:MM:SS"
	formatted = dt.strftime("%Y-%m-%d %H:%M:%S")
	return formatted


# Create a random number of max length 20
def randomNumberSize20():
    return str(random.randrange(0, 10**20))


# TODO: Add the hash function you built in the other project to this one for encryption of the passwords
# hashes passwords using MD5
def hashPass(password):
	# create a new MD5 hash object
	m = hashlib.md5()

    # update the hash object with the bytes-like object (encoded string)
	m.update(password.encode('utf-8'))

    # get the hash in a human-readable hexadecimal format
	md5_hash = m.hexdigest()

	return md5_hash

		
app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)
