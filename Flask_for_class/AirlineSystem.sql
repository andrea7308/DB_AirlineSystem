CREATE TABLE Airport (
    airport_code VARCHAR(5) PRIMARY KEY, 
    airport_city VARCHAR(20) NOT NULL,
    airport_country VARCHAR(20) NOT NULL,
    airport_type VARCHAR(20),
    CHECK (airport_type IN ('domestic', 'international', 'domestic/international'))
);

CREATE TABLE Airline (
    airline_name VARCHAR(20) PRIMARY KEY
);

CREATE TABLE Customer (
    customer_email VARCHAR(50) PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    building_num INT NOT NULL, 
    street VARCHAR(50) NOT NULL, 
    city VARCHAR(30) NOT NULL,
    state VARCHAR(30),
    phone_number VARCHAR(15),
    passport_num VARCHAR(9) UNIQUE, 
    passport_expiration DATE,
    passport_country VARCHAR(30), 
    dob DATE NOT NULL
);

CREATE TABLE Airplane (
    num_of_seats INT,
    manufacture_comp VARCHAR(20),
    age INT, 
    airplane_id VARCHAR(20),
    airline_name VARCHAR(20),	
    PRIMARY KEY(airplane_id, airline_name),
    FOREIGN KEY (airline_name) REFERENCES Airline(airline_name)
);


CREATE TABLE Flight (
    airplane_id VARCHAR(20),
    airline_name VARCHAR(20),
    flight_num VARCHAR(20),
    departure_date_time DATETIME,
    arrival_date_time DATETIME NOT NULL,
    dept_airport VARCHAR(5) NOT NULL,
    arr_airport VARCHAR(5) NOT NULL,
    flight_price DECIMAL(10,2),
    flight_status VARCHAR(20),
    PRIMARY KEY(airline_name, flight_num, departure_date_time),
    FOREIGN KEY(airplane_id,airline_name) REFERENCES Airplane(airplane_id, airline_name),
    FOREIGN  KEY(dept_airport) REFERENCES Airport(airport_code),
    FOREIGN KEY(arr_airport) REFERENCES Airport(airport_code),
    CHECK(flight_status IN ('On-time', 'Delayed'))
);


CREATE TABLE Airline_Staff (
    username VARCHAR(10) PRIMARY KEY,
    password VARCHAR(20) NOT NULL,
    first_name VARCHAR(20) NOT NULL,
    last_name VARCHAR(20) NOT NULL,
    dob DATE,
    airlinestaff_email VARCHAR(50) NOT NULL,
    airline_name VARCHAR(20),
    FOREIGN KEY(airline_name) references Airline(airline_name)
);


CREATE TABLE Phone_Numbers (
    username VARCHAR(10) NOT NULL,
    phone_number VARCHAR(15),
    PRIMARY KEY(username, phone_number),
    FOREIGN KEY (username) REFERENCES Airline_Staff(username)
);


CREATE TABLE Review (
    rate INT,
    comment VARCHAR(4000),
    customer_email VARCHAR(50),
    airline_name VARCHAR(20),
    flight_num VARCHAR(20),
    departure_date_time DATETIME,
    PRIMARY KEY(customer_email, flight_num, departure_date_time, airline_name),
    FOREIGN KEY (customer_email) REFERENCES Customer(customer_email),
    FOREIGN KEY (airline_name, flight_num, departure_date_time)
        REFERENCES Flight(airline_name, flight_num, departure_date_time)
);

CREATE TABLE Ticket (
    ticket_id BIGINT PRIMARY KEY,
    card_type VARCHAR(10) NOT NULL,
    card_number VARCHAR(20) NOT NULL,
    name_on_card VARCHAR(50) NOT NULL,
    card_exp_date DATE NOT NULL,
    purchase_date_time DATETIME NOT NULL,
    customer_email VARCHAR(50) NOT NULL,
    airline_name VARCHAR(20),
    da_num VARCHAR(20),
    departure_date_time DATETIME,
    FOREIGN KEY (customer_email) REFERENCES Customer(customer_email),
    FOREIGN KEY (airline_name, flight_num, departure_date_time) REFERENCES Flight(airline_name, flight_num, departure_date_time),
    CHECK (card_type IN ('credit', 'debit'))

);


