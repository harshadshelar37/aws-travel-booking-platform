import boto3, time

ssm = boto3.client('ssm', region_name='eu-west-3')

cmd = """cd /home/ec2-user/app/backend && python3 -c "
import os, mysql.connector, random
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASS = os.getenv('DB_PASS', '')
conn = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, database='travel_db')
cursor = conn.cursor()

# Delete existing flights (which use airport codes)
cursor.execute('DELETE FROM flights')

print('Seeding flights with city names...')
airlines = ['IndiGo', 'Air India', 'Vistara', 'SpiceJet', 'Akasa Air']
cities = ['Delhi', 'Mumbai', 'Bangalore', 'Hyderabad', 'Chennai', 'Kolkata', 'Pune', 'Goa']

for _ in range(500):
    origin = random.choice(cities)
    dest = random.choice([c for c in cities if c != origin])
    departure = datetime.now() + timedelta(days=random.randint(1, 30), hours=random.randint(1, 23))
    arrival = departure + timedelta(hours=random.randint(1, 4), minutes=random.randint(0, 59))
    duration = str((arrival - departure).seconds // 3600) + 'h ' + str(((arrival - departure).seconds // 60) % 60) + 'm'
    price = round(random.uniform(2500, 15000), 2)
    airline = random.choice(airlines)
    cursor.execute(
        'INSERT INTO flights (airline, origin, destination, departure_time, arrival_time, price, duration) VALUES (%s, %s, %s, %s, %s, %s, %s)',
        (airline, origin, dest, departure, arrival, price, duration)
    )

conn.commit()
cursor.execute('SELECT COUNT(*) FROM flights')
print('Total flights:', cursor.fetchone()[0])
cursor.close()
conn.close()
" 2>&1"""

res = ssm.send_command(
    InstanceIds=['i-075c1bba4a4ca7f9c'],
    DocumentName='AWS-RunShellScript',
    Parameters={'commands': [cmd]}
)
cid = res['Command']['CommandId']

for i in range(15):
    time.sleep(5)
    out = ssm.get_command_invocation(CommandId=cid, InstanceId='i-075c1bba4a4ca7f9c')
    if out['Status'] in ['Success', 'Failed', 'TimedOut']:
        print('Status:', out['Status'])
        print(out['StandardOutputContent'].encode('ascii','ignore').decode('ascii'))
        if out['StandardErrorContent']:
            print('STDERR:', out['StandardErrorContent'][:300].encode('ascii','ignore').decode('ascii'))
        break
