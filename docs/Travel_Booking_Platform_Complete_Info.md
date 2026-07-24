Complete Project Information & Architecture
Project: WanderLust Travel Booking Platform
This document provides a comprehensive overview of the entire Travel Booking Platform. It details the
technologies used, the infrastructure, the file structure, and why specific choices were made. This is
designed to serve as a complete reference for explaining the project to an interviewer.
1. Project Overview
What it is: A full-stack web application that allows users to search and book Flights, Hotels, Cabs, and
Holiday Packages. It also features an Admin Dashboard to track total revenue, bookings, and users.
Tech Stack Used:
 Frontend: HTML, CSS, JavaScript (Vanilla)
 Backend: Python with Flask framework
 Database: MySQL
 Cloud Provider: Amazon Web Services (AWS)
 Infrastructure as Code: AWS CloudFormation
2. Cloud Infrastructure (AWS)
The project uses a highly scalable 3-tier architecture on AWS:
 Application Load Balancer (ALB): Acts as the entry point. It receives incoming web traffic and
routes it to available EC2 instances. If an instance goes down, ALB redirects traffic to healthy ones.
 Auto Scaling Group (ASG) & EC2: The web servers. ASG ensures that if traffic spikes, new EC2
instances are automatically launched to handle the load.
 Amazon RDS (MySQL): The managed database. It is placed in a private subnet so it is completely
hidden from the public internet for security.
3. Code Organization & File Structure
Frontend (src/frontend/)
 Contains index.html, style.css, and app.js. These run in the user's browser.

 Why separate frontend? Keeping the frontend separate from the backend allows for better
performance and a cleaner API-driven design.
Backend API (src/backend/app.py)
 This Python Flask app defines API endpoints (e.g., /api/flights, /api/book).
 Where it runs: It runs on the AWS EC2 instances on port 5000.
Database Scripts (src/backend/schema.sql & seed.py)
 What they do: schema.sql creates tables for users, bookings, etc. seed.py inserts dummy data.
 Why we use them: When an EC2 instance launches, it runs seed.py to automatically populate the
RDS database so the website is immediately usable without manual setup.
4. Automation & Deployment (Infrastructure as Code)
CloudFormation (cloudformation/travel_booking_platform.yaml)
 What it is: A massive YAML file that defines every AWS resource (VPC, Security Groups, ALB, ASG,
RDS).
 Why we use it: Instead of manually creating resources via the AWS Console, we upload this file.
AWS reads it and automatically provisions the entire architecture. This guarantees zero human error
and allows the infrastructure to be version-controlled.
Deployment Scripts (build_yaml.py & deploy_now2.py)
 build_yaml.py: Takes our local python and HTML files and injects them directly into the
CloudFormation YAML template.
 deploy_now2.py: Connects to the AWS EC2 instance remotely to trigger updates.
5. Security & Server Configuration
 Nginx (src/nginx/nginx.conf): Used as a reverse proxy on the EC2 instances. It takes HTTP
requests on Port 80 and passes them to our Flask app on Port 5000 securely.
 Systemd (travel-backend.service): A Linux service manager. We use it to ensure the Flask app
automatically starts when the EC2 instance boots up, and restarts if it ever crashes.
 Security Groups: Firewalls are configured so only the Load Balancer can talk to the EC2 instances,
and only EC2 instances can talk to the RDS database.
