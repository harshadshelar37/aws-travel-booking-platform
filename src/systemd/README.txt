===========================================================================
SYSTEMD & GUNICORN - PRODUCTION BACKEND RUNNER
===========================================================================

WHAT THIS FOLDER IS FOR:
If you just run 'python3 app.py', the server will stop working the moment you close your SSH terminal. To fix this, we use Gunicorn (a production Python server) and Systemd (Linux's background service manager). Systemd ensures your backend runs in the background 24/7 and automatically restarts if it crashes.

HOW TO DEPLOY MANUALLY FROM SCRATCH:
1. SSH into your EC2 instance.
2. Install Gunicorn:
   pip3 install gunicorn
3. Create a Systemd service file:
   sudo nano /etc/systemd/system/travel_backend.service
4. Paste the following configuration into the file:

[Unit]
Description=Gunicorn instance to serve travel backend
After=network.target

[Service]
User=ec2-user
Group=ec2-user
WorkingDirectory=/home/ec2-user/app/backend
ExecStart=/usr/local/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target

5. Reload Systemd so it sees your new file:
   sudo systemctl daemon-reload
6. Start the service:
   sudo systemctl start travel_backend
7. Enable it to start automatically when the server reboots:
   sudo systemctl enable travel_backend
8. Check its status if something goes wrong:
   sudo systemctl status travel_backend
