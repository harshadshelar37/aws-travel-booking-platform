import boto3

ssm = boto3.client('ssm', region_name='eu-west-3')
ssm.send_command(
    InstanceIds=['i-06f837271e996ee8f'],
    DocumentName='AWS-RunShellScript',
    Parameters={
        'commands': [
            'sed -i "s|proxy_pass http://127.0.0.1:5000/;|proxy_pass http://127.0.0.1:5000;|" /etc/nginx/conf.d/travel.conf',
            'systemctl reload nginx'
        ]
    }
)
print("Command sent!")
