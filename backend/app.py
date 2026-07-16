import os
import pymysql
from flask import Flask, jsonify, request, send_from_directory
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='../frontend', static_url_path='/')

# Database connection details
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "")
DB_NAME = os.getenv("DB_NAME", "traveldb")

def get_db_connection():
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME,
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except Exception as e:
        print(f"Error connecting to DB: {e}")
        return None

# Serve Frontend
@app.route('/')
def index():
    return app.send_static_file('index.html')

# Health Check
@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

# ================== FLIGHTS API ==================
@app.route('/api/flights', methods=['GET'])
def get_flights():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Flights")
            flights = cursor.fetchall()
        return jsonify(flights), 200
    finally:
        conn.close()

# ================== HOTELS API ==================
@app.route('/api/hotels', methods=['GET'])
def get_hotels():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Hotels")
            hotels = cursor.fetchall()
        return jsonify(hotels), 200
    finally:
        conn.close()

# ================== CABS API ==================
@app.route('/api/cabs', methods=['GET'])
def get_cabs():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Cab_Services")
            cabs = cursor.fetchall()
        return jsonify(cabs), 200
    finally:
        conn.close()

# ================== PACKAGES API ==================
@app.route('/api/packages', methods=['GET'])
def get_packages():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Holiday_Packages")
            packages = cursor.fetchall()
        return jsonify(packages), 200
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
