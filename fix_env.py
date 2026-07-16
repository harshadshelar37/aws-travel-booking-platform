import boto3
ssm = boto3.client('ssm', region_name='eu-west-3')
ssm.send_command(
    InstanceIds=['i-01133d4e9c6fa91b7'],
    DocumentName='AWS-RunShellScript',
    Parameters={
        'commands': [
            'mkdir -p /home/ec2-user/app/backend',
            'cat << "EOF" > /home/ec2-user/app/backend/.env\nDB_HOST=prod-mysql-db.crqqqs4mutlt.eu-west-3.rds.amazonaws.com\nDB_USER=admin\nDB_PASS=12345678\nDB_NAME=travel_db\nEOF',
            'chown ec2-user:ec2-user /home/ec2-user/app/backend/.env',
            '/opt/aws/bin/cfn-init -v --stack travel-booking-prod --resource AppLaunchTemplate --region eu-west-3 --configsets default',
            'systemctl enable travel-backend',
            'systemctl restart travel-backend'
        ]
    }
)
print("Fix sent!")