-- INSERT STATEMENTS
INSERT INTO Airport (airport_code, airport_city, airport_country, airport_type) VALUES
('ATL', 'Atlanta', 'United States', 'international'),
('BOS', 'Boston', 'United States', 'domestic/international'),
('CDG', 'Paris', 'France', 'international'),
('DBX', 'Dubai', 'United Arab Emirates', 'international'),
('DCA', 'Washington DC', 'United States', 'domestic'),
('DEN', 'Denver', 'United States', 'domestic/international'),
('EWR', 'Newark', 'United States', 'domestic/international'),
('FRA', 'Frankfurt', 'Germany', 'international'),
('GRU', 'São Paulo', 'Brazil', 'international'),
('HND', 'Tokyo', 'Japan', 'international'),
('IAH', 'Houston', 'United States', 'domestic'),
('JFK', 'New York City', 'United States', 'domestic'),
('LAS', 'Las Vegas', 'United States', 'domestic/international'),
('LAX', 'Los Angeles', 'United States', 'international'),
('LGA', 'New York City', 'United States', 'domestic'),
('LHR', 'London', 'United Kingdom', 'international'),
('MAD', 'Madrid', 'Spain', 'international'),
('MIA', 'Miami', 'United States', 'international'),
('ORD', 'Chicago', 'United States', 'international'),
('PHX', 'Phoenix', 'United States', 'domestic/international'),
('PVG', 'Shanghai', 'China', 'international'),
('SAN', 'San Diego', 'United States', 'domestic/international'),
('SEA', 'Seattle', 'United States', 'international'),
('SFO', 'San Francisco', 'United States', 'domestic'),
('SJU', 'San Juan', 'United States', 'domestic'),
('SYD', 'Sydney', 'Australia', 'international'),
('YVR', 'Vancouver', 'Canada', 'international'),
('YYZ', 'Toronto', 'Canada', 'international');

INSERT INTO Airline (airline_name) VALUES
('Air France'),
('Alaska'),
('American Airlines'),
('Delta Air Lines'),
('Emirates'),
('Jet Blue'),
('Southwest'),
('United');

INSERT INTO Customer (
    customer_email, first_name, last_name, password,
    building_num, street, city, state,
    phone_number, passport_num, passport_expiration,
    passport_country, dob
) VALUES
('ag8754@nyu.edu', 'Andrea', 'Gonzalez', '5f4dcc3b5aa765d61d8327deb882cf99',
 636, 'Greenwich St.', 'New York', 'New York',
 '1234567890', '123456789', '2025-11-22',
 'texas', '2025-11-22'),

('lola@email.com', 'lola', 'lola', '827ccb0eea8a706c4c34a16891f84e7b',
 1, '1', 'LIC', 'NV',
 '1234567', '9182734', '2050-10-20',
 'US', '2011-11-11'),

('paulitoed', 'this', 'this', '9e925e9341b490bfd3b4c4ca3b0c1ef2',
 2, 'this', 'this', 'this',
 '929', '1313423', '2025-12-01',
 'this', '2025-12-03'),

('test@test.com', 'Test', 'Test', '5f4dcc3b5aa765d61d8327deb882cf99',
 123, 'Street', 'City', 'State',
 '1234567890', '1', '2029-07-04',
 'country', '2000-06-09'),

('test2@test.com', 'Test2', 'Test', '827ccb0eea8a706c4c34a16891f84e7b',
 123, 'Street', 'City', 'State',
 '1234567890', '12', '2033-06-29',
 'country', '2004-02-04');

INSERT INTO Airplane (
    num_of_seats, manufacture_comp, age, airplane_id, airline_name
) VALUES
(200, 'Mango', 23, '1011', 'Air France'),
(150, 'Airbus', 15, 'N123GS', 'United'),
(1,   'Airbus', 23, 'N124HJ', 'United'),
(155, 'Boeing', 9,  'N221WN', 'Southwest'),
(40,  'Boeing', 20, 'N234JK', 'Jet Blue'),
(300, 'Boeing', 25, 'N303ZS', 'Air France'),
(300, 'Boeing', 25, 'N303ZS', 'Delta Air Lines'),
(180, 'Boeing', 20, 'N303ZS', 'Jet Blue'),
(150, 'Airbus', 15, 'N326CS', 'Jet Blue'),
(150, 'Airbus', 15, 'N326RH', 'Emirates'),
(180, 'Boeing', 20, 'N333PK', 'United'),
(300, 'Boeing', 25, 'N365LS', 'Southwest'),
(180, 'Boeing', 20, 'N378PS', 'Alaska'),
(190, 'Boeing', 5,  'N450UA', 'United'),
(168, 'Boeing', 8,  'N490EK', 'Emirates'),
(160, 'Boeing', 4,  'N615DA', 'Delta Air Lines'),
(165, 'Airbus', 2,  'N670AS', 'Alaska'),
(180, 'Airbus', 6,  'N734JB', 'Jet Blue'),
(220, 'Airbus', 3,  'N781UA', 'United'),
(175, 'Airbus', 7,  'N902AF', 'Air France');

