#Import Flask Library

from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
import os
from dotenv import load_dotenv
import json
import random

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
	return render_template('customer_login.html')

#Define route for register
@app.route('/register')
def register():
	return render_template('customer_register.html')

#Authenticates the login
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM Customer WHERE customer_email = %s and password = %s'
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
		return redirect(url_for('customerPage'))
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('customer_login.html', error=error)

#Authenticates the register
@app.route('/registerAuthCustomer', methods=['GET', 'POST'])
def registerAuthCustomer():

	#stores the necessary info from customer
	fields = [
    "first_name", "last_name", "password", "building_num",
    "street", "city", "state", "phone_number", "passport_num",
    "passport_expiration", "passport_country", "dob"
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
		# fields from html arr
		arr = list()
		arr.append(customer_email)
		# loop over the fields
		for field in fields:
			arr.append(request.form[field])
		ins = 'INSERT INTO Customer VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
		cursor.execute(ins, tuple(arr))
		conn.commit()
		cursor.close()
		return render_template('index.html')

@app.route('/customerPage', methods=['GET', 'POST'])
def customerPage():
	customer_email = session.get('username')
	cursor = conn.cursor()
	
	query1 ="""
			select t.ticket_id, t.airline_name, t.flight_num, 
				f.departure_date_time, f.arrival_date_time 
			from Ticket as t 
			join Flight as f 
			on t.airline_name = f.airline_name 
			and t.flight_num = f.flight_num 
			and t.departure_date_time = f.departure_date_time 
			where t.customer_email = %s 
			and f.departure_date_time >= now()
			"""
	cursor.execute(query1, (customer_email,))
	data1 = cursor.fetchall()
	
	query2 = 'select r.rate, r.comment, r.airline_name, r.departure_date_time from Review as r where r.customer_email = %s  order by departure_date_time asc'
	cursor.execute(query2, (customer_email,))
	data2 = cursor.fetchall()

	cursor.close()
	return render_template('customer.html', customer_email=customer_email, flights=data1, reviews=data2)


@app.route('/reviewPage', methods=['GET'])
def reviewPage():
	customer_email = session.get('username')
	cursor = conn.cursor()

	# all the reviews made by customer
	query1 ="""
			select rate, comment, airline_name, departure_date_time, flight_num
			from Review 
			where customer_email = %s
			"""
	
	cursor.execute(query1, (customer_email,))
	reviews = cursor.fetchall()

	query2 ="""
			select t.ticket_id, t.airline_name, t.flight_num, 
				f.departure_date_time, f.arrival_date_time 
			from Ticket as t 
			join Flight as f 
			on t.airline_name = f.airline_name 
			and t.flight_num = f.flight_num 
			and t.departure_date_time = f.departure_date_time 
			where t.customer_email = %s 
			and f.departure_date_time < now()
			"""
	
	cursor.execute(query2, (customer_email,))
	flights = cursor.fetchall()

	cursor.close()

	return render_template('reviews.html', reviews=reviews, flights=flights )

@app.route('/review', methods=['POST'])
def review():
	customer_email = session.get('username')
	cursor = conn.cursor()

	flight_info = json.loads(request.form['flight'])
	airline_name = flight_info['airline_name']
	flight_num = flight_info['flight_num']
	departure_date_time = flight_info['departure_date_time']

	rating = request.form['rating']
	comment = request.form['comment']

	ins ="""
		 insert into Review(customer_email, flight_num, 
		 	departure_date_time, airline_name, rate, comment) 
		 values (%s, %s, %s, %s, %s, %s)
		 """

	cursor.execute(ins, (customer_email, flight_num, departure_date_time, airline_name, rating, comment))
	conn.commit()
	cursor.close()

	return redirect(url_for('reviewPage'))

@app.route('/displayFlights', methods=['GET', 'POST'])
def displayFlights():
	return render_template('displayFlights.html')

@app.route('/purchaseFlight/<flight_num>', methods=['GET'])
def purchaseFlight(flight_num):
	cursor = conn.cursor()

	query = """
        SELECT * FROM Flight
        WHERE flight_num = %s
    """
	cursor.execute(query, (flight_num,))
	flight = cursor.fetchone()

	return render_template('purchaseFlight.html', flight=flight)

@app.route('/confirmPurchase', methods=['POST'])
def confirmPurchase():
	username = session['username']
	cursor = conn.cursor()

	airline_name = request.form['airline_name']
	flight_num = request.form['flight_num']
	departure_date_time = request.form['departure_date_time']

	check =	"""
			SELECT * FROM Ticket
			WHERE customer_email = %s
			AND airline_name = %s
			AND flight_num = %s
			AND departure_date_time = %s
    		"""

	cursor.execute(check, (username, airline_name, flight_num, departure_date_time))
	if cursor.fetchone():
			query1 = """
					SELECT ticket_id, airline_name, flight_num, departure_date_time
					FROM Ticket
					WHERE customer_email = %s
					ORDER BY departure_date_time
					"""
			cursor.execute(query1, (username,))
			flights = cursor.fetchall()
			
			cursor.close()
			# Pass message to customerPage
			return render_template('customer.html', customer_email=username, flights=flights,
								message="You already purchased a ticket for this flight.")


	cursor.execute("select ticket_id from Ticket")
	all_ticket_ids = [row['ticket_id'] for row in cursor.fetchall()]

	
	ticket_id = random.randint(1000, 9999)
	while ticket_id in all_ticket_ids:
		ticket_id = random.randint(1000, 9999)

	card_type = request.form['card_type']
	card_number = request.form['card_number']
	name_on_card = request.form['name_on_card']
	card_exp_date = request.form['card_exp_date']
	card_exp_date = card_exp_date + "-01" 
	customer_email = username

	ins="""
		insert into Ticket ( 
			ticket_id,
			card_type,
			card_number,
			name_on_card,
			purchase_date_time,
			card_exp_date,
			customer_email,
			airline_name,
			flight_num,
			departure_date_time
		)
		values (%s, %s, %s, %s, now(), %s, %s, %s, %s, %s)
		"""
	
	cursor.execute(ins, (
		ticket_id, 
		card_type, 
		card_number, 
		name_on_card, 
		card_exp_date, 
		customer_email, 
		airline_name, 
		flight_num, 
		departure_date_time
	))
	
	conn.commit()
	cursor.close()

	return redirect(url_for('purchaseSuccess'))

@app.route('/purchaseSuccess')
def purchaseSuccess():
    return render_template('purchaseSuccess.html')


@app.route('/searchFlights', methods=['GET', 'POST'])
def searchFlights():
	cursor = conn.cursor()

	dept_airport = request.form['departure_airport']
	arr_airport = request.form['arrival_airport']
	departure_date = request.form['departure_date']

	query1= """
			select airline_name, flight_num, departure_date_time,
				arrival_date_time, dept_airport, arr_airport, flight_price 
			from Flight
			where dept_airport = %s 
			and arr_airport = %s
			and date(departure_date_time) = %s
			"""
	
	cursor.execute(query1, (dept_airport, arr_airport, departure_date))
	flights = cursor.fetchall()
	cursor.close()

	return render_template('searchFlights.html', flights=flights)

@app.route('/home')
def home():
    
    username = session['username']
    cursor = conn.cursor()
    query = 'SELECT * from Flight'
    cursor.execute(query)
    data1 = cursor.fetchall() 
    cursor.close()
    return render_template('home.html', username=username, flights=data1)

		
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
	session.pop('username')
	return redirect('/')
		
app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)
