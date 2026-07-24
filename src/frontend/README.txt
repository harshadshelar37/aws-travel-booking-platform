===========================================================================
FRONTEND - HTML, CSS, JAVASCRIPT
===========================================================================

WHAT THIS FOLDER IS FOR:
This folder contains the client-side code for the Travel Booking Platform.
- index.html: The main structural layout of the web page.
- style.css: The CSS stylesheets (glassmorphism, animations, layouts).
- app.js: The logic that powers the UI tabs, fetches location data, and calculates mock prices.

HOW TO DEPLOY MANUALLY FROM SCRATCH:
1. Open your terminal or command prompt.
2. Connect to your EC2 instance using SSH:
   ssh -i your-key.pem ec2-user@<YOUR-EC2-PUBLIC-IP>
3. Create the app directory if it doesn't exist:
   mkdir -p /home/ec2-user/app/frontend
4. Open a new terminal on your local machine and use SCP to securely copy these 3 files to your EC2 instance:
   scp -i your-key.pem index.html style.css app.js ec2-user@<YOUR-EC2-PUBLIC-IP>:/home/ec2-user/app/frontend/
5. If NGINX is configured correctly (see src/nginx/README.txt), the website will instantly update to reflect your newly copied files.
6. Clear your browser cache (Ctrl + F5) to see the changes live!
