import os
from flask import Flask, jsonify, request, send_from_directory
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash

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

# ----- AUTHENTICATION ROUTES -----

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    
    if not name or not email or not password:
        return jsonify({"error": "Missing fields"}), 400
        
    conn = get_db_connection()
    if not conn: return jsonify({"error": "Database connection failed"}), 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            return jsonify({"error": "Email already registered"}), 409
            
        hashed_pw = generate_password_hash(password)
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            (name, email, hashed_pw)
        )
        conn.commit()
        user_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return jsonify({"status": "success", "id": user_id, "name": name, "email": email})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    conn = get_db_connection()
    if not conn: return jsonify({"error": "Database connection failed"}), 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            return jsonify({"status": "success", "id": user['id'], "name": user['name'], "email": user['email']})
        else:
            return jsonify({"error": "Invalid email or password"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ----- SUGGESTIONS ROUTE -----

@app.route('/api/locations', methods=['GET'])
def get_locations():
    conn = get_db_connection()
    if not conn: return jsonify({"error": "Database connection failed"}), 500
    
    try:
        cursor = conn.cursor()
        locations = set()
        
        try:
            cursor.execute("SELECT DISTINCT origin FROM flights")
            for row in cursor.fetchall(): locations.add(row[0])
        except: pass
            
        try:
            cursor.execute("SELECT DISTINCT destination FROM flights")
            for row in cursor.fetchall(): locations.add(row[0])
        except: pass
            
        try:
            cursor.execute("SELECT DISTINCT location FROM hotels")
            for row in cursor.fetchall(): locations.add(row[0])
        except: pass
            
        try:
            cursor.execute("SELECT DISTINCT origin FROM buses")
            for row in cursor.fetchall(): locations.add(row[0])
        except: pass

        try:
            cursor.execute("SELECT DISTINCT destination FROM buses")
            for row in cursor.fetchall(): locations.add(row[0])
        except: pass
            
        cursor.close()
        conn.close()
        
        extra_cities = {
            "Delhi", "Mumbai", "Bangalore", "Hyderabad", "Chennai", "Kolkata", 
            "Pune", "Ahmedabad", "Jaipur", "Surat", "Lucknow", "Kanpur", "Nagpur",
            "Indore", "Thane", "Bhopal", "Visakhapatnam", "Patna", "Vadodara",
            "Ghaziabad", "Ludhiana", "Agra", "Nashik", "Faridabad", "Meerut",
            "Rajkot", "Varanasi", "Srinagar", "Aurangabad", "Amritsar", "Navi Mumbai",
            "Ranchi", "Howrah", "Coimbatore", "Gwalior", "Vijayawada", "Jodhpur",
            "Madurai", "Raipur", "Kota", "Guwahati", "Chandigarh", "Mysore",
            "Tiruchirappalli", "Bareilly", "Gurgaon", "Noida", "Kochi", "Dehradun",
            "Jammu", "Mangalore", "Udaipur", "Goa",
            "New York", "London", "Paris", "Tokyo", "Dubai", "Singapore", "Sydney"
        }
        locations.update(extra_cities)
        
        return jsonify({"locations": sorted(list(locations))})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ----- DATA ROUTES -----

@app.route('/api/flights', methods=['GET'])
def get_flights():
    conn = get_db_connection()
    if not conn: return jsonify({"error": "Database connection failed"}), 500
    
    origin = request.args.get('origin', '')
    destination = request.args.get('destination', '')
    sort = request.args.get('sort', '')
    
    airport_map = {
        "DELHI": "DEL", "MUMBAI": "BOM", "BANGALORE": "BLR",
        "GOA": "GOI", "PUNE": "PNQ", "HYDERABAD": "HYD",
        "CHENNAI": "MAA", "KOLKATA": "CCU", "KOCHI": "COK",
        "AHMEDABAD": "AMD", "JAIPUR": "JAI", "LUCKNOW": "LKO"
    }

    query = "SELECT * FROM flights WHERE 1=1"
    params = []
    if origin:
        origin_code = airport_map.get(origin.upper(), origin.upper())
        query += " AND (origin = %s OR origin LIKE %s)"
        params.extend([origin_code, f"%{origin}%"])
    if destination:
        dest_code = airport_map.get(destination.upper(), destination.upper())
        query += " AND (destination = %s OR destination LIKE %s)"
        params.extend([dest_code, f"%{destination}%"])
        
    if sort == "price_asc":
        query += " ORDER BY price ASC"
    elif sort == "price_desc":
        query += " ORDER BY price DESC"
    else:
        query += " ORDER BY departure_time ASC"
    
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
        query += " AND location LIKE %s"
        params.append(f"%{location}%")
        
    if sort == "price_asc":
        query += " ORDER BY price_per_night ASC"
    elif sort == "price_desc":
        query += " ORDER BY price_per_night DESC"
    else:
        query += " ORDER BY rating DESC"
    
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
    destination = request.args.get('destination', '')
    query = "SELECT * FROM packages WHERE 1=1"
    params = []
    if destination:
        query += " AND destination LIKE %s"
        params.append(f"%{destination}%")
    query += " LIMIT 20"
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(rows)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
@app.route('/api/buses', methods=['GET'])
def get_buses():
    conn = get_db_connection()
    if not conn: return jsonify({"error": "Database connection failed"}), 500
    
    origin = request.args.get('origin', '')
    destination = request.args.get('destination', '')
    
    query = "SELECT * FROM buses WHERE 1=1"
    params = []
    if origin:
        query += " AND origin LIKE %s"
        params.append(f"%{origin}%")
    if destination:
        query += " AND destination LIKE %s"
        params.append(f"%{destination}%")
        
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
        
@app.route('/api/book', methods=['POST'])
def book_service():
    data = request.json
    conn = get_db_connection()
    if not conn: return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor()
        user_id = data.get('user_id')
        service_type = data['service_type'].capitalize() # Flight, Hotel, etc.
        # Handle plural to singular mapping
        if service_type == 'Flights': service_type = 'Flight'
        elif service_type == 'Hotels': service_type = 'Hotel'
        elif service_type == 'Cabs': service_type = 'Cab'
        elif service_type == 'Packages': service_type = 'Package'
        
        cursor.execute(
            "INSERT INTO bookings (user_id, booking_type, reference_id, status, payment_status) VALUES (%s, %s, %s, 'Confirmed', 'Paid')",
            (user_id, service_type, data['service_id'])
        )
        conn.commit()
        booking_id = cursor.lastrowid
        
        # Insert payment record
        cursor.execute(
            "INSERT INTO payments (booking_id, amount, payment_mode, status) VALUES (%s, %s, 'Credit Card', 'Success')",
            (booking_id, data['total_price'])
        )
        conn.commit()
        
        cursor.close()
        conn.close()
        return jsonify({"success": True, "booking_id": booking_id, "message": "Booking Confirmed!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/admin/stats', methods=['GET'])
def get_admin_stats():
    conn = get_db_connection()
    if not conn: return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor(dictionary=True)
        
        # Get total users
        cursor.execute("SELECT COUNT(*) as total_users FROM users")
        total_users = cursor.fetchone()['total_users']
        
        # Get total bookings
        cursor.execute("SELECT COUNT(*) as total_bookings FROM bookings")
        total_bookings = cursor.fetchone()['total_bookings']
        
        # Get total revenue
        cursor.execute("SELECT SUM(amount) as total_revenue FROM payments WHERE status = 'Success'")
        rev_row = cursor.fetchone()
        total_revenue = float(rev_row['total_revenue']) if rev_row['total_revenue'] else 0.0
        
        # Get recent bookings
        query = '''
            SELECT b.booking_id, u.name as user_name, b.booking_type, b.booking_date, p.amount 
            FROM bookings b 
            JOIN users u ON b.user_id = u.user_id 
            LEFT JOIN payments p ON b.booking_id = p.booking_id
            ORDER BY b.booking_date DESC 
            LIMIT 5
        '''
        cursor.execute(query)
        recent_bookings = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            "total_users": total_users,
            "total_bookings": total_bookings,
            "total_revenue": total_revenue,
            "recent_bookings": recent_bookings
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
