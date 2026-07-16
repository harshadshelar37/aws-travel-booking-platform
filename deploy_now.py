import boto3, time

ssm = boto3.client('ssm', region_name='eu-west-3')
res = ssm.send_command(
    InstanceIds=['i-075c1bba4a4ca7f9c'],
    DocumentName='AWS-RunShellScript',
    Parameters={'commands': [
        'cfn-init -v --stack travel-booking-prod --resource AppLaunchTemplate --region eu-west-3 && systemctl daemon-reload && systemctl restart travel-backend && systemctl restart nginx && echo DEPLOYED_OK'
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
        if out['StandardErrorContent']:
            print('STDERR:', out['StandardErrorContent'][:300].encode('ascii','ignore').decode('ascii'))
        break
    print(f'  attempt {i+1}: still running...')
