import boto3
import base64
import time

ssm = boto3.client('ssm', region_name='eu-west-3')
instance_id = 'i-075c1bba4a4ca7f9c'

def run_cmd(cmd):
    ssm.send_command(InstanceIds=[instance_id], DocumentName='AWS-RunShellScript', Parameters={'commands': [cmd]})
    time.sleep(1)

def push_file(local_path, remote_path):
    print(f'Pushing {local_path}...')
    with open(local_path, 'rb') as f:
        data = f.read()
    b64 = base64.b64encode(data).decode('utf-8')
    chunk_size = 30000
    
    run_cmd(f'rm -f {remote_path}.b64')
    
    for i in range(0, len(b64), chunk_size):
        chunk = b64[i:i+chunk_size]
        run_cmd(f'echo {chunk} | tr -d "\\n" >> {remote_path}.b64')
        print(f'  chunk {i}')
        time.sleep(1)
        
    run_cmd(f'base64 -d {remote_path}.b64 > {remote_path} && chown ec2-user:ec2-user {remote_path} && rm {remote_path}.b64')
    print(f'Finished {local_path}')

push_file('src/frontend/app.js', '/home/ec2-user/app/frontend/app.js')
push_file('src/frontend/index.html', '/home/ec2-user/app/frontend/index.html')
push_file('src/frontend/style.css', '/home/ec2-user/app/frontend/style.css')
run_cmd('systemctl restart nginx')
print('Deployed successfully via SSM chunking!')
