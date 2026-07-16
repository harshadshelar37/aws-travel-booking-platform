import boto3
import time

ssm = boto3.client('ssm', region_name='eu-west-3')

cmd = 'mysql -u root -e "USE travel_db; SHOW TABLES;"'

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
