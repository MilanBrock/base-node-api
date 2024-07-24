## Introduction
This is a TypeScript Node.js API application.


## Installation
After cloning the repository, run the following command to install the necessary dependencies:
```npm install```  


## Setup
Create a .env file in the root directory of the project based on the provided .env.example file. This file contains environment variables required for the application.
```cp .env.example .env```
Fill in the necessary values in the .env file.  


## Database Setup
To set up a local PostgreSQL database, follow these general steps:

Install PostgreSQL:  

Download and install PostgreSQL from https://www.postgresql.org/download/.  
Start PostgreSQL service:  
 
Ensure that the PostgreSQL service is running.  
Create a new database:  

Open a terminal and run the PostgreSQL command-line tool (psql).
Run the following commands to create a new user and database:
```
CREATE USER your_username WITH PASSWORD 'your_password';
CREATE DATABASE your_database_name;
GRANT ALL PRIVILEGES ON DATABASE your_database_name TO your_username;
```
Update the .env file:
Add your database configuration details (username, password, database name) to the .env file.


## Starting the Application
To start the application, use the following command:
```
npm start
```

## Example API Calls
You can find example API calls in the exampleCalls folder. This folder contains an export of requests that can be used with Postman.



