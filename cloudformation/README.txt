===========================================================================
CLOUD FORMATION - INFRASTRUCTURE AS CODE
===========================================================================

WHAT THIS FOLDER IS FOR:
This folder contains 'travel_booking_platform.yaml'. This single file contains the blueprint for the entire AWS infrastructure for the project. When uploaded to AWS CloudFormation, AWS automatically creates the Virtual Private Cloud (VPC), Subnets, Application Load Balancer (ALB), Auto Scaling Groups for EC2 instances, and the RDS MySQL Database.

HOW TO DEPLOY MANUALLY FROM SCRATCH:
1. Log in to your AWS Management Console.
2. Search for 'CloudFormation' in the top search bar.
3. Click 'Create stack' -> 'With new resources (standard)'.
4. Select 'Template is ready' and 'Upload a template file'.
5. Click 'Choose file' and upload 'travel_booking_platform.yaml' from this folder.
6. Click 'Next'.
7. Enter a Stack Name (e.g., 'travel-booking-prod').
8. Fill in the Parameters:
   - EnvironmentName: prod
   - DBUsername: admin
   - DBPassword: (Enter a strong password)
   - NotificationEmail: your_email@example.com (for Auto Scaling alerts)
   - KeyPairName: (Select your existing EC2 Key Pair to allow SSH access)
9. Click 'Next' through the remaining screens.
10. On the Review page, scroll to the bottom, check the box that says 'I acknowledge that AWS CloudFormation might create IAM resources', and click 'Submit'.

AWS will now take about 10-15 minutes to build your entire infrastructure!
Once the status says 'UPDATE_COMPLETE' or 'CREATE_COMPLETE', click the 'Outputs' tab.
You will see the 'WebsiteURL'. Click it to view your live website.