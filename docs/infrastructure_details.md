Infrastructure Architecture & File Organization
This document explains the infrastructure of the Travel Booking Platform in simple terms. It describes
where different files are stored, why they are created, and their purpose. This is useful for explaining
the architecture to an interviewer.
1. Infrastructure as Code (CloudFormation)
File: cloudformation/travel_booking_platform.yaml
What it is: A blueprint of our entire AWS infrastructure written in YAML code.
Why we created it: Instead of manually clicking through the AWS console to create networks (VPC),
servers (EC2), and databases (RDS), we wrote this file. AWS reads this file and automatically builds
everything for us.
Where it is stored: Locally on the developer's computer. During deployment, it is uploaded to the
AWS CloudFormation service, which provisions the resources.
What is the use: It ensures our infrastructure is reproducible, version-controlled, and can be deployed
or destroyed with a single command.
2. Application Code (Frontend & Backend)
Files: src/frontend/ (index.html, style.css, app.js) and src/backend/ (app.py)
What they are:
 Frontend: The visual website interface users interact with.
 Backend: The Python Flask API that processes user requests, handles bookings, and talks to the
database.
Why we created them: To build the actual logic and user interface of the Travel Booking Platform.
Where they are stored: They live in the local project repository and are copied into the AWS EC2
instances (servers) at the path: /home/ec2-user/app/
Why store them there: EC2 instances act as our web servers. They need this code locally to run the
application and serve web pages to users accessing our load balancer URL.
3. Database Initialization Scripts
Files: src/backend/schema.sql and src/backend/seed.py
What they are: SQL commands to create database tables (users, flights, hotels, etc.) and a Python
script to populate those tables with dummy data.

Why we created them: A new database starts empty. We need these scripts to set up the structure
and provide initial data so the website functions immediately after deployment.
Where they are stored: Inside the EC2 instance, they are executed once during setup.
Why we store data in RDS instead of EC2: We use a separate Amazon RDS (Relational Database
Service) instance to store the actual data. RDS is fully managed, scalable, and secure. Keeping the
database separate from the EC2 web servers means that if a web server crashes, our data is safe and
intact in RDS.
4. Deployment & Automation Scripts
Files: build_yaml.py, deploy_now.py, deploy_now2.py, inject.py
What they are: Python scripts written to automate the deployment process.
Why we created them:
 build_yaml.py takes our local application code (src/ folder) and embeds it into the CloudFormation
blueprint.
 deploy_now2.py runs commands via AWS Systems Manager (SSM) to tell the live EC2 servers to pull
updates and restart.
Where they are stored: Only locally on the developer's machine. They are tools used by the
developer to push updates, so they do not need to be hosted on AWS.
What is the use: They save time and reduce human error when pushing new code changes to the live
production environment.
5. Server Configuration Files
Files: src/nginx/nginx.conf and src/backend/travel-backend.service
What they are: Configuration files for Nginx (a powerful web server) and Systemd (a Linux service
manager).
Why we created them:
 nginx.conf tells Nginx to take internet traffic coming on Port 80 and route it internally to our Python
app on Port 5000.
 travel-backend.service tells the Linux server to keep our Python app running in the background, and
to automatically restart it if the server reboots or the app crashes.
Where they are stored: In the EC2 instance at the system level (/etc/nginx/ and
/etc/systemd/system/).
