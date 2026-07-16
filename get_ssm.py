import boto3
import sys
import time

command_id = sys.argv[1]
instance_id = sys.argv[2]

ssm = boto3.client('ssm', region_name='eu-west-3')

while True:
    response = ssm.get_command_invocation(
        CommandId=command_id,
        InstanceId=instance_id
    )
    status = response['Status']
    if status in ['Pending', 'InProgress']:
        time.sleep(2)
    else:
        out = response.get('StandardOutputContent', '')
        err = response.get('StandardErrorContent', '')
        with open('ssm_output.txt', 'w', encoding='utf-8') as f:
            f.write("--- STDOUT ---\n")
            f.write(out)
            f.write("\n--- STDERR ---\n")
            f.write(err)
        break
