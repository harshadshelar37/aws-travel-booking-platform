import boto3
import time

ssm = boto3.client('ssm', region_name='eu-west-3')
cmd = '''
python3 -c "
with open('/usr/share/nginx/html/app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if 'card-price' in line or 'price-highlight' in line or '?' in line:
        if '?' in line and ' ? ' in line: continue
        if '?' in line and ' ?' in line: continue
        if '/api/' in line: continue
        print(f'{i+1}: {line.strip()}')
"
'''
res = ssm.send_command(
    InstanceIds=['i-075c1bba4a4ca7f9c'],
    DocumentName='AWS-RunShellScript',
    Parameters={'commands': [cmd]}
)
cid = res['Command']['CommandId']
for _ in range(15):
    time.sleep(2)
    out = ssm.get_command_invocation(CommandId=cid, InstanceId='i-075c1bba4a4ca7f9c')
    if out['Status'] in ['Success', 'Failed']:
        print(out['StandardOutputContent'])
        break
