# Infrastructure Setup Guide

This document explains how the AWS infrastructure for the Travel Booking Platform was created step-by-step in simple terms. We used **AWS CloudFormation** to automate the creation of all resources.

## Step 1: Networking Foundation (VPC)
- **Virtual Private Cloud (VPC)**: We created a private network in AWS to securely host our application.
- **Subnets**: The network is divided into public subnets (for resources that need internet access, like the Load Balancer) and private subnets (for the database).
- **Internet Gateway**: Attached to the VPC to allow traffic in and out of the public subnets.

## Step 2: Database Layer (Amazon RDS)
- **Subnet Group**: We placed the database in the private subnets so it cannot be directly accessed from the internet.
- **MySQL RDS Instance**: We created a managed MySQL database to store travel bookings, users, flights, buses, and hotels.
- **Security Group**: Configured to only allow database connections from our application servers.

## Step 3: Compute Layer (Amazon EC2 & Auto Scaling)
- **Launch Template**: A blueprint for our virtual servers (EC2 instances). It automatically installs Python, Node.js, configures the database connection securely using AWS Systems Manager (SSM), and starts the backend and frontend apps on boot.
- **Auto Scaling Group**: Automatically adds or removes EC2 instances based on traffic. This ensures the platform stays online even if there's a surge of users booking trips.
- **Security Group**: Configured to allow web traffic (HTTP on port 80 and 8080) from the Load Balancer.

## Step 4: Traffic Routing (Application Load Balancer)
- **Load Balancer (ALB)**: Acts as the front door for the application. It receives all user traffic and evenly distributes it across the healthy EC2 instances in the Auto Scaling Group.
- **Target Groups**: Used by the ALB to monitor the health of the EC2 instances. If an instance fails, the ALB stops sending traffic to it.

## Step 5: Automation & Configuration
- **AWS Systems Manager (SSM)**: Instead of hardcoding the database password in our code, we securely stored it in SSM Parameter Store. The EC2 instances fetch the password at startup to connect to the database.
- **CloudFormation**: All of the above steps were written as code (YAML). By deploying the template, AWS automatically built the entire environment in exactly the right order!
