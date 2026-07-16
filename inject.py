import yaml

with open('travel_booking_platform.yaml', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the start of the files section under setup:
start_idx = -1
end_idx = -1
for i, line in enumerate(lines):
    if line.strip() == "files:" and "setup:" in "".join(lines[i-5:i]):
        start_idx = i
    if line.strip() == "commands:" and start_idx != -1 and end_idx == -1:
        end_idx = i
        break

if start_idx == -1 or end_idx == -1:
    print("Could not find files: or commands: section")
    exit(1)

new_files_content = """          files:
            /etc/nginx/nginx.conf:
              content: |
                user nginx;
                worker_processes auto;
                error_log /var/log/nginx/error.log notice;
                pid /run/nginx.pid;
                include /usr/share/nginx/modules/*.conf;
                events {
                    worker_connections 1024;
                }
                http {
                    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                                      '$status $body_bytes_sent "$http_referer" '
                                      '"$http_user_agent" "$http_x_forwarded_for"';
                    access_log  /var/log/nginx/access.log  main;
                    sendfile            on;
                    tcp_nopush          on;
                    keepalive_timeout   65;
                    types_hash_max_size 4096;
                    include             /etc/nginx/mime.types;
                    default_type        application/octet-stream;
                    include /etc/nginx/conf.d/*.conf;
                }
              mode: '000644'
              owner: 'root'
              group: 'root'
            /home/ec2-user/app/backend/schema.sql:
              content: |
                CREATE DATABASE IF NOT EXISTS travel_db;
                USE travel_db;

                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS flights (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    airline VARCHAR(100) NOT NULL,
                    origin VARCHAR(10) NOT NULL,
                    destination VARCHAR(10) NOT NULL,
                    departure_time DATETIME NOT NULL,
                    arrival_time DATETIME NOT NULL,
                    price DECIMAL(10,2) NOT NULL,
                    class_type VARCHAR(50) DEFAULT 'Economy',
                    duration VARCHAR(50)
                );

                CREATE TABLE IF NOT EXISTS hotels (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    location VARCHAR(255) NOT NULL,
                    rating DECIMAL(3,1) DEFAULT 4.0,
                    price_per_night DECIMAL(10,2) NOT NULL,
                    amenities TEXT
                );

                CREATE TABLE IF NOT EXISTS cabs (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    type VARCHAR(100) NOT NULL,
                    driver_name VARCHAR(255),
                    price_per_km DECIMAL(10,2) NOT NULL,
                    availability BOOLEAN DEFAULT TRUE
                );

                CREATE TABLE IF NOT EXISTS packages (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    destination VARCHAR(255) NOT NULL,
                    days INT NOT NULL,
                    price DECIMAL(10,2) NOT NULL,
                    includes TEXT
                );

                CREATE TABLE IF NOT EXISTS bookings (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    service_type VARCHAR(50) NOT NULL,
                    service_id INT NOT NULL,
                    total_price DECIMAL(10,2) NOT NULL,
                    status VARCHAR(50) DEFAULT 'Confirmed',
                    booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                );
              mode: '000644'
              owner: 'ec2-user'
              group: 'ec2-user'
            /home/ec2-user/app/backend/seed.py:
              content: |
                import os
                import mysql.connector
                import random
                from datetime import datetime, timedelta
                
                DB_HOST = os.getenv("DB_HOST", "localhost")
                DB_USER = os.getenv("DB_USER", "root")
                DB_PASS = os.getenv("DB_PASS", "")
                
                try:
                    conn = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASS)
                    cursor = conn.cursor()
                    
                    # Execute Schema
                    with open('/home/ec2-user/app/backend/schema.sql', 'r') as f:
                        sql_script = f.read()
                        
                    for statement in sql_script.split(';'):
                        if statement.strip():
                            cursor.execute(statement)
                    
                    # Seed Flights
                    cursor.execute("SELECT COUNT(*) FROM travel_db.flights")
                    if cursor.fetchone()[0] == 0:
                        airlines = ["IndiGo", "Air India", "Vistara", "SpiceJet", "Akasa Air"]
                        cities = ["DEL", "BOM", "BLR", "HYD", "MAA", "CCU", "PNQ", "GOI"]
                        print("Seeding flights...")
                        for _ in range(500):
                            origin = random.choice(cities)
                            dest = random.choice([c for c in cities if c != origin])
                            departure = datetime.now() + timedelta(days=random.randint(1, 30), hours=random.randint(1, 23))
                            arrival = departure + timedelta(hours=random.randint(1, 4), minutes=random.randint(0, 59))
                            duration = f"{(arrival - departure).seconds // 3600}h {((arrival - departure).seconds // 60) % 60}m"
                            price = round(random.uniform(2500, 15000), 2)
                            airline = random.choice(airlines)
                            cursor.execute(
                                "INSERT INTO travel_db.flights (airline, origin, destination, departure_time, arrival_time, price, duration) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                                (airline, origin, dest, departure, arrival, price, duration)
                            )
                    
                    # Seed Hotels
                    cursor.execute("SELECT COUNT(*) FROM travel_db.hotels")
                    if cursor.fetchone()[0] == 0:
                        print("Seeding hotels...")
                        cities = ["Delhi", "Mumbai", "Bangalore", "Hyderabad", "Chennai", "Kolkata", "Pune", "Goa"]
                        hotel_prefixes = ["Taj", "Oberoi", "ITC", "Radisson", "Marriott", "Hyatt", "Novotel", "Lemon Tree"]
                        for _ in range(200):
                            name = f"{random.choice(hotel_prefixes)} {random.choice(['Grand', 'Palace', 'Residency', 'Suites', 'Resort'])}"
                            location = random.choice(cities)
                            rating = round(random.uniform(3.5, 5.0), 1)
                            price = round(random.uniform(1500, 25000), 2)
                            amenities = "WiFi, Pool, Spa, Breakfast"
                            cursor.execute(
                                "INSERT INTO travel_db.hotels (name, location, rating, price_per_night, amenities) VALUES (%s, %s, %s, %s, %s)",
                                (name, location, rating, price, amenities)
                            )

                    # Seed Cabs
                    cursor.execute("SELECT COUNT(*) FROM travel_db.cabs")
                    if cursor.fetchone()[0] == 0:
                        print("Seeding cabs...")
                        types = ["Sedan", "SUV", "Hatchback", "Luxury"]
                        for i in range(100):
                            ctype = random.choice(types)
                            price = round(random.uniform(12.0, 35.0), 2)
                            cursor.execute(
                                "INSERT INTO travel_db.cabs (type, driver_name, price_per_km) VALUES (%s, %s, %s)",
                                (ctype, f"Driver {i}", price)
                            )
                            
                    # Seed Packages
                    cursor.execute("SELECT COUNT(*) FROM travel_db.packages")
                    if cursor.fetchone()[0] == 0:
                        print("Seeding packages...")
                        dests = ["Goa", "Manali", "Kerala", "Andaman", "Kashmir", "Dubai", "Maldives"]
                        for _ in range(50):
                            dest = random.choice(dests)
                            days = random.randint(3, 10)
                            price = round(random.uniform(15000, 150000), 2)
                            cursor.execute(
                                "INSERT INTO travel_db.packages (destination, days, price, includes) VALUES (%s, %s, %s, %s)",
                                (dest, days, price, "Flights, Hotel, Transfers, Meals")
                            )

                    conn.commit()
                    cursor.close()
                    conn.close()
                    print("Seeding completed successfully!")
                except Exception as e:
                    print(f"Database error: {e}")
              mode: '000755'
              owner: 'ec2-user'
              group: 'ec2-user'
            /home/ec2-user/app/backend/app.py:
              content: |
                import os
                from flask import Flask, jsonify, request, send_from_directory
                import mysql.connector
                from mysql.connector import Error
                from dotenv import load_dotenv
                
                load_dotenv()
                
                app = Flask(__name__, static_folder='../frontend', static_url_path='/')
                
                DB_HOST = os.getenv("DB_HOST", "localhost")
                DB_USER = os.getenv("DB_USER", "root")
                DB_PASS = os.getenv("DB_PASS", "")
                
                def get_db_connection():
                    try:
                        conn = mysql.connector.connect(
                            host=DB_HOST,
                            user=DB_USER,
                            password=DB_PASS,
                            database="travel_db"
                        )
                        return conn
                    except Error as e:
                        print(f"Error connecting to MySQL: {e}")
                        return None
                
                @app.route('/')
                def index():
                    return app.send_static_file('index.html')
                
                @app.route('/health')
                def health():
                    return jsonify({"status": "healthy"}), 200
                
                @app.route('/api/flights', methods=['GET'])
                def get_flights():
                    conn = get_db_connection()
                    if not conn: return jsonify({"error": "Database connection failed"}), 500
                    
                    origin = request.args.get('origin', '')
                    destination = request.args.get('destination', '')
                    sort = request.args.get('sort', '')
                    
                    query = "SELECT * FROM flights WHERE 1=1"
                    params = []
                    if origin:
                        query += " AND origin = %s"
                        params.append(origin.upper())
                    if destination:
                        query += " AND destination = %s"
                        params.append(destination.upper())
                        
                    if sort == "price_asc":
                        query += " ORDER BY price ASC"
                    elif sort == "price_desc":
                        query += " ORDER BY price DESC"
                    
                    query += " LIMIT 50"
                    
                    try:
                        cursor = conn.cursor(dictionary=True)
                        cursor.execute(query, tuple(params))
                        rows = cursor.fetchall()
                        cursor.close()
                        conn.close()
                        return jsonify(rows)
                    except Exception as e:
                        return jsonify({"error": str(e)}), 500
                
                @app.route('/api/hotels', methods=['GET'])
                def get_hotels():
                    conn = get_db_connection()
                    if not conn: return jsonify({"error": "Database connection failed"}), 500
                    
                    location = request.args.get('location', '')
                    sort = request.args.get('sort', '')
                    
                    query = "SELECT * FROM hotels WHERE 1=1"
                    params = []
                    if location:
                        query += " AND location = %s"
                        params.append(location.capitalize())
                        
                    if sort == "price_asc":
                        query += " ORDER BY price_per_night ASC"
                    elif sort == "price_desc":
                        query += " ORDER BY price_per_night DESC"
                    
                    query += " LIMIT 50"
                    
                    try:
                        cursor = conn.cursor(dictionary=True)
                        cursor.execute(query, tuple(params))
                        rows = cursor.fetchall()
                        cursor.close()
                        conn.close()
                        return jsonify(rows)
                    except Exception as e:
                        return jsonify({"error": str(e)}), 500
                        
                @app.route('/api/cabs', methods=['GET'])
                def get_cabs():
                    conn = get_db_connection()
                    if not conn: return jsonify({"error": "Database connection failed"}), 500
                    try:
                        cursor = conn.cursor(dictionary=True)
                        cursor.execute("SELECT * FROM cabs LIMIT 20")
                        rows = cursor.fetchall()
                        cursor.close()
                        conn.close()
                        return jsonify(rows)
                    except Exception as e:
                        return jsonify({"error": str(e)}), 500
                        
                @app.route('/api/packages', methods=['GET'])
                def get_packages():
                    conn = get_db_connection()
                    if not conn: return jsonify({"error": "Database connection failed"}), 500
                    try:
                        cursor = conn.cursor(dictionary=True)
                        cursor.execute("SELECT * FROM packages LIMIT 20")
                        rows = cursor.fetchall()
                        cursor.close()
                        conn.close()
                        return jsonify(rows)
                    except Exception as e:
                        return jsonify({"error": str(e)}), 500
                        
                @app.route('/api/book', methods=['POST'])
                def book_service():
                    data = request.json
                    conn = get_db_connection()
                    if not conn: return jsonify({"error": "Database connection failed"}), 500
                    try:
                        cursor = conn.cursor()
                        cursor.execute(
                            "INSERT INTO bookings (user_id, service_type, service_id, total_price) VALUES (NULL, %s, %s, %s)",
                            (data['service_type'], data['service_id'], data['total_price'])
                        )
                        conn.commit()
                        booking_id = cursor.lastrowid
                        cursor.close()
                        conn.close()
                        return jsonify({"status": "success", "booking_id": booking_id, "message": "Booking Confirmed!"})
                    except Exception as e:
                        return jsonify({"error": str(e)}), 500

                if __name__ == '__main__':
                    app.run(host='0.0.0.0', port=5000)
              mode: '000644'
              owner: 'ec2-user'
              group: 'ec2-user'
            /home/ec2-user/app/backend/requirements.txt:
              content: |
                Flask==2.2.5
                Werkzeug==2.2.3
                mysql-connector-python==8.0.33
                python-dotenv==1.0.0
                gunicorn==21.2.0
              mode: '000644'
              owner: 'ec2-user'
              group: 'ec2-user'
            /home/ec2-user/app/frontend/index.html:
              content: |
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>WanderLust | Advanced Travel Booking</title>
                    <link rel="preconnect" href="https://fonts.googleapis.com">
                    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
                    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&display=swap" rel="stylesheet">
                    <link rel="stylesheet" href="style.css">
                    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
                </head>
                <body>
                    <header class="navbar">
                        <div class="logo"><i class="fa-solid fa-plane-departure"></i> WanderLust</div>
                        <nav>
                            <ul class="nav-links">
                                <li><a href="#" class="active" data-target="flights"><i class="fa-solid fa-plane"></i> Flights</a></li>
                                <li><a href="#" data-target="hotels"><i class="fa-solid fa-hotel"></i> Hotels</a></li>
                                <li><a href="#" data-target="cabs"><i class="fa-solid fa-taxi"></i> Cabs</a></li>
                                <li><a href="#" data-target="packages"><i class="fa-solid fa-suitcase-rolling"></i> Packages</a></li>
                            </ul>
                        </nav>
                        <div class="user-actions">
                            <button class="btn btn-outline" onclick="showModal('login')">Log In</button>
                            <button class="btn btn-primary" onclick="showModal('login')">Sign Up</button>
                        </div>
                    </header>

                    <main id="main-view">
                        <!-- Search View -->
                        <section class="hero">
                            <div class="hero-content">
                                <h1>Experience The World</h1>
                                <p>Premium flights, luxury hotels, and exclusive holiday packages all in one place.</p>
                            </div>
                        </section>

                        <section class="search-section">
                            <div class="glass-card search-container">
                                <div class="search-tabs">
                                    <button class="tab-btn active" data-target="flights">Flights</button>
                                    <button class="tab-btn" data-target="hotels">Hotels</button>
                                    <button class="tab-btn" data-target="cabs">Cabs</button>
                                    <button class="tab-btn" data-target="packages">Packages</button>
                                </div>
                                
                                <div class="search-form-container" id="form-container">
                                    <!-- Form dynamically injected by JS -->
                                </div>
                            </div>
                        </section>

                        <section class="results-section" id="results-section" style="display: none;">
                            <div class="results-header">
                                <h2 id="results-title">Available Options</h2>
                                <div class="filters">
                                    <select id="sort-select">
                                        <option value="">Sort By</option>
                                        <option value="price_asc">Price: Low to High</option>
                                        <option value="price_desc">Price: High to Low</option>
                                    </select>
                                </div>
                            </div>
                            <div class="loader" id="loader" style="display:none;"><div class="spinner"></div></div>
                            <div class="results-grid" id="results-grid">
                                <!-- Results will be injected here via JS -->
                            </div>
                        </section>
                    </main>

                    <!-- Checkout View (Hidden initially) -->
                    <main id="checkout-view" style="display:none;">
                        <section class="checkout-section">
                            <div class="glass-card checkout-container">
                                <h2><i class="fa-solid fa-credit-card"></i> Complete Your Booking</h2>
                                <div id="booking-summary" class="booking-summary"></div>
                                <form id="payment-form" class="payment-form">
                                    <div class="input-group">
                                        <label>Cardholder Name</label>
                                        <input type="text" required placeholder="John Doe">
                                    </div>
                                    <div class="input-group">
                                        <label>Card Number</label>
                                        <input type="text" required placeholder="XXXX XXXX XXXX XXXX">
                                    </div>
                                    <div class="row">
                                        <div class="input-group">
                                            <label>Expiry</label>
                                            <input type="text" required placeholder="MM/YY">
                                        </div>
                                        <div class="input-group">
                                            <label>CVV</label>
                                            <input type="password" required placeholder="***">
                                        </div>
                                    </div>
                                    <button type="submit" class="btn btn-primary btn-block">Pay Securely</button>
                                    <button type="button" class="btn btn-outline btn-block mt-2" onclick="goBackToSearch()">Cancel</button>
                                </form>
                            </div>
                        </section>
                    </main>

                    <!-- Success View -->
                    <main id="success-view" style="display:none;">
                        <section class="success-section">
                            <div class="glass-card success-container text-center">
                                <div class="success-icon"><i class="fa-solid fa-circle-check"></i></div>
                                <h2>Booking Confirmed!</h2>
                                <p>Your booking ID is <strong id="booking-id-display"></strong>.</p>
                                <p>We have sent the e-tickets to your email address.</p>
                                <button class="btn btn-primary mt-4" onclick="goBackToSearch()">Book Another</button>
                            </div>
                        </section>
                    </main>

                    <!-- Login Modal -->
                    <div id="login-modal" class="modal">
                        <div class="modal-content glass-card">
                            <span class="close" onclick="closeModal('login')">&times;</span>
                            <h2>Login</h2>
                            <div class="input-group">
                                <label>Email</label>
                                <input type="email" placeholder="Email">
                            </div>
                            <div class="input-group">
                                <label>Password</label>
                                <input type="password" placeholder="Password">
                            </div>
                            <button class="btn btn-primary btn-block" onclick="closeModal('login')">Login</button>
                        </div>
                    </div>

                    <footer>
                        <p>&copy; 2026 WanderLust Travel Platform. All Rights Reserved.</p>
                    </footer>

                    <script src="app.js"></script>
                </body>
                </html>
              mode: '000644'
              owner: 'ec2-user'
              group: 'ec2-user'
            /home/ec2-user/app/frontend/style.css:
              content: |
                :root {
                    --primary-color: #ff5722;
                    --primary-hover: #e64a19;
                    --bg-color: #f0f2f5;
                    --text-color: #333;
                    --glass-bg: rgba(255, 255, 255, 0.85);
                    --glass-border: rgba(255, 255, 255, 0.3);
                    --glass-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
                }

                * { margin: 0; padding: 0; box-sizing: border-box; }

                body {
                    font-family: 'Outfit', sans-serif;
                    background: linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%);
                    color: var(--text-color);
                    min-height: 100vh;
                    display: flex;
                    flex-direction: column;
                }

                .navbar {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    padding: 1.5rem 5%;
                    background: var(--glass-bg);
                    backdrop-filter: blur(10px);
                    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
                    position: sticky;
                    top: 0;
                    z-index: 1000;
                }

                .logo { font-size: 1.8rem; font-weight: 800; color: var(--primary-color); }

                .nav-links { display: flex; list-style: none; gap: 2rem; }
                .nav-links a { 
                    text-decoration: none; color: #555; font-weight: 600; 
                    padding-bottom: 0.3rem; transition: 0.3s;
                }
                .nav-links a:hover, .nav-links a.active {
                    color: var(--primary-color);
                    border-bottom: 2px solid var(--primary-color);
                }

                .btn {
                    padding: 0.6rem 1.5rem; border: none; border-radius: 8px;
                    font-weight: 600; cursor: pointer; transition: 0.3s;
                    font-family: 'Outfit', sans-serif;
                }
                .btn-primary { background: var(--primary-color); color: #fff; }
                .btn-primary:hover { background: var(--primary-hover); transform: translateY(-2px); box-shadow: 0 4px 15px rgba(255,87,34,0.3); }
                .btn-outline { background: transparent; border: 2px solid var(--primary-color); color: var(--primary-color); }
                .btn-outline:hover { background: var(--primary-color); color: #fff; }
                .btn-block { width: 100%; padding: 1rem; font-size: 1.1rem; }
                .mt-2 { margin-top: 1rem; }
                .mt-4 { margin-top: 2rem; }

                .hero {
                    text-align: center; padding: 4rem 2rem 2rem;
                    color: #111;
                }
                .hero h1 { font-size: 3.5rem; font-weight: 800; margin-bottom: 1rem; }
                .hero p { font-size: 1.2rem; opacity: 0.8; }

                .search-section { padding: 0 5%; margin-top: -1rem; margin-bottom: 3rem; }
                
                .glass-card {
                    background: var(--glass-bg);
                    backdrop-filter: blur(15px);
                    border: 1px solid var(--glass-border);
                    border-radius: 20px;
                    box-shadow: var(--glass-shadow);
                    padding: 2rem;
                }

                .search-container { max-width: 1000px; margin: 0 auto; }
                .search-tabs { display: flex; gap: 1rem; margin-bottom: 2rem; border-bottom: 1px solid #ddd; padding-bottom: 1rem; overflow-x: auto;}
                .tab-btn {
                    background: none; border: none; font-size: 1.1rem; font-weight: 600;
                    color: #666; cursor: pointer; padding: 0.5rem 1rem; transition: 0.3s;
                    border-radius: 8px;
                }
                .tab-btn:hover { background: #f0f0f0; }
                .tab-btn.active { background: var(--primary-color); color: #fff; }

                .search-form { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.5rem; align-items: end; }
                .input-group { display: flex; flex-direction: column; text-align: left;}
                .row { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;}
                .input-group label { font-size: 0.9rem; font-weight: 600; color: #555; margin-bottom: 0.5rem; }
                .input-group input, .input-group select {
                    padding: 0.8rem 1rem; border: 1px solid #ccc; border-radius: 8px;
                    font-size: 1rem; font-family: 'Outfit', sans-serif; transition: 0.3s;
                }
                .input-group input:focus { border-color: var(--primary-color); outline: none; box-shadow: 0 0 0 3px rgba(255,87,34,0.1); }
                .btn-search { padding: 0.9rem; font-size: 1.1rem; }

                .results-section { padding: 2rem 5%; max-width: 1200px; margin: 0 auto; flex: 1; width: 100%;}
                .results-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem; }
                .filters select { padding: 0.5rem; border-radius: 8px; border: 1px solid #ccc; font-family: 'Outfit'; }
                
                .results-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; }
                
                .result-card {
                    background: #fff; border-radius: 15px; padding: 1.5rem;
                    box-shadow: 0 10px 20px rgba(0,0,0,0.05); transition: 0.3s;
                    display: flex; flex-direction: column; gap: 1rem;
                    border-top: 4px solid var(--primary-color);
                }
                .result-card:hover { transform: translateY(-5px); box-shadow: 0 15px 30px rgba(0,0,0,0.1); }
                .card-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #eee; padding-bottom: 0.5rem;}
                .card-header h3 { font-size: 1.2rem; color: #222; }
                .price { font-size: 1.5rem; font-weight: 800; color: var(--primary-color); }
                .card-body p { margin-bottom: 0.5rem; font-size: 0.95rem; color: #555; display: flex; justify-content: space-between;}
                .card-body p strong { color: #222; }

                /* Loader */
                .loader { display: flex; justify-content: center; padding: 3rem; }
                .spinner { width: 40px; height: 40px; border: 4px solid rgba(255,87,34,0.2); border-left-color: var(--primary-color); border-radius: 50%; animation: spin 1s linear infinite; }
                @keyframes spin { 0% {transform: rotate(0deg);} 100% {transform: rotate(360deg);} }

                /* Checkout */
                .checkout-section, .success-section { padding: 4rem 5%; display: flex; justify-content: center; flex: 1;}
                .checkout-container, .success-container { max-width: 500px; width: 100%; }
                .checkout-container h2 { margin-bottom: 1.5rem; text-align: center; }
                .booking-summary { background: #f9f9f9; padding: 1rem; border-radius: 8px; margin-bottom: 2rem; border-left: 4px solid var(--primary-color); }
                .booking-summary p { margin-bottom: 0.5rem; font-size: 1rem;}

                /* Success */
                .success-icon { font-size: 5rem; color: #4CAF50; margin-bottom: 1rem; }
                .text-center { text-align: center; }

                /* Modal */
                .modal { display: none; position: fixed; z-index: 2000; left: 0; top: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.5); backdrop-filter: blur(5px); justify-content: center; align-items: center; }
                .modal-content { max-width: 400px; width: 90%; position: relative; display: flex; flex-direction: column; gap: 1rem;}
                .close { position: absolute; right: 1.5rem; top: 1rem; font-size: 1.5rem; cursor: pointer; color: #555;}

                footer { text-align: center; padding: 2rem; background: #222; color: #aaa; margin-top: auto; }
              mode: '000644'
              owner: 'ec2-user'
              group: 'ec2-user'
            /home/ec2-user/app/frontend/app.js:
              content: |
                let currentServiceType = 'flights';
                let currentBookingData = null;

                const formTemplates = {
                    flights: `
                        <div class="search-form">
                            <div class="input-group">
                                <label><i class="fa-solid fa-plane-departure"></i> From</label>
                                <select id="flight-origin" required>
                                    <option value="">Select City</option>
                                    <option value="DEL">Delhi (DEL)</option>
                                    <option value="BOM">Mumbai (BOM)</option>
                                    <option value="BLR">Bangalore (BLR)</option>
                                    <option value="GOI">Goa (GOI)</option>
                                    <option value="HYD">Hyderabad (HYD)</option>
                                </select>
                            </div>
                            <div class="input-group">
                                <label><i class="fa-solid fa-plane-arrival"></i> To</label>
                                <select id="flight-dest" required>
                                    <option value="">Select City</option>
                                    <option value="BOM">Mumbai (BOM)</option>
                                    <option value="DEL">Delhi (DEL)</option>
                                    <option value="BLR">Bangalore (BLR)</option>
                                    <option value="GOI">Goa (GOI)</option>
                                    <option value="HYD">Hyderabad (HYD)</option>
                                </select>
                            </div>
                            <div class="input-group">
                                <label><i class="fa-regular fa-calendar"></i> Date</label>
                                <input type="date" required id="flight-date">
                            </div>
                            <button type="button" class="btn btn-primary btn-search" onclick="searchData('flights')"><i class="fa-solid fa-magnifying-glass"></i> Search</button>
                        </div>
                    `,
                    hotels: `
                        <div class="search-form" style="grid-template-columns: 2fr 1fr 1fr auto;">
                            <div class="input-group">
                                <label><i class="fa-solid fa-location-dot"></i> City/Location</label>
                                <select id="hotel-loc" required>
                                    <option value="">Select City</option>
                                    <option value="Delhi">Delhi</option>
                                    <option value="Mumbai">Mumbai</option>
                                    <option value="Goa">Goa</option>
                                    <option value="Bangalore">Bangalore</option>
                                </select>
                            </div>
                            <div class="input-group">
                                <label>Check-In</label>
                                <input type="date" required id="hotel-in">
                            </div>
                            <div class="input-group">
                                <label>Check-Out</label>
                                <input type="date" required id="hotel-out">
                            </div>
                            <button type="button" class="btn btn-primary btn-search" onclick="searchData('hotels')"><i class="fa-solid fa-magnifying-glass"></i> Search</button>
                        </div>
                    `,
                    cabs: `
                        <div class="search-form">
                            <div class="input-group">
                                <label>Pickup Location</label>
                                <input type="text" placeholder="Enter Pickup" required>
                            </div>
                            <div class="input-group">
                                <label>Drop Location</label>
                                <input type="text" placeholder="Enter Drop" required>
                            </div>
                            <button type="button" class="btn btn-primary btn-search" onclick="searchData('cabs')">Search Cabs</button>
                        </div>
                    `,
                    packages: `
                        <div class="search-form">
                            <div class="input-group">
                                <label>Destination</label>
                                <select id="pkg-dest" required>
                                    <option value="">Any</option>
                                    <option value="Goa">Goa</option>
                                    <option value="Manali">Manali</option>
                                    <option value="Kerala">Kerala</option>
                                    <option value="Maldives">Maldives</option>
                                </select>
                            </div>
                            <button type="button" class="btn btn-primary btn-search" onclick="searchData('packages')">Explore Packages</button>
                        </div>
                    `
                };

                document.addEventListener('DOMContentLoaded', () => {
                    const formContainer = document.getElementById('form-container');
                    formContainer.innerHTML = formTemplates['flights'];

                    // Tab Switching
                    document.querySelectorAll('.tab-btn').forEach(btn => {
                        btn.addEventListener('click', (e) => {
                            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
                            e.target.classList.add('active');
                            currentServiceType = e.target.getAttribute('data-target');
                            formContainer.innerHTML = formTemplates[currentServiceType];
                            document.getElementById('results-section').style.display = 'none';
                        });
                    });
                    
                    document.getElementById('sort-select').addEventListener('change', () => {
                        searchData(currentServiceType);
                    });
                });

                function searchData(type) {
                    const grid = document.getElementById('results-grid');
                    const resultsSec = document.getElementById('results-section');
                    const loader = document.getElementById('loader');
                    
                    resultsSec.style.display = 'block';
                    grid.innerHTML = '';
                    loader.style.display = 'flex';
                    
                    let url = '/api/' + type + '?';
                    let sort = document.getElementById('sort-select').value;
                    if (sort) url += '&sort=' + sort;
                    
                    if (type === 'flights') {
                        let orig = document.getElementById('flight-origin').value;
                        let dest = document.getElementById('flight-dest').value;
                        if(orig) url += '&origin=' + orig;
                        if(dest) url += '&destination=' + dest;
                    } else if (type === 'hotels') {
                        let loc = document.getElementById('hotel-loc').value;
                        if(loc) url += '&location=' + loc;
                    }

                    fetch(url)
                        .then(res => res.json())
                        .then(data => {
                            loader.style.display = 'none';
                            if (data.error) {
                                grid.innerHTML = \`<p style="color:red;">Error: \${data.error}</p>\`;
                                return;
                            }
                            if (data.length === 0) {
                                grid.innerHTML = '<p>No results found for your search criteria.</p>';
                                return;
                            }
                            renderResults(type, data);
                        })
                        .catch(err => {
                            loader.style.display = 'none';
                            grid.innerHTML = '<p style="color:red;">Failed to fetch data from API.</p>';
                        });
                }

                function renderResults(type, data) {
                    const grid = document.getElementById('results-grid');
                    let html = '';
                    
                    data.forEach(item => {
                        if (type === 'flights') {
                            html += \`
                            <div class="result-card">
                                <div class="card-header">
                                    <h3><i class="fa-solid fa-plane"></i> \${item.airline}</h3>
                                    <span class="price">₹\${item.price}</span>
                                </div>
                                <div class="card-body">
                                    <p><span>\${item.origin} <i class="fa-solid fa-arrow-right"></i> \${item.destination}</span></p>
                                    <p><span>Duration:</span> <strong>\${item.duration}</strong></p>
                                    <p><span>Class:</span> <strong>\${item.class_type}</strong></p>
                                    <button class="btn btn-primary btn-block mt-2" onclick="initiateBooking('\${type}', \${item.id}, \${item.price}, '\${item.airline} Flight from \${item.origin} to \${item.destination}')">Book Now</button>
                                </div>
                            </div>\`;
                        } else if (type === 'hotels') {
                            html += \`
                            <div class="result-card">
                                <div class="card-header">
                                    <h3><i class="fa-solid fa-hotel"></i> \${item.name}</h3>
                                    <span class="price">₹\${item.price_per_night}<span style="font-size:0.8rem;color:#777;">/night</span></span>
                                </div>
                                <div class="card-body">
                                    <p><span>Location:</span> <strong>\${item.location}</strong></p>
                                    <p><span>Rating:</span> <strong>\${item.rating} <i class="fa-solid fa-star" style="color:#FFC107;"></i></strong></p>
                                    <p><span>Amenities:</span> <strong style="font-size:0.8rem;">\${item.amenities}</strong></p>
                                    <button class="btn btn-primary btn-block mt-2" onclick="initiateBooking('\${type}', \${item.id}, \${item.price_per_night}, '\${item.name} in \${item.location}')">Book Room</button>
                                </div>
                            </div>\`;
                        } else if (type === 'cabs') {
                            html += \`
                            <div class="result-card">
                                <div class="card-header">
                                    <h3><i class="fa-solid fa-taxi"></i> \${item.type}</h3>
                                    <span class="price">₹\${item.price_per_km}<span style="font-size:0.8rem;color:#777;">/km</span></span>
                                </div>
                                <div class="card-body">
                                    <p><span>Driver:</span> <strong>\${item.driver_name}</strong></p>
                                    <button class="btn btn-primary btn-block mt-2" onclick="initiateBooking('\${type}', \${item.id}, \${item.price_per_km}, '\${item.type} Cab')">Book Cab</button>
                                </div>
                            </div>\`;
                        } else if (type === 'packages') {
                            html += \`
                            <div class="result-card">
                                <div class="card-header">
                                    <h3><i class="fa-solid fa-map-location-dot"></i> \${item.destination}</h3>
                                    <span class="price">₹\${item.price}</span>
                                </div>
                                <div class="card-body">
                                    <p><span>Duration:</span> <strong>\${item.days} Days</strong></p>
                                    <p><span>Includes:</span> <strong style="font-size:0.8rem;">\${item.includes}</strong></p>
                                    <button class="btn btn-primary btn-block mt-2" onclick="initiateBooking('\${type}', \${item.id}, \${item.price}, '\${item.days} Days Package to \${item.destination}')">Book Package</button>
                                </div>
                            </div>\`;
                        }
                    });
                    
                    grid.innerHTML = html;
                }

                function initiateBooking(type, id, price, desc) {
                    currentBookingData = {
                        service_type: type,
                        service_id: id,
                        total_price: price
                    };
                    
                    document.getElementById('main-view').style.display = 'none';
                    document.getElementById('checkout-view').style.display = 'flex';
                    
                    document.getElementById('booking-summary').innerHTML = \`
                        <p><strong>Service:</strong> \${desc}</p>
                        <p><strong>Total Amount to Pay:</strong> <span class="price" style="font-size:1.2rem;">₹\${price}</span></p>
                    \`;
                }
                
                function goBackToSearch() {
                    document.getElementById('checkout-view').style.display = 'none';
                    document.getElementById('success-view').style.display = 'none';
                    document.getElementById('main-view').style.display = 'block';
                }

                document.getElementById('payment-form').addEventListener('submit', (e) => {
                    e.preventDefault();
                    const btn = e.target.querySelector('button[type="submit"]');
                    btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Processing...';
                    btn.disabled = true;
                    
                    fetch('/api/book', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(currentBookingData)
                    })
                    .then(res => res.json())
                    .then(data => {
                        btn.innerHTML = 'Pay Securely';
                        btn.disabled = false;
                        if(data.status === 'success') {
                            document.getElementById('checkout-view').style.display = 'none';
                            document.getElementById('success-view').style.display = 'flex';
                            document.getElementById('booking-id-display').innerText = 'WL' + data.booking_id.toString().padStart(6, '0');
                        } else {
                            alert('Booking failed: ' + data.error);
                        }
                    })
                    .catch(err => {
                        btn.innerHTML = 'Pay Securely';
                        btn.disabled = false;
                        alert('Payment processing failed.');
                    });
                });

                function showModal(id) { document.getElementById(id+'-modal').style.display = 'flex'; }
                function closeModal(id) { document.getElementById(id+'-modal').style.display = 'none'; }
              mode: '000644'
              owner: 'ec2-user'
              group: 'ec2-user'
            /etc/nginx/conf.d/travel.conf:
              content: |
                server {
                    listen 80;
                    server_name _;
                    
                    root /home/ec2-user/app/frontend;
                    index index.html;
                    
                    location / {
                        try_files $uri $uri/ /index.html;
                    }
                    
                    location /health {
                        proxy_pass http://127.0.0.1:5000;
                        proxy_set_header Host $host;
                    }
                    
                    location /api/ {
                        proxy_pass http://127.0.0.1:5000;
                        proxy_set_header Host $host;
                        proxy_set_header X-Real-IP $remote_addr;
                    }
                }
              mode: '000644'
              owner: 'root'
              group: 'root'
"""

new_commands_content = """          commands:
            01_install_deps:
              command: "pip3 install -r /home/ec2-user/app/backend/requirements.txt"
            02_run_seed:
              command: "python3 /home/ec2-user/app/backend/seed.py"
"""

lines = lines[:start_idx] + [new_files_content, new_commands_content] + lines[end_idx+3:]

with open('travel_booking_platform.yaml', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Injected successfully!")
