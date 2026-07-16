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

    # Seed Buses
    cursor.execute("SELECT COUNT(*) FROM travel_db.buses")
    if cursor.fetchone()[0] == 0:
        print("Seeding buses...")
        operators = ["VRL Travels", "SRS Travels", "Orange Travels", "Neeta Travels", "Kallada"]
        bus_types = ["Volvo AC Semi-Sleeper", "Scania AC Multi-Axle", "Non-AC Sleeper", "AC Sleeper"]
        cities = ["Delhi", "Mumbai", "Bangalore", "Hyderabad", "Chennai", "Kolkata", "Pune", "Goa", "Manali", "Jaipur"]
        for _ in range(150):
            origin = random.choice(cities)
            dest = random.choice([c for c in cities if c != origin])
            operator = random.choice(operators)
            btype = random.choice(bus_types)
            price = round(random.uniform(500, 3000), 2)
            duration = f"{random.randint(5, 18)}h {random.randint(0, 59)}m"
            pickup = f"{random.choice(['Main', 'City Center', 'Highway', 'Terminal', 'Station'])} Point"
            drop = f"{random.choice(['Main', 'City Center', 'Highway', 'Terminal', 'Station'])} Point"
            cursor.execute(
                "INSERT INTO travel_db.buses (operator_name, bus_type, origin, destination, pickup_point, drop_point, duration, price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (operator, btype, origin, dest, pickup, drop, duration, price)
            )

    conn.commit()
    cursor.close()
    conn.close()
    print("Seeding completed successfully!")
except Exception as e:
    print(f"Database error: {e}")
