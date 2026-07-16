import boto3, time

ssm = boto3.client('ssm', region_name='eu-west-3')

# Add more buses with popular city pairs to ensure searches return results
cmd = """cd /home/ec2-user/app/backend && python3 -c "
import os, mysql.connector, random
from dotenv import load_dotenv
load_dotenv()
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASS = os.getenv('DB_PASS', '')
conn = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, database='travel_db')
cursor = conn.cursor()

# Delete existing buses and re-seed with proper city name casing
cursor.execute('DELETE FROM buses')

operators = ['VRL Travels', 'SRS Travels', 'Orange Travels', 'Neeta Travels', 'Kallada Travels', 'APSRTC', 'MSRTC']
bus_types = ['Volvo AC Semi-Sleeper', 'Scania AC Multi-Axle', 'Non-AC Sleeper', 'AC Sleeper', 'Volvo AC Seater']
# Use same city names as search input
cities = ['Delhi', 'Mumbai', 'Bangalore', 'Hyderabad', 'Chennai', 'Kolkata', 'Pune', 'Goa', 'Manali', 'Jaipur', 'Ahmedabad', 'Kochi', 'Surat', 'Vadodara']
pickup_opts = ['Main Bus Terminal', 'City Center Stop', 'Highway Junction', 'Railway Station', 'Airport Road']
drop_opts = ['Central Bus Stand', 'City Stop', 'Highway Point', 'Main Station', 'Market Square']

for _ in range(300):
    origin = random.choice(cities)
    dest = random.choice([c for c in cities if c != origin])
    op = random.choice(operators)
    btype = random.choice(bus_types)
    price = round(random.uniform(500, 3000), 2)
    dur = str(random.randint(5, 18)) + 'h ' + str(random.randint(0, 59)) + 'm'
    pickup = random.choice(pickup_opts)
    drop = random.choice(drop_opts)
    cursor.execute(
        'INSERT INTO buses (operator_name, bus_type, origin, destination, pickup_point, drop_point, duration, price) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',
        (op, btype, origin, dest, pickup, drop, dur, price)
    )
conn.commit()

cursor.execute('SELECT COUNT(*) FROM buses')
print('Total buses:', cursor.fetchone()[0])
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

for i in range(15):
    time.sleep(5)
    out = ssm.get_command_invocation(CommandId=cid, InstanceId='i-075c1bba4a4ca7f9c')
    if out['Status'] in ['Success', 'Failed', 'TimedOut']:
        print('Status:', out['Status'])
        print(out['StandardOutputContent'].encode('ascii','ignore').decode('ascii'))
        break
    print('  attempt', i+1, '- still running...')
