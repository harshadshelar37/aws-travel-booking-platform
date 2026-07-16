import boto3, time
ssm = boto3.client('ssm', region_name='eu-west-3')
res = ssm.send_command(
    InstanceIds=['i-075c1bba4a4ca7f9c'],
    DocumentName='AWS-RunShellScript',
    Parameters={'commands': [
        'cd /home/ec2-user/app/backend && source .env 2>/dev/null; export DB_HOST= DB_USER= DB_PASS= && python3 seed.py 2>&1 && echo SEED_DONE'
    ]}
)
cid = res['Command']['CommandId']
print('CMD:', cid)
time.sleep(40)
out = ssm.get_command_invocation(CommandId=cid, InstanceId='i-075c1bba4a4ca7f9c')
print('Status:', out['Status'])
print(out['StandardOutputContent'].encode('ascii','ignore').decode('ascii'))
print('ERR:', out['StandardErrorContent'][:500].encode('ascii','ignore').decode('ascii'))
