import urllib.request, json

base = 'http://prod-alb-600778398.eu-west-3.elb.amazonaws.com'
tests = [
    '/api/flights',
    '/api/flights?origin=DEL&destination=BOM',
    '/api/hotels',
    '/api/hotels?location=Mumbai',
    '/api/buses',
    '/api/buses?origin=Delhi&destination=Mumbai',
    '/api/cabs',
    '/api/packages',
    '/api/locations',
]
for path in tests:
    try:
        res = urllib.request.urlopen(base + path, timeout=6)
        data = json.loads(res.read().decode())
        if isinstance(data, list):
            print('OK  ' + path + ': ' + str(len(data)) + ' results')
        elif isinstance(data, dict) and 'locations' in data:
            print('OK  ' + path + ': ' + str(len(data['locations'])) + ' locations')
        else:
            print('OK  ' + path + ': ' + str(data)[:80])
    except Exception as e:
        print('ERR ' + path + ': ' + str(e))
