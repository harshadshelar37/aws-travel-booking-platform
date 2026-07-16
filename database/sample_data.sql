-- Sample Users (Password is 'password123' hashed, here just plain or mock hash for testing)
INSERT INTO Users (name, email, password, phone) VALUES
('John Doe', 'john@example.com', 'hashed_pass_1', '1234567890'),
('Alice Smith', 'alice@example.com', 'hashed_pass_2', '0987654321');

-- Sample Flights
INSERT INTO Flights (flight_name, source, destination, departure, arrival, price, available_seats) VALUES
('Airbus A320', 'New York', 'London', '2025-10-01 08:00:00', '2025-10-01 20:00:00', 450.00, 150),
('Boeing 737', 'Los Angeles', 'Tokyo', '2025-11-05 10:00:00', '2025-11-06 14:00:00', 800.00, 200),
('Emirates A380', 'Dubai', 'Paris', '2025-12-15 09:00:00', '2025-12-15 14:00:00', 600.00, 300);

-- Sample Hotels
INSERT INTO Hotels (hotel_name, city, rating, price, rooms) VALUES
('The Plaza Hotel', 'New York', 4.8, 250.00, 50),
('Hilton Tokyo', 'Tokyo', 4.5, 180.00, 100),
('Ritz Paris', 'Paris', 4.9, 500.00, 30);

-- Sample Cabs
INSERT INTO Cab_Services (cab_name, driver, location, price, status) VALUES
('NYC Yellow Cab', 'Mike Johnson', 'New York', 50.00, 'Available'),
('Tokyo Taxi', 'Kenji Sato', 'Tokyo', 40.00, 'Available'),
('Paris Chauffeur', 'Jean Dupont', 'Paris', 80.00, 'Available');

-- Sample Holiday Packages
INSERT INTO Holiday_Packages (package_name, days, price, description) VALUES
('NYC Weekend Getaway', 3, 1200.00, 'Enjoy 3 days in the Big Apple including hotel and flights.'),
('Tokyo Explorer', 7, 2500.00, 'A full week exploring the vibrant city of Tokyo.'),
('Romantic Paris', 5, 2000.00, '5 days of romance in the city of lights.');
