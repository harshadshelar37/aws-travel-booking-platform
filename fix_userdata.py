import yaml

with open('travel_booking_platform.yaml', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Add travel-backend.service to files
files_idx = -1
for i, line in enumerate(lines):
    if line.strip() == "files:" and "setup:" in "".join(lines[i-5:i]):
        files_idx = i
        break

if files_idx != -1:
    service_content = """            /etc/systemd/system/travel-backend.service:
              content: |
                [Unit]
                Description=Gunicorn instance to serve travel backend
                After=network.target

                [Service]
                User=ec2-user
                Group=ec2-user
                WorkingDirectory=/home/ec2-user/app/backend
                Environment="PATH=/usr/local/bin:/usr/bin"
                EnvironmentFile=/home/ec2-user/app/backend/.env
                ExecStart=/usr/local/bin/gunicorn --workers 3 --bind 127.0.0.1:5000 app:app

                [Install]
                WantedBy=multi-user.target
              mode: '000644'
              owner: 'root'
              group: 'root'
"""
    lines.insert(files_idx + 1, service_content)

# Fix UserData
start_idx = -1
end_idx = -1
for i, line in enumerate(lines):
    if line.strip() == "UserData:":
        start_idx = i
    if start_idx != -1 and line.strip() == "AppTargetGroup:":
        end_idx = i
        break

if start_idx != -1 and end_idx != -1:
    new_userdata = """        UserData:
          Fn::Base64: !Sub |
            #!/bin/bash
            yum update -y
            yum install -y nginx python3 python3-pip mariadb105
            
            cat << 'EOT' > /home/ec2-user/app/backend/.env
            DB_HOST=${RDSInstance.Endpoint.Address}
            DB_USER=${DBUsername}
            DB_PASS=${DBPassword}
            DB_NAME=travel_db
            EOT
            
            /opt/aws/bin/cfn-init -v --stack ${AWS::StackName} --resource AppLaunchTemplate --region ${AWS::Region} --configsets default
            
            chown -R ec2-user:ec2-user /home/ec2-user/app
            chmod 755 /home/ec2-user
            chmod -R 755 /home/ec2-user/app
            
            systemctl enable travel-backend
            systemctl restart travel-backend
            systemctl enable nginx
            systemctl restart nginx
  """
    lines = lines[:start_idx] + [new_userdata] + lines[end_idx:]

with open('travel_booking_platform.yaml', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Fixed UserData and Service!")
