===========================================================================
NGINX - WEB SERVER & REVERSE PROXY
===========================================================================

WHAT THIS FOLDER IS FOR:
NGINX acts as the front door to your EC2 instance. It serves your static HTML/JS files directly to users, and 'reverse proxies' (forwards) any API requests to your Python backend running on port 5000.

HOW TO DEPLOY MANUALLY FROM SCRATCH:
1. SSH into your EC2 instance.
2. Install NGINX:
   sudo yum install nginx -y
3. Open the main NGINX configuration file:
   sudo nano /etc/nginx/nginx.conf
4. Edit the 'server' block to include these two crucial sections:
   
   location / {
       root /home/ec2-user/app/frontend;
       index index.html;
   }

   location /api/ {
       proxy_pass http://127.0.0.1:5000/;
       proxy_set_header Host $host;
       proxy_set_header X-Real-IP $remote_addr;
   }

5. Save the file and restart NGINX to apply the changes:
   sudo systemctl restart nginx
6. Make sure NGINX starts automatically when the server reboots:
   sudo systemctl enable nginx
