import boto3, time
ssm = boto3.client('ssm', region_name='eu-west-3')
res = ssm.send_command(
    InstanceIds=['i-075c1bba4a4ca7f9c'],
    DocumentName='AWS-RunShellScript',
    Parameters={'commands': ['mysql -u admin -p12345678 -h prod-mysql-db.crqqqs4mutlt.eu-west-3.rds.amazonaws.com travel_db -e "SELECT COUNT(*) as buses_count FROM buses; SELECT COUNT(*) as packages_count FROM packages;" 2>&1']}
)
cid = res['Command']['CommandId']
time.sleep(8)
out = ssm.get_command_invocation(CommandId=cid, InstanceId='i-075c1bba4a4ca7f9c')
print(out['StandardOutputContent'].encode('ascii','ignore').decode('ascii'))
print(out['StandardErrorContent'].encode('ascii','ignore').decode('ascii'))
