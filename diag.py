import boto3, time

ssm = boto3.client('ssm', region_name='eu-west-3')

# Check live app.js and look for JS errors
res = ssm.send_command(
    InstanceIds=['i-075c1bba4a4ca7f9c'],
    DocumentName='AWS-RunShellScript',
    Parameters={'commands': [
        # Check if app.js is there and check for syntax issues
        'python3 -c "import py_compile, sys; py_compile.compile(\'x\', doraise=True)" 2>&1 || true;'
        'node --check /home/ec2-user/app/frontend/app.js 2>&1 && echo "JS_OK" || echo "JS_ERROR";'
        'head -5 /home/ec2-user/app/frontend/app.js;'
        'grep -c "rupee\\|\\\\u20b9\\|₹" /home/ec2-user/app/frontend/app.js || true;'
        'curl -s "http://127.0.0.1:5000/api/flights" | python3 -c "import json,sys; d=json.load(sys.stdin); print(len(d), \'flights, first:\', d[0].get(\'airline\') if d else \'NONE\')" 2>&1'
    ]}
)
cid = res['Command']['CommandId']
print('CMD:', cid)
time.sleep(8)
out = ssm.get_command_invocation(CommandId=cid, InstanceId='i-075c1bba4a4ca7f9c')
print('Status:', out['Status'])
print(out['StandardOutputContent'].encode('ascii','ignore').decode('ascii'))
print('ERR:', out['StandardErrorContent'][:500].encode('ascii','ignore').decode('ascii'))