INSERT INTO Flight (
    airplane_id, airline_name, flight_num,
    departure_date_time, arrival_date_time,
    dept_airport, arr_airport,
    flight_price, flight_status
) VALUES
('1011', 'Air France', '48407208184604508436',
 '2025-12-05 19:07:00', '2025-12-06 19:08:00',
 'JFK', 'CDG', 123.45, 'delayed'),

('N303ZS', 'Air France', '61983286426849401608',
 '2025-12-01 04:21:00', '2025-12-02 04:21:00',
 'JFK', 'CDG', 120.04, 'on-time'),

('N902AF', 'Air France', 'AF340',
 '2025-12-01 16:00:00', '2025-12-02 06:20:00',
 'JFK', 'CDG', 780.00, 'On-time'),

('N902AF', 'Air France', 'AF341',
 '2025-12-10 10:00:00', '2025-12-10 12:20:00',
 'CDG', 'JFK', 805.00, 'on-time'),

('N670AS', 'Alaska', 'AS210',
 '2025-09-15 09:20:00', '2025-09-15 12:10:00',
 'SEA', 'SAN', 165.00, 'On-time'),

('N615DA', 'Delta Air Lines', 'DL450',
 '2025-10-20 07:45:00', '2025-10-20 09:55:00',
 'ATL', 'MIA', 178.99, 'On-time'),

('N615DA', 'Delta Air Lines', 'DL451',
 '2025-10-23 19:00:00', '2025-10-23 21:10:00',
 'MIA', 'ATL', 184.50, 'Delayed'),

('N490EK', 'Emirates', 'EK204',
 '2025-12-15 22:00:00', '2025-12-16 19:00:00',
 'JFK', 'DBX', 920.00, 'On-time'),

('N490EK', 'Emirates', 'EK205',
 '2025-12-28 08:30:00', '2025-12-28 13:40:00',
 'DBX', 'JFK', 950.00, 'Delayed'),

('N303ZS', 'Jet Blue', 'JB16223',
 '2025-12-30 22:00:00', '2025-12-31 05:00:00',
 'JFK', 'CDG', 345.77, 'on-time'),

('N326CS', 'Jet Blue', 'JB3322',
 '2025-12-23 06:00:00', '2025-12-23 13:00:00',
 'DBX', 'LGA', 1346.89, 'delayed'),

('N303ZS', 'Jet Blue', 'JB3467',
 '2025-11-05 18:30:00', '2025-11-05 22:00:00',
 'LGA', 'IAH', 345.77, 'on-time'),

('N326CS', 'Jet Blue', 'JB3597',
 '2026-03-01 22:20:00', '2026-03-02 02:05:00',
 'PVG', 'JFK', 79.55, 'on-time'),

('N734JB', 'Jet Blue', 'JB765',
 '2025-09-28 13:30:00', '2025-09-28 16:45:00',
 'LGA', 'MIA', 199.25, 'On-time'),

('N734JB', 'Jet Blue', 'JB766',
 '2025-10-04 11:00:00', '2025-10-04 14:15:00',
 'MIA', 'LGA', 207.40, 'On-time'),

('N221WN', 'Southwest', 'SW330',
 '2025-08-12 06:00:00', '2025-08-12 07:45:00',
 'SFO', 'LAS', 89.99, 'On-time'),

('N221WN', 'Southwest', 'SW331',
 '2025-08-18 15:00:00', '2025-08-18 16:50:00',
 'LAS', 'SFO', 92.75, 'On-time'),

('N450UA', 'United', 'UA120',
 '2025-11-05 09:00:00', '2025-11-05 12:15:00',
 'LGA', 'ORD', 249.99, 'On-time'),

('N781UA', 'United', 'UA121',
 '2025-11-12 14:30:00', '2025-11-12 18:45:00',
 'ORD', 'LGA', 258.50, 'Delayed'),

('N781UA', 'United', 'UA235',
 '2026-01-03 05:30:00', '2026-01-04 12:00:00',
 'JFK', 'SJU', 800.00, 'Delayed'),

('N124HJ', 'United', 'UA255',
 '2026-01-03 05:30:00', '2026-01-04 12:00:00',
 'JFK', 'SJU', 800.00, 'Delayed'),

('N123GS', 'United', 'UA255',
 '2026-01-04 05:30:00', '2026-01-04 12:00:00',
 'JFK', 'SJU', 800.00, 'Delayed'),

