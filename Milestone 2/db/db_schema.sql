CREATE TABLE airlines (
    airline_id INT AUTO_INCREMENT PRIMARY KEY ,
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
INSERT INTO airlines (
    airline_id, airline_code, origin_city, destination_city,
    departure_time, arrival_time, ticket_price, capacity, available_seats, operator_name
) VALUES
(6, 'AL006', 'Hyderabad', 'Chennai', '2025-03-02 06:30:00', '2025-03-02 07:40:00', 4200.00, 180, 170, 'IndiGo'),
(7, 'AL007', 'Chennai', 'Mumbai', '2025-03-02 08:30:00', '2025-03-02 10:30:00', 6500.00, 200, 190, 'Air India'),
(8, 'AL008', 'Mumbai', 'Ahmedabad', '2025-03-02 11:30:00', '2025-03-02 12:45:00', 3800.00, 180, 160, 'GoAir'),
(9, 'AL009', 'Ahmedabad', 'Jaipur', '2025-03-02 13:30:00', '2025-03-02 14:45:00', 4100.00, 150, 145, 'SpiceJet'),
(10, 'AL010', 'Jaipur', 'Delhi', '2025-03-02 15:30:00', '2025-03-02 16:30:00', 3500.00, 160, 155, 'Vistara'),
(11, 'AL011', 'Delhi', 'Mumbai', '2025-03-03 06:00:00', '2025-03-03 08:00:00', 7000.00, 200, 185, 'Air India'),
(12, 'AL012', 'Mumbai', 'Goa', '2025-03-03 09:00:00', '2025-03-03 10:15:00', 5200.00, 180, 178, 'IndiGo'),
(13, 'AL013', 'Goa', 'Hyderabad', '2025-03-03 11:30:00', '2025-03-03 12:45:00', 4600.00, 180, 172, 'SpiceJet'),
(14, 'AL014', 'Hyderabad', 'Delhi', '2025-03-03 13:30:00', '2025-03-03 15:45:00', 7200.00, 200, 192, 'Vistara'),
(15, 'AL015', 'Delhi', 'Chennai', '2025-03-03 16:30:00', '2025-03-03 18:45:00', 6800.00, 200, 197, 'GoAir'),
(16, 'AL016', 'Bengaluru', 'Delhi', '2025-03-04 06:30:00', '2025-03-04 08:45:00', 7100.00, 200, 180, 'Air India'),
(17, 'AL017', 'Delhi', 'Dubai', '2025-03-04 09:30:00', '2025-03-04 12:00:00', 14500.00, 220, 210, 'Emirates'),
(18, 'AL018', 'Dubai', 'Mumbai', '2025-03-04 13:30:00', '2025-03-04 18:00:00', 14200.00, 220, 215, 'Air India'),
(19, 'AL019', 'Mumbai', 'Singapore', '2025-03-04 19:00:00', '2025-03-05 02:00:00', 21500.00, 250, 240, 'Singapore Airlines'),
(20, 'AL020', 'Singapore', 'Chennai', '2025-03-05 06:00:00', '2025-03-05 10:00:00', 19800.00, 250, 230, 'IndiGo'),
(21, 'AL021', 'Chennai', 'Kuala Lumpur', '2025-03-06 08:00:00', '2025-03-06 13:00:00', 17200.00, 220, 215, 'AirAsia'),
(22, 'AL022', 'Kuala Lumpur', 'Hyderabad', '2025-03-06 15:00:00', '2025-03-06 18:30:00', 16000.00, 200, 190, 'Malaysia Airlines'),
(23, 'AL023', 'Hyderabad', 'Colombo', '2025-03-07 07:00:00', '2025-03-07 09:00:00', 10500.00, 180, 172, 'SriLankan Airlines'),
(24, 'AL024', 'Colombo', 'Delhi', '2025-03-07 10:30:00', '2025-03-07 14:00:00', 12500.00, 200, 190, 'Vistara'),
(25, 'AL025', 'Delhi', 'London', '2025-03-08 02:00:00', '2025-03-08 10:30:00', 48500.00, 300, 295, 'British Airways');

SELECT * FROM airlines;

CREATE TABLE reservations (
    reservation_id INTEGER PRIMARY KEY AUTO_INCREMENT,
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
(3, 'TXN103', 'AL004', 'Delhi', 'Kolkata', 'Kiran Das', '9123456789', 6),
(4, 'TXN104', 'AL002', 'Bengaluru', 'Pune', 'Anjali Mehta', '9090909090', 18),
(5, 'TXN105', 'AL005', 'Kolkata', 'Hyderabad', 'Vikram Singh', '9876001234', 45),
(6, 'TXN106', 'AL007', 'Chennai', 'Mumbai', 'Sneha Patel', '9123004567', 27),
(7, 'TXN107', 'AL009', 'Ahmedabad', 'Jaipur', 'Rajesh Verma', '9811122233', 14),
(8, 'TXN108', 'AL010', 'Jaipur', 'Delhi', 'Divya Nair', '9000765432', 10),
(9, 'TXN109', 'AL012', 'Mumbai', 'Goa', 'Abdul Rahman', '9998877665', 5),
(10, 'TXN110', 'AL014', 'Hyderabad', 'Delhi', 'Tanya Sharma', '9888777666', 39),
(11, 'TXN111', 'AL016', 'Bengaluru', 'Delhi', 'Praveen Rao', '9776655443', 9),
(12, 'TXN112', 'AL017', 'Delhi', 'Dubai', 'Farah Khan', '9898989898', 56),
(13, 'TXN113', 'AL019', 'Mumbai', 'Singapore', 'Arjun Malhotra', '9011223344', 78),
(14, 'TXN114', 'AL023', 'Hyderabad', 'Colombo', 'Roshni Perera', '9080706050', 34),
(15, 'TXN115', 'AL025', 'Delhi', 'London', 'David Williams', '9700112233', 102),
(16, 'TXN116', 'AL001', 'Hyderabad', 'Bengaluru', 'Karthik Reddy', '9876500012', 21),
(17, 'TXN117', 'AL002', 'Bengaluru', 'Pune', 'Priya Sharma', '9822113344', 32),
(18, 'TXN118', 'AL003', 'Pune', 'Delhi', 'Rahul Joshi', '9012233445', 15),
(19, 'TXN119', 'AL005', 'Kolkata', 'Hyderabad', 'Aditi Rao', '9123456700', 58),
(20, 'TXN120', 'AL007', 'Chennai', 'Mumbai', 'Rohan Gupta', '9890123456', 42),
(21, 'TXN121', 'AL009', 'Ahmedabad', 'Jaipur', 'Simran Kaur', '9990001112', 17),
(22, 'TXN122', 'AL012', 'Mumbai', 'Goa', 'Neeraj Kumar', '9887766554', 28),
(23, 'TXN123', 'AL016', 'Bengaluru', 'Delhi', 'Sandeep Nair', '9765432100', 8),
(24, 'TXN124', 'AL017', 'Delhi', 'Dubai', 'Fatima Sheikh', '9811223344', 63),
(25, 'TXN125', 'AL019', 'Mumbai', 'Singapore', 'Anand Pillai', '9955443322', 82);

CREATE TABLE airline (
    airline_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    airline_code VARCHAR(10) UNIQUE,
    origin_city VARCHAR(50) NOT NULL,
    destination_city VARCHAR(50) NOT NULL,
    available_seats INT CHECK (available_seats >= 0),
    ticket_price DECIMAL(10,2) DEFAULT 4000
);

CREATE TABLE reservation (
    reservation_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    airline_id INT,
    passenger_name VARCHAR(50) NOT NULL,
    seat_number INT,
    FOREIGN KEY (airline_id) REFERENCES airline(airline_id),
    UNIQUE (airline_id, seat_number)
);

INSERT INTO airline (airline_code, origin_city, destination_city, available_seats, ticket_price) VALUES
('AL001', 'Hyderabad', 'Bengaluru', 160, 4500.00),
('AL002', 'Bengaluru', 'Pune', 175, 4800.00),
('AL003', 'Pune', 'Delhi', 190, 7200.00),
('AL004', 'Delhi', 'Kolkata', 180, 6800.00),
('AL005', 'Kolkata', 'Hyderabad', 195, 6000.00),
('AL006', 'Hyderabad', 'Chennai', 170, 4200.00),
('AL007', 'Chennai', 'Mumbai', 190, 6500.00),
('AL008', 'Mumbai', 'Ahmedabad', 160, 3800.00),
('AL009', 'Ahmedabad', 'Jaipur', 145, 4100.00),
('AL010', 'Jaipur', 'Delhi', 155, 3500.00),
('AL011', 'Delhi', 'Mumbai', 185, 7000.00),
('AL012', 'Mumbai', 'Goa', 178, 5200.00),
('AL013', 'Goa', 'Hyderabad', 172, 4600.00),
('AL014', 'Hyderabad', 'Delhi', 192, 7200.00),
('AL015', 'Delhi', 'Chennai', 197, 6800.00),
('AL016', 'Bengaluru', 'Delhi', 180, 7100.00),
('AL017', 'Delhi', 'Dubai', 210, 14500.00),
('AL018', 'Dubai', 'Mumbai', 215, 14200.00),
('AL019', 'Mumbai', 'Singapore', 240, 21500.00),
('AL020', 'Singapore', 'Chennai', 230, 19800.00),
('AL021', 'Chennai', 'Kuala Lumpur', 215, 17200.00),
('AL022', 'Kuala Lumpur', 'Hyderabad', 190, 16000.00),
('AL023', 'Hyderabad', 'Colombo', 172, 10500.00),
('AL024', 'Colombo', 'Delhi', 190, 12500.00),
('AL025', 'Delhi', 'London', 295, 48500.00);

INSERT INTO reservation (airline_id, passenger_name, seat_number) VALUES
(1, 'Ravi Kumar', 12),
(2, 'Anjali Mehta', 18),
(3, 'Megha Reddy', 24),
(4, 'Kiran Das', 6),
(5, 'Vikram Singh', 45),
(6, 'Sneha Patel', 27),
(7, 'Rajesh Verma', 14),
(8, 'Divya Nair', 10),
(9, 'Abdul Rahman', 5),
(10, 'Tanya Sharma', 39),
(11, 'Praveen Rao', 9),
(12, 'Farah Khan', 56),
(13, 'Arjun Malhotra', 78),
(14, 'Roshni Perera', 34),
(15, 'David Williams', 102),
(16, 'Karthik Reddy', 21),
(17, 'Priya Sharma', 32),
(18, 'Rahul Joshi', 15),
(19, 'Aditi Rao', 58),
(20, 'Rohan Gupta', 42),
(21, 'Simran Kaur', 17),
(22, 'Neeraj Kumar', 28),
(23, 'Sandeep Nair', 8),
(24, 'Fatima Sheikh', 63),
(25, 'Anand Pillai', 82);
