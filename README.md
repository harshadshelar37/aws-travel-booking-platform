# AWS Travel Booking Platform (TravelEase)

![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)
![NodeJS](https://img.shields.io/badge/node.js-6DA55F?style=for-the-badge&logo=node.js&logoColor=white)
![MySQL](https://img.shields.io/badge/mysql-%2300f.svg?style=for-the-badge&logo=mysql&logoColor=white)
![CloudFormation](https://img.shields.io/badge/CloudFormation-FF4F8B?style=for-the-badge&logo=amazon-aws&logoColor=white)

A highly available, scalable, and fully automated travel booking platform deployed on Amazon Web Services (AWS) using Infrastructure as Code (CloudFormation). 

This platform allows users to book flights, hotels, and buses. It features a custom VPC, secure database management, dynamic Auto Scaling, and load balancing to ensure the application remains fast and online even during traffic spikes.

## Features
- **Dynamic Auto Scaling**: The application automatically spins up new EC2 backend servers if traffic increases and removes them when traffic drops.
- **High Availability**: Traffic is intelligently routed via an Application Load Balancer (ALB) to healthy instances across multiple Availability Zones.
- **Secure Secrets Management**: Database passwords and environment variables are securely stored in AWS Systems Manager (SSM) Parameter Store.
- **Infrastructure as Code**: The entire environment (VPC, Subnets, EC2, RDS, ALB, Security Groups) is automated using a single AWS CloudFormation template.

## Architecture Highlights
- **VPC & Subnets**: Custom networking with Public Subnets for the ALB and Private Subnets for the backend servers and RDS database.
- **Compute Layer**: Node.js backend hosted on Amazon Linux 2023 EC2 instances launched via a Launch Template.
- **Database Layer**: Amazon RDS MySQL instance deployed in private subnets for maximum security.

## How It Was Built
For a step-by-step simple explanation of how the AWS infrastructure was designed and created, please see the [INFRA_SETUP.md](INFRA_SETUP.md) file!

## Setup / Deployment
To deploy this infrastructure yourself:
1. Upload the `cloudformation/travel_booking_platform.yaml` template to AWS CloudFormation.
2. Provide the required parameters (DB Password, Instance Type, etc.).
3. Wait for the stack to complete, and access the application via the Load Balancer DNS name provided in the CloudFormation Outputs tab.
