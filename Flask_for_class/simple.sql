-- (code, city, country, airport_type (can be 'domestic', 'international', 'domestic/international'))
-- Below are the inserts for the Airports in 'A':
INSERT INTO Airport VALUES ('ONE', '1', 'A', 'domestic');
INSERT INTO Airport VALUES ('TWO', '2', 'A', 'domestic');
INSERT INTO Airport VALUES ('THREE', '3', 'A', 'domestic/international');
INSERT INTO Airport VALUES ('FOUR', '4', 'A', 'international');

-- B:
INSERT INTO Airport VALUES ('FIVE', '5', 'B', 'domestic/international');
INSERT INTO Airport VALUES ('SIX', '6', 'B', 'domestic');
-- C:
INSERT INTO Airport VALUES ('SEVEN', '7', 'C', 'domestic/international');
INSERT INTO Airport VALUES ('EIGHT', '8', 'C', 'domestic');



-- Airlines in my imaginary system:
INSERT INTO Airline VALUES ('rho');
INSERT INTO Airline VALUES ('gamma');
INSERT INTO Airline VALUES ('chi');



-- Insert values into Airplane in order to test
-- (num of seats, manufacture comp, age, id, name (this is the name of the airline which owns it))
INSERT INTO Airplane VALUES (3, 'Mango', 20, 100, 'rho');
INSERT INTO Airplane VALUES (180, 'Boeing', 19, 1011, 'rho');
INSERT INTO Airplane VALUES (150, 'Airbus', 18, 200, 'gamma');
INSERT INTO Airplane VALUES (180, 'Boeing', 17, 2022, 'gamma');
INSERT INTO Airplane VALUES (150, 'Airbus', 21, 300, 'chi');
INSERT INTO Airplane VALUES (180, 'Boeing', 11, 3033, 'chi');