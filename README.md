# TravelEase - AWS Travel Booking Platform

![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/mysql-%2300f.svg?style=for-the-badge&logo=mysql&logoColor=white)
![CloudFormation](https://img.shields.io/badge/CloudFormation-FF4F8B?style=for-the-badge&logo=amazon-aws&logoColor=white)

A highly available, scalable, and fully automated travel booking platform deployed on Amazon Web Services (AWS) using Infrastructure as Code (CloudFormation). 

This full-stack platform (HTML/CSS/JS Frontend, Python Flask Backend) allows users to seamlessly search and book Flights, Hotels, Cabs, Buses, and Holiday Packages. It features a custom VPC, secure database management, dynamic Auto Scaling, and load balancing to ensure the application remains fast and online even during massive traffic spikes.

## 🚀 Key Features
- **Dynamic Auto Scaling**: The application automatically spins up new EC2 backend servers if traffic increases and terminates them when traffic drops to save costs.
- **High Availability**: Traffic is intelligently routed via an Application Load Balancer (ALB) to healthy instances across multiple Availability Zones.
- **AI Chatbot Assistant**: Features an integrated NLP chatbot capable of live weather tracking, Wikipedia lookups, math, and booking status tracking.
- **Admin Dashboard**: Secure administrative portal to manage inventory, track revenue, and monitor registered users in real-time.
- **Infrastructure as Code (IaC)**: The entire environment (VPC, Subnets, EC2, RDS, ALB, Security Groups) is automated using a single AWS CloudFormation template.

## 🏗️ Architecture Highlights
- **VPC & Subnets**: Custom networking with Public Subnets for the ALB and Private Subnets for the backend servers and RDS database.
- **Compute Layer**: Python Flask backend hosted on Amazon Linux 2 EC2 instances, served via NGINX and Gunicorn (Systemd).
- **Database Layer**: Amazon RDS MySQL instance deployed in private subnets for maximum security.

## 📚 Documentation
I have created extensive documentation for this project in the \docs/\ folder:
- [\docs/PROJECT_ARCHITECTURE.md\](docs/PROJECT_ARCHITECTURE.md): A deep dive into the 3-Tier AWS Architecture with Mermaid diagrams.
- [\docs/APPLICATION_FEATURES.md\](docs/APPLICATION_FEATURES.md): An exhaustive guide to all user and admin features.
- [\docs/AWS_INTERVIEW_QnA.txt\](docs/AWS_INTERVIEW_QnA.txt): A Q&A guide explaining how to discuss this project in cloud engineering interviews.

*(Note: There is also a \README.txt\ inside every major folder explaining how to deploy that specific component manually).*

## ⚙️ How To Deploy
To deploy this infrastructure yourself:
1. Upload the \cloudformation/travel_booking_platform.yaml\ template to AWS CloudFormation.
2. Provide the required parameters (DB Password, Instance Type, etc.).
3. Wait for the stack to complete (approx. 10-15 mins).
4. Access the live web application via the Load Balancer DNS URL provided in the CloudFormation Outputs tab!
