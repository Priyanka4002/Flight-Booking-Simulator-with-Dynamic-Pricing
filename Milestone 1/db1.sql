create database flight_booking;
use flight_booking;

CREATE TABLE airlines (
    airline_id INTEGER PRIMARY KEY,
    airline_code VARCHAR(10),
    origin_city VARCHAR(50),
    destination_city VARCHAR(50),
    departure_time DATETIME,
    arrival_time DATETIME,
    ticket_price DECIMAL(10, 2),
    capacity INT,
    available_seats INT,
    operator_name VARCHAR(20)
);

INSERT INTO airlines (
    airline_id, airline_code, origin_city, destination_city,
    departure_time, arrival_time, ticket_price, capacity, available_seats, operator_name
) VALUES
(1, 'AL001', 'Hyderabad', 'Bengaluru', '2025-03-01 07:00:00', '2025-03-01 08:15:00', 4500.00, 180, 160, 'Air India'),
(2, 'AL002', 'Bengaluru', 'Pune', '2025-03-01 09:00:00', '2025-03-01 10:30:00', 4800.00, 180, 175, 'IndiGo'),
(3, 'AL003', 'Pune', 'Delhi', '2025-03-01 11:00:00', '2025-03-01 13:15:00', 7200.00, 200, 190, 'SpiceJet'),
(4, 'AL004', 'Delhi', 'Kolkata', '2025-03-01 14:00:00', '2025-03-01 16:00:00', 6800.00, 200, 180, 'Vistara'),
(5, 'AL005', 'Kolkata', 'Hyderabad', '2025-03-01 17:00:00', '2025-03-01 19:00:00', 6000.00, 200, 195, 'GoAir');

SELECT * FROM airlines;

SELECT airline_id, airline_code, origin_city, destination_city, ticket_price
FROM airlines;

/* Update */
UPDATE airlines
SET available_seats = 150
WHERE airline_id = 5;

/* Delete */
DELETE FROM airlines
WHERE airline_id = 2;

/* ORDER BY */
SELECT airline_code, ticket_price
FROM airlines
ORDER BY ticket_price ASC;

SELECT airline_code, departure_time
FROM airlines
ORDER BY departure_time DESC;

/* WHERE */
SELECT *
FROM airlines
WHERE origin_city = 'Delhi';

SELECT airline_code, ticket_price
FROM airlines
WHERE ticket_price > 5000;

/* LIMIT */
SELECT airline_code, ticket_price
FROM airlines
ORDER BY ticket_price ASC
LIMIT 3;

/* AGGREGATE FUNCTIONS */
SELECT COUNT(*) AS total_airlines FROM airlines;
SELECT AVG(ticket_price) AS avg_ticket_price FROM airlines WHERE origin_city = 'Hyderabad';

/* GROUP BY */
SELECT origin_city, AVG(ticket_price) AS avg_ticket_price FROM airlines GROUP BY origin_city;
SELECT origin_city, AVG(ticket_price) AS avg_ticket_price FROM airlines GROUP BY origin_city HAVING AVG(ticket_price) < 6000;

/* Create reservations table */
CREATE TABLE reservations (
    reservation_id INTEGER AUTO_INCREMENT PRIMARY KEY,
    transaction_id VARCHAR(20),
    airline_code VARCHAR(10),
    origin_city VARCHAR(50),
    destination_city VARCHAR(50),
    passenger_name VARCHAR(50),
    contact_number VARCHAR(15),
    seat_number INT
);

INSERT INTO reservations (
    reservation_id, transaction_id, airline_code, origin_city, destination_city,
    passenger_name, contact_number, seat_number
) VALUES
(1, 'TXN101', 'AL001', 'Hyderabad', 'Bengaluru', 'Ravi Kumar', '9876543210', 12),
(2, 'TXN102', 'AL003', 'Pune', 'Delhi', 'Megha Reddy', '9988776655', 24),
(3, 'TXN103', 'AL004', 'Delhi', 'Kolkata', 'Kiran Das', '9123456789', 6);

/* Joins */

/* Inner Join */
SELECT r.passenger_name, a.airline_code, a.origin_city, a.destination_city
FROM reservations r
INNER JOIN airlines a ON r.airline_code = a.airline_code;

/* Left Join */
SELECT a.airline_code, a.origin_city, a.destination_city, r.passenger_name
FROM airlines a
LEFT JOIN reservations r ON a.airline_code = r.airline_code;

/* Full Outer Join Simulation using UNION */
SELECT a.airline_code, r.passenger_name
FROM airlines a
LEFT JOIN reservations r ON a.airline_code = r.airline_code
UNION
SELECT a.airline_code, r.passenger_name
FROM reservations r
LEFT JOIN airlines a ON a.airline_code = r.airline_code;

/* Transactions */
BEGIN;
SELECT available_seats FROM airlines WHERE airline_id = 1;
UPDATE airlines
SET available_seats = available_seats - 1
WHERE airline_id = 1;

INSERT INTO reservations (airline_code, passenger_name, seat_number)
VALUES ('AL001', 'Sanjana Rao', 25);

select *from reservations;
--COMMIT

/* Constraints */
CREATE TABLE airline (
    airline_id INTEGER AUTO_INCREMENT PRIMARY KEY ,
    airline_code VARCHAR(10) UNIQUE,
    origin_city VARCHAR(50) NOT NULL,
    destination_city VARCHAR(50) NOT NULL,
    available_seats INT CHECK (available_seats >= 0),
    ticket_price DECIMAL(10,2) DEFAULT 4000
);



CREATE TABLE reservation (
    reservation_id INTEGER AUTO_INCREMENT PRIMARY KEY,
    airline_id INT,
    passenger_name VARCHAR(50) NOT NULL,
    seat_number INT UNIQUE,
    FOREIGN KEY (airline_id) REFERENCES airline(airline_id)
);


Insert into airline values(11,'C1','gannavaram','hyderabad',50,125);
INSERT INTO airline (airline_code, origin_city, destination_city, available_seats, ticket_price)
VALUES
('AI101', 'Hyderabad', 'Delhi', 120, 5500),
('AI102', 'Delhi', 'Mumbai', 150, 6000),
('AI103', 'Mumbai', 'Chennai', 100, 4800),
('AI104', 'Chennai', 'Kolkata', 90, 4500),
('AI105', 'Kolkata', 'Hyderabad', 80, 5000);

select *from airline;

INSERT INTO reservation (airline_id, passenger_name, seat_number)
VALUES
(11,'Priya Reddy', 12),
(12, 'Rahul Sharma', 15),
(13, 'Sneha Verma', 18),
(14, 'Vikram Rao', 22),
(15, 'Pooja Nair', 25),
(16, 'Arjun Das', 30);

select *from reservation;




