 # Week 7: Secure Authentication System
 Student Name: Aurore Marie Anaelle Chellapanaick 
 Student ID: M01068404
 Course: CST1510 -CW2 -  Multi-Domain Intelligence Platform 
## Project Description
 A command-line authentication system implementing secure password hashing
 This system allows users to register accounts and log in with proper pass
## Features
 - Secure password hashing using bcrypt with automatic salt generation
 - User registration with duplicate username prevention
 - User login with password verification- Input validation for usernames and passwords
 - File-based user data persistence
## Technical Implementation
 - Hashing Algorithm: bcrypt with automatic salting
 - Data Storage: Plain text file (`users.txt`) with comma-separated values
 - Password Security: One-way hashing, no plaintext storage- Validation: Username (3-20 alphanumeric characters), Password (6-50 characters)

# Week 8: Data Pipelines and CRUD (SQL)

## Project description
 This lab transitions the CST1510 Multi-Domain Intelligence platform project from simple file-based storage(Week 7's users.txt) to a robust and professional SQLite database.
 The main focus is the creation of a secure and scalable data management layer capable of handling data across three distinct domains: Cyber Incidents, Datasets Metadata, and IT Tickets. All project data is centralized with intelligence_platform.db, which also supports secure user authentication.

## Features
 Data Migration: Moves users from text file to database with password security preserved.

 Comprehensive Schema: Defines four key tables(users, cyber_incidents, datasets_metadata, it_tickets) with proper keys and relationships.

 Bulk data loading: Automates CSV-to-database import using Python and pandas.

 Full CRUD  functionality: Implements Create, Read, Update, and Delete operations for all data entities.

 Security: Uses parameterized SQQL queries for all database operations, preventing SQL injection.
 
 Authentication: Integrates bcrypt password hashing for secure logins and registration.

## Technical Implementation
 Database: SQLite(intelligence_platform.db)

 Programming Language: Python (with sqlite3, pandas, and bcrypt)

 Architecture: 
  -Seperate scripts for connecction, schema, and table CRUD functions
  -Clear seperation of business logic and data manipulation.

 Schema Overview: 
  -users: handles authentic data
  -cyber_incidents: Security event records linked to users
  -datasets_metadata: Stores info on available datasets
  -it_tickets: Tracks IT service requests

 This setup forms the secure, efficient foundation for the Multi-Domain Intelligence Platform, enabling scalable analytics and future web integration.
