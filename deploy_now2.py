import boto3, time

ssm = boto3.client('ssm', region_name='eu-west-3')

res = ssm.send_command(
    InstanceIds=['i-075c1bba4a4ca7f9c'],
    DocumentName='AWS-RunShellScript',
    Parameters={'commands': [
        'cd /home/ec2-user/app && python3 build_yaml.py',
        'cfn-init -v --stack travel-booking-prod --resource AppLaunchTemplate --region eu-west-3 && systemctl restart nginx'
    ]}
)
cid = res['Command']['CommandId']
print('CMD:', cid)

for i in range(15):
    time.sleep(5)
    out = ssm.get_command_invocation(CommandId=cid, InstanceId='i-075c1bba4a4ca7f9c')
    if out['Status'] in ['Success', 'Failed', 'TimedOut']:
        print('Status:', out['Status'])
        print(out['StandardOutputContent'].encode('ascii','ignore').decode('ascii')[-800:])
        break
