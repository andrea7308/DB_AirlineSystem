#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
import os
from dotenv import load_dotenv

load_dotenv('.env')

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

#Define route for login
@app.route('/login')
def login():
	return render_template('login.html')

#Define route for register
@app.route('/register')
def register():
	return render_template('register.html')

# Defines route for airline staff registration page
@app.route('/airline_staff_registration')
def airlineReg():
	return render_template('airline_staff_registration.html')

# Defines route for the airline staff login page
@app.route('/airline_staff_login')
def airlineLog():
	return render_template('airline_staff_login.html')

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


# ========== AIRLINE STAFF RELATED FUNCTIONS
# authenticates the register - admin register
@app.route('/airlineRegAuth', methods=['GET', 'POST'])
def airlineRegAuth():
	#grabs information from the forms

	# username has to be checked if already exists
	admin_username = request.form['username']

	# airline_name has to be checked if exists
	airline_name = request.form['airline_name']

	# list of fields which need to be added to the db
	fields = [
		"password", "first_name", "last_name", "dob", "airlinestaff_email"
	]

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
		arr = list()
		arr.append(admin_username)
		for field in fields:
			arr.append(request.form[field])
		arr.append(airline_name)

		# insert the values into the Airline_Staff table
		ins = 'INSERT INTO Airline_Staff VALUES(%s, %s, %s, %s, %s, %s, %s)'
		cursor.execute(ins, tuple(arr))

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
	password = request.form['password']

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
		return redirect(url_for('airline_staff'))
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('airline_staff_login.html', error=error)


@app.route('/airline_staff')
def airline_staff():
	username = session['username']
	return render_template('airline_staff.html', user=username)


# @app.route('/home')
# def home():
    
#     username = session['username']
#     cursor = conn.cursor();
#     query = 'SELECT ts, blog_post FROM blog WHERE username = %s ORDER BY ts DESC'
#     cursor.execute(query, (username))
#     data1 = cursor.fetchall() 
#     for each in data1:
#         print(each['blog_post'])
#     cursor.close()
#     return render_template('home.html', username=username, posts=data1)

		
# @app.route('/post', methods=['GET', 'POST'])
# def post():
# 	username = session['username']
# 	cursor = conn.cursor();
# 	blog = request.form['blog']
# 	query = 'INSERT INTO blog (blog_post, username) VALUES(%s, %s)'
# 	cursor.execute(query, (blog, username))
# 	conn.commit()
# 	cursor.close()
# 	return redirect(url_for('home'))

@app.route('/logout')
def logout():
	session.pop('email')
	return redirect('/')
		
app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)
