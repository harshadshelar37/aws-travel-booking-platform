===========================================================================
SCRIPTS - DEPLOYMENT & AUTOMATION
===========================================================================

WHAT THIS FOLDER IS FOR:
This folder contains Python scripts written to make your life easier when deploying changes. Instead of manually using SCP (Secure Copy) to push every single HTML or Python file to your EC2 instance over and over, these scripts automate it.

- fast_deploy.py: Uses AWS Systems Manager (SSM) to bypass SSH entirely. It takes your local frontend files, breaks them into small Base64 chunks, and pushes them directly into your EC2 instance in seconds.
- build_yaml.py: A script that takes your source code and injects it directly into the CloudFormation YAML template (using AWS cfn-init). This is useful if you want to deploy a brand new environment from scratch without doing any manual SCP transfers.
- seed_remote.py: A script to remotely execute SQL commands on the database by tunneling through SSM.

HOW TO USE:
1. Ensure you have your AWS credentials configured locally (aws configure).
2. Ensure you have the 'boto3' Python library installed (pip install boto3).
3. If you make a change to 'src/frontend/style.css', simply open your terminal and run:
   python scripts/fast_deploy.py
   (Note: you may need to update the instance ID inside the script if your EC2 instance changes).
4. The script will automatically push the changes and restart NGINX for you.
