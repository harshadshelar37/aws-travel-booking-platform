===========================================================================
DATABASE - MYSQL SCHEMA & SEED DATA
===========================================================================

WHAT THIS FOLDER IS FOR:
This folder holds your database structure.
- schema.sql: The SQL commands that create your tables (users, flights, hotels, buses, bookings).
- sample_data.sql: Mock data so your frontend search actually returns results when testing.

HOW TO DEPLOY MANUALLY FROM SCRATCH:
Because your RDS database is private (inside a Private Subnet), you cannot connect to it directly from your home computer. You must connect through your EC2 instance (which acts as a Bastion Host).

1. SSH into your EC2 instance.
2. Install the MySQL client:
   sudo yum install mysql -y
3. Copy the 'schema.sql' and 'sample_data.sql' files from your computer to the EC2 instance using SCP.
4. Run the schema file against your RDS instance:
   mysql -h <YOUR-RDS-ENDPOINT> -u admin -p travel_db < schema.sql
   (It will prompt you for your password).
5. Run the sample data file:
   mysql -h <YOUR-RDS-ENDPOINT> -u admin -p travel_db < sample_data.sql

Your database is now fully populated!
