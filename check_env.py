import boto3, time
ssm = boto3.client('ssm', region_name='eu-west-3')
res = ssm.send_command(
    InstanceIds=['i-075c1bba4a4ca7f9c'],
    DocumentName='AWS-RunShellScript',
    Parameters={'commands': [
        'cd /home/ec2-user/app/backend && python3 -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv(\"DB_HOST\"))"'
    ]}
)
cid = res['Command']['CommandId']
time.sleep(5)
out = ssm.get_command_invocation(CommandId=cid, InstanceId='i-075c1bba4a4ca7f9c')
print(out['StandardOutputContent'].encode('ascii','ignore').decode('ascii'))
print(out['StandardErrorContent'].encode('ascii','ignore').decode('ascii'))
