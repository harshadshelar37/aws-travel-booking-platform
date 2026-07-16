import boto3, time

ssm = boto3.client('ssm', region_name='eu-west-3')

cmd = """cd /home/ec2-user/app/frontend && node -c app.js 2>&1"""

res = ssm.send_command(
    InstanceIds=['i-075c1bba4a4ca7f9c'],
    DocumentName='AWS-RunShellScript',
    Parameters={'commands': [cmd]}
)
cid = res['Command']['CommandId']

for i in range(15):
    time.sleep(2)
    out = ssm.get_command_invocation(CommandId=cid, InstanceId='i-075c1bba4a4ca7f9c')
    if out['Status'] in ['Success', 'Failed', 'TimedOut']:
        print('Status:', out['Status'])
        print(out['StandardOutputContent'])
        break
