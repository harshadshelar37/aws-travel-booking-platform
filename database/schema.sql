CREATE TABLE IF NOT EXISTS Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS Flights (
    flight_id INT AUTO_INCREMENT PRIMARY KEY,
    flight_name VARCHAR(100) NOT NULL,
    source VARCHAR(100) NOT NULL,
    destination VARCHAR(100) NOT NULL,
    departure DATETIME NOT NULL,
    arrival DATETIME NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    available_seats INT NOT NULL
);

CREATE TABLE IF NOT EXISTS Hotels (
    hotel_id INT AUTO_INCREMENT PRIMARY KEY,
    hotel_name VARCHAR(150) NOT NULL,
    city VARCHAR(100) NOT NULL,
    rating DECIMAL(2, 1) DEFAULT 0.0,
    price DECIMAL(10, 2) NOT NULL,
    rooms INT NOT NULL
);

CREATE TABLE IF NOT EXISTS Cab_Services (
    cab_id INT AUTO_INCREMENT PRIMARY KEY,
    cab_name VARCHAR(100) NOT NULL,
    driver VARCHAR(100) NOT NULL,
    location VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    status ENUM('Available', 'Booked', 'Maintenance') DEFAULT 'Available'
);

CREATE TABLE IF NOT EXISTS Holiday_Packages (
    package_id INT AUTO_INCREMENT PRIMARY KEY,
    package_name VARCHAR(150) NOT NULL,
    days INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS Bookings (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    booking_type ENUM('Flight', 'Hotel', 'Cab', 'Package') NOT NULL,
    reference_id INT NOT NULL, -- Refers to flight_id, hotel_id, etc. based on type
    booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('Pending', 'Confirmed', 'Cancelled') DEFAULT 'Pending',
    payment_status ENUM('Unpaid', 'Paid', 'Refunded') DEFAULT 'Unpaid',
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id INT,
    amount DECIMAL(10, 2) NOT NULL,
    payment_mode ENUM('Credit Card', 'Debit Card', 'UPI', 'Net Banking') NOT NULL,
    status ENUM('Success', 'Failed', 'Pending') DEFAULT 'Pending',
    transaction_id VARCHAR(100) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (booking_id) REFERENCES Bookings(booking_id) ON DELETE CASCADE
);
