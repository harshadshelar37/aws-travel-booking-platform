===========================================================================
BACKEND - FLASK API & PYTHON SCRIPTING
===========================================================================

WHAT THIS FOLDER IS FOR:
This folder contains the Python Flask application that acts as the bridge between your Frontend UI and your RDS Database.
- app.py: The main Flask server containing the endpoints (e.g., /api/search).
- requirements.txt: The list of Python libraries needed to run the app (Flask, boto3, mysql-connector-python).

HOW TO DEPLOY MANUALLY FROM SCRATCH:
1. SSH into your EC2 instance.
2. Ensure Python 3 and pip are installed:
   sudo yum install python3 python3-pip -y
3. Create the backend directory:
   mkdir -p /home/ec2-user/app/backend
4. Use SCP to copy 'app.py' and 'requirements.txt' to this directory.
5. Navigate to the folder on your EC2 instance:
   cd /home/ec2-user/app/backend
6. Install the dependencies:
   pip3 install -r requirements.txt
7. Create a '.env' file in this folder to hold your database secrets:
   nano .env
   (Add your DB_HOST, DB_USER, DB_PASSWORD, DB_NAME here).
8. Run the Flask app for testing:
   python3 app.py
9. Your backend is now running on port 5000! (Note: In production, we use Systemd + Gunicorn to run this automatically. See src/systemd/README.txt).