('N450UA', 'United', 'UA300',
 '2025-11-22 08:10:00', '2025-11-22 10:50:00',
 'EWR', 'SJU', 310.00, 'On-time');

INSERT INTO Airline_Staff (
    username, password, first_name, last_name,
    dob, airlinestaff_email, airline_name
) VALUES

('Paulitoed', '827ccb0eea8a706c4c34a16891f84e7b', 'P', 'G',
 '2025-10-27', 'psg', 'Air France'),

('testinggg', '827ccb0eea8a706c4c34a16891f84e7b', 'this', 'this',
 '2025-12-01', 'this@nyu.edu', 'Jet Blue');


INSERT INTO Phone_Numbers (username, phone_number) VALUES
('testinggg', '12345'),
('testinggg', '67');

INSERT INTO Review (
    rate, comment, customer_email,
    airline_name, flight_num, departure_date_time
) VALUES
(5, 'it was amazing', 'ag8754@nyu.edu',
 'Air France', '61983286426849401608', '2025-12-01 04:21:00'),

(3, 'Nice', 'ag8754@nyu.edu',
 'Air France', 'AF340', '2025-12-01 16:00:00'),

(5, 'Loved it!', 'ag8754@nyu.edu',
 'Jet Blue', 'JB3467', '2025-11-05 18:30:00'),

(4, 'it was awesome', 'bradtheman@gmail.com',
 'Air France', '61983286426849401608', '2025-12-01 04:21:00'),

(4, 'it was a mediocre experience', 'bradtheman@gmail.com',
 'Jet Blue', 'JB3467', '2025-11-05 18:30:00');

INSERT INTO Ticket (
    ticket_id, card_type, card_number, name_on_card,
    card_exp_date, purchase_date_time,
    customer_email, airline_name, flight_num, departure_date_time
) VALUES
(1289, 'debit', '123', '123',
 '2027-03-01', '2025-12-04 23:27:58',
 'test2@test.com', 'Jet Blue', 'JB3597', '2026-03-01 22:20:00'),

(2522, 'debit', '123455667', 'Andera Gonzalez',
 '2033-04-01', '2025-12-01 19:25:44',
 'ag8754@nyu.edu', 'Jet Blue', 'JB3597', '2026-03-01 22:20:00'),

(3125, 'debit', '123456', 'Andrea Gonzalez',
 '2028-02-01', '2025-12-02 23:06:13',
 'ag8754@nyu.edu', 'United', 'UA255', '2026-01-03 05:30:00'),

(3345, 'debit', '1234567', 'Andrea Gonzalez',
 '2028-09-13', '2025-11-21 22:15:22',
 'ag8754@nyu.edu', 'Jet Blue', 'JB3597', '2026-03-01 22:20:00'),

(4703, 'debit', '12312372', 'LOLA',
 '0004-12-01', '2025-12-04 23:36:43',
 'lola@email.com', 'United', 'UA255', '2026-01-03 05:30:00'),

(6971, 'debit', '123435646', 'Andrea Gonzalez',
 '2028-03-01', '2025-12-01 19:48:58',
 'ag8754@nyu.edu', 'Emirates', 'EK205', '2025-12-28 08:30:00'),

(7170, 'debit', '123456', 'Andrea Gonzalez',
 '2029-03-01', '2025-12-04 21:52:11',
 'ag8754@nyu.edu', 'Air France', 'AF341', '2025-12-10 10:00:00'),

(7493, 'debit', '12345678', 'Andera Gonzalez',
 '2029-03-01', '2025-12-01 19:23:08',
 'ag8754@nyu.edu', 'Air France', '61983286426849401608', '2025-12-01 04:21:00'),

(8291, 'debit', '122', 'test',
 '2036-07-01', '2025-12-04 22:33:58',
 'test2@test.com', 'Air France', 'AF341', '2025-12-10 10:00:00'),

(9154, 'debit', '123456789', 'Andera Gonzalez',
 '2028-07-01', '2025-12-01 19:22:48',
 'ag8754@nyu.edu', 'Air France', '61983286426849401608', '2025-12-01 04:21:00'),

(9528, 'debit', '12345566', 'Andera Gonzalez',
 '2028-06-01', '2025-12-01 19:36:18',
 'ag8754@nyu.edu', 'Air France', 'AF340', '2025-12-01 16:00:00'),

(12345, 'debit', '1234567', 'Andrea Gonzalez',
 '2028-09-13', '2025-11-21 21:21:33',
 'ag8754@nyu.edu', 'Jet Blue', 'JB3467', '2025-11-05 18:30:00');


