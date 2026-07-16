import boto3, time

ssm = boto3.client('ssm', region_name='eu-west-3')

# Run seed using python to load .env inline — no bash tricks needed
cmd = """cd /home/ec2-user/app/backend && python3 -c "
import os, mysql.connector, random
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASS = os.getenv('DB_PASS', '')
print('Connecting to:', DB_HOST)
conn = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASS)
cursor = conn.cursor()

# Run schema to create missing tables
with open('/home/ec2-user/app/backend/schema.sql') as f:
    for stmt in f.read().split(';'):
        if stmt.strip():
            try: cursor.execute(stmt)
            except: pass

# Seed buses if empty
cursor.execute('SELECT COUNT(*) FROM travel_db.buses')
if cursor.fetchone()[0] == 0:
    print('Seeding buses...')
    operators = ['VRL Travels', 'SRS Travels', 'Orange Travels', 'Neeta Travels', 'Kallada Travels']
    bus_types = ['Volvo AC Semi-Sleeper', 'Scania AC Multi-Axle', 'Non-AC Sleeper', 'AC Sleeper']
    cities = ['Delhi', 'Mumbai', 'Bangalore', 'Hyderabad', 'Chennai', 'Kolkata', 'Pune', 'Goa', 'Manali', 'Jaipur', 'Ahmedabad']
    for _ in range(150):
        origin = random.choice(cities)
        dest = random.choice([c for c in cities if c != origin])
        op = random.choice(operators)
        btype = random.choice(bus_types)
        price = round(random.uniform(500, 3000), 2)
        dur = str(random.randint(5,18)) + 'h ' + str(random.randint(0,59)) + 'm'
        pickup = random.choice(['Main', 'City Center', 'Terminal', 'Station']) + ' Point'
        drop = random.choice(['Main', 'City Center', 'Terminal', 'Station']) + ' Point'
        cursor.execute('INSERT INTO travel_db.buses (operator_name, bus_type, origin, destination, pickup_point, drop_point, duration, price) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)', (op,btype,origin,dest,pickup,drop,dur,price))
    conn.commit()
    print('Buses seeded!')

# Seed packages if empty
cursor.execute('SELECT COUNT(*) FROM travel_db.packages')
if cursor.fetchone()[0] == 0:
    print('Seeding packages...')
    dests = ['Goa', 'Manali', 'Kerala', 'Andaman', 'Kashmir', 'Dubai', 'Maldives', 'Singapore', 'Bangkok']
    for _ in range(50):
        dest = random.choice(dests)
        days = random.randint(3, 10)
        price = round(random.uniform(15000, 150000), 2)
        cursor.execute('INSERT INTO travel_db.packages (destination, days, price, includes) VALUES (%s,%s,%s,%s)', (dest, days, price, 'Flights, Hotel, Transfers, Meals'))
    conn.commit()
    print('Packages seeded!')

cursor.close()
conn.close()
print('Done!')
" 2>&1"""

res = ssm.send_command(
    InstanceIds=['i-075c1bba4a4ca7f9c'],
    DocumentName='AWS-RunShellScript',
    Parameters={'commands': [cmd]}
)
cid = res['Command']['CommandId']
print('CMD:', cid)

# Poll until done
for i in range(20):
    time.sleep(5)
    out = ssm.get_command_invocation(CommandId=cid, InstanceId='i-075c1bba4a4ca7f9c')
    if out['Status'] in ['Success', 'Failed', 'TimedOut']:
        print('Status:', out['Status'])
        print(out['StandardOutputContent'].encode('ascii','ignore').decode('ascii'))
        if out['StandardErrorContent']:
            print('STDERR:', out['StandardErrorContent'][:300].encode('ascii','ignore').decode('ascii'))
        break
    print(f'  Attempt {i+1}: still running...')
