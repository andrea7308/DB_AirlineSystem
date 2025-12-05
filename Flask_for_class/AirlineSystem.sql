-- CREATE TABLES
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

CREATE TABLE Airplane (
    num_of_seats INT,
    manufacture_comp VARCHAR(20),
    age INT, 
    airplane_id VARCHAR(20),
    airline_name VARCHAR(20),	
    PRIMARY KEY(airplane_id, airline_name),
    FOREIGN KEY (airline_name) REFERENCES Airline(airline_name)
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

-- INSERT STATEMENTS
INSERT INTO Airline(airline_name) VALUES ('Jet Blue');
INSERT INTO Airline(airline_name) VALUES ('American Airlines');
INSERT INTO Airline(airline_name) VALUES ('United');
INSERT INTO Airline(airline_name) VALUES ('Southwest');
INSERT INTO Airline(airline_name) VALUES ('Alaska');
INSERT INTO Airline(airline_name) VALUES ('Emirates');
INSERT INTO Airline(airline_name) VALUES ('Air France');
INSERT INTO Airline(airline_name) VALUES ('Delta Air Lines');

INSERT INTO Airport(airport_code, airport_city, airport_country, airport_type) VALUES ('JFK', 'New York City', 'United States', 'domestic');
INSERT INTO Airport(airport_code, airport_city, airport_country, airport_type) VALUES ('LGA', 'New York City', 'United States', 'domestic');
INSERT INTO Airport(airport_code, airport_city, airport_country, airport_type) VALUES ('SFO', 'San Francisco', 'United States', 'domestic');
INSERT INTO Airport(airport_code, airport_city, airport_country, airport_type) VALUES ('IAH', 'Houston', 'United States', 'domestic');
INSERT INTO Airport(airport_code, airport_city, airport_country, airport_type) VALUES ('SJU', 'San Juan', 'United States', 'domestic');
INSERT INTO Airport(airport_code, airport_city, airport_country, airport_type) VALUES ('DBX', 'Dubai', 'United Arab Emirates', 'international');
INSERT INTO Airport(airport_code, airport_city, airport_country, airport_type) VALUES ('PVG', 'Shanghai', 'China', 'international');
INSERT INTO Airport(airport_code, airport_city, airport_country, airport_type) VALUES ('HND', 'Tokyo', 'Japan', 'international');

INSERT INTO Customer(customer_email, first_name, last_name, password, building_num, street, city, state, phone_number, passport_num, passport_expiration, passport_country, dob) VALUES 
('marybrad@gmail.com', 'Marilyn', 'Bradshaw', 'password123', 370, 'Jay Street', 'Brooklyn', 'New York', '0123456789', 'a12345678', '2030-12-01', 'United States', '2004-02-05'),
('lvegs56@gmail.com', 'Lucinda', 'Vega', 'password456', 370, 'Jay Street', 'Brooklyn', 'New York', '9876543210', 'b12345678', '2029-07-15', 'United States', '2003-12-13'),
('bradtheman@gmail.com', 'Brad', 'Cooper', 'password789', 370, 'Jay Street', 'Brooklyn', 'New York', '2345678901', 'c12345678', '2040-03-14', 'United States', '2003-07-15');

INSERT INTO Airplane(num_of_seats, manufacture_comp, age, airplane_id, airline_name) VALUES 
(180, 'Boeing', 20, 'N303ZS', 'Jet Blue'),
(150, 'Airbus', 15, 'N326CS', 'Jet Blue'),
(300, 'Boeing', 25, 'N303ZS', 'Delta Air Lines'),
(180, 'Boeing', 20, 'N333PK', 'United'),
(150, 'Airbus', 15, 'N123GS', 'United'),
(300, 'Boeing', 25, 'N365LS', 'Southwest'),
(180, 'Boeing', 20, 'N378PS', 'Alaska'),
(150, 'Airbus', 15, 'N326RH', 'Emirates'),
(300, 'Boeing', 25, 'N303ZS', 'Air France');

INSERT INTO Airline_Staff(username, password, first_name, last_name, DOB, airlinestaff_email, airline_name)
VALUES ('kimb23', 'password123', 'Kim', 'Bernard', '2000-04-13', 'kimb23@gmail.com', 'Jet Blue');

INSERT INTO Flight(airplane_id, flight_num, departure_date_time, arrival_date_time, dept_airport, arr_airport, flight_price, flight_status, airline_name) VALUES
('N303ZS', 'JB3467','2025-11-05 22:00:00', 'LGA', 'IAH', 345.77, 'on-time', 'Jet Blue'),
('N326CS', 'JB3322', '2025-12-23 06:00:00', '2025-12-23 13:00:00', 'DBX', 'LGA', 1346.89, 'delayed', 'Jet Blue'),
('N326CS', 'JB3597', '2026-03-01 22:20:00', '2026-03-02 02:05:00', 'PVG', 'JFK', 79.55, 'on-time', 'Jet Blue');

INSERT INTO Ticket(ticket_id, customer_email, card_type, card_number, name_on_card, card_exp_date, purchase_date_time) VALUES
(2790314569333, 'marybrad@gmail.com', 'credit', '378282246310005', 'Marilyn Bradshaw', '2027-09-30', '2025-09-30 03:22:08'),
(2790314543411, 'lvegs56@gmail.com', 'debit', '4111111111111111', 'Lucinda Vega', '2028-10-30', '2025-10-30 10:13:40'),
(2790314567677, 'bradtheman@gmail.com', 'credit', '371449635398431', 'Brad Cooper', '2026-10-30', '2025-10-30 17:00:01');

-- QUERIES
-- a. Show all future flights
SELECT * FROM Flight;

-- b. Show all delayed flights
SELECT airline_name, flight_num, departure_date_time
FROM Flight
WHERE flight_status = 'delayed';

-- c. Show customer names who bought tickets
SELECT c.first_name, c.last_name
FROM Ticket t
JOIN Customer c ON c.customer_email = t.customer_email;

-- d. Show airplanes owned by Jet Blue
SELECT airplane_id, num_of_seats, manufacture_comp
FROM Airplane
WHERE airline_name = 'Jet Blue';


