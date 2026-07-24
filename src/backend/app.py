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
            "Delhi", "Mumbai", "Bangalore", "Hyderabad", "Chennai", "Kolkata", "Pune", "Ahmedabad", "Jaipur", "Surat",
            "Lucknow", "Kanpur", "Nagpur", "Indore", "Thane", "Bhopal", "Visakhapatnam", "Patna", "Vadodara", "Ghaziabad",
            "Ludhiana", "Agra", "Nashik", "Faridabad", "Meerut", "Rajkot", "Varanasi", "Srinagar", "Aurangabad", "Amritsar",
            "Navi Mumbai", "Ranchi", "Howrah", "Coimbatore", "Gwalior", "Vijayawada", "Jodhpur", "Madurai", "Raipur", "Kota",
            "Guwahati", "Chandigarh", "Mysore", "Tiruchirappalli", "Bareilly", "Gurgaon", "Noida", "Kochi", "Dehradun", "Jammu",
            "Mangalore", "Udaipur", "Goa", "Aligarh", "Jalandhar", "Bhubaneswar", "Salem", "Mira-Bhayandar", "Warangal", "Guntur",
            "Bhiwandi", "Saharanpur", "Gorakhpur", "Bikaner", "Amravati", "Noida", "Jamshedpur", "Bhilai", "Cuttack", "Firozabad",
            "Kochi", "Nellore", "Bhavnagar", "Dehradun", "Durgapur", "Asansol", "Rourkela", "Nanded", "Kolhapur", "Ajmer",
            "Akola", "Gulbarga", "Jamnagar", "Ujjain", "Loni", "Siliguri", "Jhansi", "Ulhasnagar", "Jammu", "Sangli-Miraj & Kupwad",
            "Mangalore", "Erode", "Belgaum", "Ambattur", "Tirunelveli", "Malegaon", "Gaya", "Jalgaon", "Udaipur", "Maheshtala",
            "Davanagere", "Kozhikode", "Kurnool", "Rajpur Sonarpur", "Rajahmundry", "Bokaro", "South Dumdum", "Bellary", "Patiala",
            "Gopalpur", "Agartala", "Bhagalpur", "Muzaffarnagar", "Bhatpara", "Panihati", "Latur", "Dhule", "Tirupati", "Rohtak",
            "Korba", "Bhilwara", "Berhampur", "Muzaffarpur", "Ahmednagar", "Mathura", "Kollam", "Avadi", "Kadapa", "Kamarhati",
            "Sambalpur", "Bilaspur", "Shahjahanpur", "Satara", "Bijapur", "Rampur", "Shivamogga", "Chandrapur", "Junagadh",
            "Thrissur", "Alwar", "Bardhaman", "Kulti", "Kakinada", "Nizamabad", "Parbhani", "Tumkur", "Khammam", "Ozhukarai",
            "Bihar Sharif", "Panipat", "Darbhanga", "Bally", "Aizawl", "Dewas", "Ichalkaranji", "Karnal", "Bathinda", "Jalna",
            "Eluru", "Kirari Suleman Nagar", "Barasat", "Purnia", "Satna", "Mau", "Sonipat", "Farrukhabad", "Sagar", "Rourkela",
            "Durg", "Imphal", "Ratlam", "Hapur", "Arrah", "Karimnagar", "Anantapur", "Etawah", "Ambernath", "North Dumdum",
            "Bharatpur", "Begusarai", "New Delhi", "Gandhidham", "Baranagar", "Tiruvottiyur", "Pondicherry", "Sikar", "Thoothukudi",
            "Rewa", "Mirzapur", "Raichur", "Pali", "Ramagundam", "Haridwar", "Vijayanagaram", "Katihar", "Nagercoil", "Sri Ganganagar",
            "Karawal Nagar", "Mango", "Thanjavur", "Bulandshahr", "Uluberia", "Murwara", "Rajpur Sonarpur", "Sambhal", "Singrauli",
            "Nadiad", "Secunderabad", "Naihati", "Yamunanagar", "Bidhannagar", "Pallavaram", "Bidar", "Munger", "Panchkula", "Burhanpur",
            "Raurkela Industrial Township", "Kharagpur", "Dindigul", "Gandhinagar", "Hospet", "Nangloi Jat", "English Bazar", "Ongole",
            "Deoghar", "Chapra", "Haldia", "Khandwa", "Nandyal", "Chittoor", "Orai", "Bhimavaram", "Anand", "Raebareli", "Bhiwani",
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
            "INSERT INTO bookings (user_id, service_type, service_id, total_price, status) VALUES (%s, %s, %s, %s, 'Confirmed')",
            (user_id, service_type, data['service_id'], data['total_price'])
        )
        conn.commit()
        booking_id = cursor.lastrowid
        
        cursor.close()
        conn.close()
        return jsonify({"success": True, "booking_id": booking_id, "message": "Booking Confirmed!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/user/bookings/<int:user_id>', methods=['GET'])
def get_user_bookings(user_id):
    conn = get_db_connection()
    if not conn: return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT b.*, 
                   f.airline, f.origin as flight_origin, f.destination as flight_dest,
                   h.name as hotel_name, h.location as hotel_loc,
                   c.type as cab_type, c.driver_name,
                   bus.operator_name, bus.origin as bus_origin, bus.destination as bus_dest,
                   p.destination as package_dest, p.days as package_days
            FROM bookings b
            LEFT JOIN flights f ON b.service_type IN ('Flight', 'Flights') AND b.service_id = f.id
            LEFT JOIN hotels h ON b.service_type IN ('Hotel', 'Hotels') AND b.service_id = h.id
            LEFT JOIN cabs c ON b.service_type IN ('Cab', 'Cabs') AND b.service_id = c.id
            LEFT JOIN buses bus ON b.service_type IN ('Bus', 'Buses') AND b.service_id = bus.id
            LEFT JOIN packages p ON b.service_type IN ('Package', 'Packages') AND b.service_id = p.id
            WHERE b.user_id = %s
            ORDER BY b.booking_date DESC
        ''', (user_id,))
        bookings = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(bookings)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/admin/users', methods=['GET'])
def get_admin_users():
    conn = get_db_connection()
    if not conn: return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name, email, DATE_FORMAT(created_at, '%Y-%m-%d %H:%i') as joined FROM users ORDER BY created_at DESC")
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(users)
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
        cursor.execute("SELECT SUM(total_price) as total_revenue FROM bookings WHERE status = 'Confirmed'")
        rev_row = cursor.fetchone()
        total_revenue = float(rev_row['total_revenue']) if rev_row['total_revenue'] else 0.0
        
        # Get recent bookings
        query = '''
            SELECT b.id as booking_id, u.name as user_name, b.service_type as booking_type, b.booking_date, b.total_price as amount 
            FROM bookings b 
            JOIN users u ON b.user_id = u.id 
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

import re
import requests
import random
import urllib.parse

def get_weather(city):
    try:
        geo_url = f"https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(city)}&format=json&limit=1"
        geo_res = requests.get(geo_url, headers={'User-Agent': 'TravelEaseChatbot/1.0'}, timeout=3).json()
        if not geo_res: return f"I couldn't find the location '{city}' to check the weather."
        
        lat = geo_res[0]['lat']
        lon = geo_res[0]['lon']
        
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        weather_res = requests.get(weather_url, timeout=3).json()
        temp = weather_res['current_weather']['temperature']
        return f"The current temperature in {city.title()} is {temp}°C."
    except Exception as e:
        return f"I'm having trouble fetching the weather for {city} right now."

def get_wikipedia(query):
    try:
        formatted_query = query.title().replace(' ', '_')
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(formatted_query)}"
        res = requests.get(url, headers={'User-Agent': 'TravelEaseChatbot/1.0'}, timeout=3).json()
        if 'extract' in res:
            return res['extract']
        return f"I couldn't find detailed info about '{query}'."
    except Exception as e:
        return f"I'm having trouble looking up '{query}' right now."

def get_booking_tracking(booking_id):
    conn = get_db_connection()
    if not conn: return "I'm sorry, our tracking database is currently down. Please try again later."
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM bookings WHERE id = %s", (booking_id,))
        booking = cursor.fetchone()
        
        if not booking:
            return f"I couldn't find a booking with the ID #TB-{str(booking_id).zfill(6)}. Please check your booking ID and try again."
            
        service_type = booking['service_type']
        service_id = booking['service_id']
        status = booking['status']
        date = booking['booking_date'].strftime('%b %d, %Y %I:%M %p') if booking['booking_date'] else 'Unknown'
        
        reply = f"Here is the tracking info for your booking <b>#TB-{str(booking_id).zfill(6)}</b>:<br><br>"
        reply += f"Status: <b>{status}</b><br>"
        reply += f"Booked on: {date}<br><br>"
        
        if service_type == 'Flight':
            cursor.execute("SELECT * FROM flights WHERE id = %s", (service_id,))
            flight = cursor.fetchone()
            if flight:
                reply += f"✈️ <b>Flight Details:</b><br>"
                reply += f"Airline: {flight.get('airline', 'Unknown')}<br>"
                reply += f"From: {flight.get('origin', 'Unknown')} at {flight.get('departure_time', 'Unknown')}<br>"
                reply += f"To: {flight.get('destination', 'Unknown')} at {flight.get('arrival_time', 'Unknown')}<br>"
        elif service_type == 'Hotel':
            cursor.execute("SELECT * FROM hotels WHERE id = %s", (service_id,))
            hotel = cursor.fetchone()
            if hotel:
                reply += f"🏨 <b>Hotel Details:</b><br>"
                reply += f"Name: {hotel.get('name', 'Unknown')}<br>"
                reply += f"Location: {hotel.get('location', 'Unknown')}<br>"
                reply += f"Rating: {hotel.get('rating', 'Unknown')}⭐<br>"
        elif service_type == 'Cab':
            cursor.execute("SELECT * FROM cabs WHERE id = %s", (service_id,))
            cab = cursor.fetchone()
            if cab:
                reply += f"🚕 <b>Cab Details:</b><br>"
                reply += f"Type: {cab.get('type', 'Unknown')} ({cab.get('model', 'Unknown')})<br>"
                reply += f"Driver: {cab.get('driver_name', 'Assigned soon')} (Rating: {cab.get('rating', 'N/A')})<br>"
                reply += f"ETA: Usually arrives within 10-15 mins of pickup time.<br>"
        elif service_type == 'Package':
            cursor.execute("SELECT * FROM packages WHERE id = %s", (service_id,))
            pkg = cursor.fetchone()
            if pkg:
                reply += f"🏝️ <b>Package Details:</b><br>"
                reply += f"Name: {pkg.get('name', 'Unknown')}<br>"
                reply += f"Destination: {pkg.get('destination', 'Unknown')}<br>"
                reply += f"Duration: {pkg.get('duration', 'Unknown')} Days<br>"
                
        reply += "<br>Is there anything else you need help with regarding your journey?"
        
        cursor.close()
        conn.close()
        return reply
    except Exception as e:
        print(f"Error tracking booking: {e}")
        return "I'm sorry, I encountered an error while retrieving your tracking details."

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    msg = data.get('message', '').lower()
    msg_clean = re.sub(r'[^\w\s]', '', msg).strip()
    
    # 0. Conversational Continuations
    if msg_clean in ['yes', 'yeah', 'sure', 'ok', 'okay', 'yep', 'please', 'y']:
        return jsonify({"reply": "Great! Please tell me exactly what you need help with (e.g., 'track #TB-000001', 'I need a flight', or 'tell me about Goa')."})
    if msg_clean in ['no', 'nope', 'nah', 'nothing', 'no thanks', 'n']:
        return jsonify({"reply": "Alright, thank you for contacting TravelEase support. Have a wonderful day!"})
    if msg_clean in ['help', 'more help', 'support', 'can you help me', 'i need help']:
        return jsonify({"reply": "I'm here to help! I can assist you with tracking bookings, finding flights, hotels, or cabs, and answering basic questions. What can I do for you?"})
        
    
    # 0. Booking ID Tracking Intent
    booking_match = re.search(r'(?:#?tb-|#?TB-)(\d+)', msg, re.IGNORECASE)
    if not booking_match:
        generic_match = re.search(r'(?:track|booking|trip).*?\b(\d{1,6})\b', msg, re.IGNORECASE)
        if generic_match:
            booking_match = generic_match

    if booking_match:
        booking_id = int(booking_match.group(1))
        return jsonify({"reply": get_booking_tracking(booking_id)})
    
    # 1. Weather Intent
    weather_match = re.search(r'weather\s+(?:in|for|at|of)\s+([a-z\s]+)', msg)
    if weather_match:
        city = weather_match.group(1).strip().split('?')[0]
        return jsonify({"reply": get_weather(city)})
        
    # 2. Wikipedia Intent
    info_match = re.search(r'(?:tell me about|what is|who is|info on)\s+([a-z\s]+)', msg)
    if info_match:
        query = info_match.group(1).strip().replace('the ', '').split('?')[0]
        return jsonify({"reply": get_wikipedia(query)})
        
    # 3. Math Intent
    math_match = re.search(r'(?:what is|calculate)\s*(\d+)\s*([\+\-\*\/])\s*(\d+)', msg)
    if math_match:
        num1 = int(math_match.group(1))
        op = math_match.group(2)
        num2 = int(math_match.group(3))
        res = 0
        if op == '+': res = num1 + num2
        elif op == '-': res = num1 - num2
        elif op == '*': res = num1 * num2
        elif op == '/': res = num1 / num2 if num2 != 0 else 'infinity'
        return jsonify({"reply": f"The answer is {res}."})
        
    # 4. Joke Intent
    if re.search(r'\b(joke|funny|laugh)\b', msg):
        jokes = [
            "Why do airplanes get so much rest? Because they are always in the clouds! ✈️",
            "What do you call a travel agent who can't book a flight? Grounded! 😂",
            "Why did the librarian get kicked off the plane? Because it was overbooked! 📚"
        ]
        return jsonify({"reply": random.choice(jokes)})

    # 5. Core NLP Rules
    response = ""
    
    if re.search(r'\b(hi|hello|hey|greetings|howdy)\b', msg):
        response += "Hello! 👋 I'm your TravelEase assistant. "
    
    if re.search(r'\b(flight|flights|fly|ticket|airline|aeroplane)\b', msg):
        response += "I see you're asking about flights! We offer great deals. You can search for flights using the 'Flights' tab. "
        
    elif re.search(r'\b(hotel|hotels|room|stay|resort)\b', msg):
        response += "Need a place to stay? You can explore our top-rated hotels in the 'Hotels' tab. "
        
    elif re.search(r'\b(cab|cabs|taxi|car|pickup)\b', msg):
        response += "We offer reliable cab services! You can even use the 'Live Location' feature on the Cabs tab to easily set your pickup point. "
        
    elif re.search(r'\b(cancel|cancellation|refund|money back)\b', msg):
        response += "For cancellations, you can cancel up to 24 hours before your trip. Refunds are processed to your original payment method within 5-7 business days. "
        
    elif re.search(r'\b(track|status|my booking|my trip|where is)\b', msg):
        response += "To check your booking status, please visit the 'My Trips' section at the top of the page. "
        
    elif re.search(r'\b(payment|pay|card|upi|fail|failed|money)\b', msg):
        response += "We accept Credit/Debit Cards, UPI, and Net Banking securely. If your payment failed, please ensure your card details (like the 16-digit number and expiry) are correct. "
        
    elif re.search(r'\b(thank|thanks|thx)\b', msg):
        return jsonify({"reply": "You're very welcome! Let me know if you need anything else. 😊"})
        
    if not response:
        # Fallback to Wikipedia if they just typed a term like "taj mahal"
        if len(msg_clean) > 2 and msg_clean not in ['yes', 'no', 'ok', 'okay', 'sure', 'help', 'yeah', 'yep', 'nope']:
            wiki_res = get_wikipedia(msg.strip('?').strip())
            if "I couldn't find detailed info" not in wiki_res and "I'm having trouble looking up" not in wiki_res:
                return jsonify({"reply": wiki_res})
                
        response = "I can fetch live weather, lookup information, calculate math, tell jokes, and help with your bookings! Try asking 'What is the weather in Mumbai?' or 'Tell me about Goa'."
    else:
        response += "Is there anything else I can help you with today?"
        
    return jsonify({"reply": response.strip()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
