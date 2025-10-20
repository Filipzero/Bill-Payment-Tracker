# Billing-Payment-Tracker
This project is a command line application built using python that helps keep track of bills like Internet, Water and Electricity. Each user in the system is unique and has their own set of bills which are categorized accordingly. Each bill has its own attribute that sets it apart like electricity bills that track the kWh usage, water bills that track cubic meter consumption and internet bills that track data usage in GB. 

This system provides key features such as:

* **User based bill management**
* **Monthly expenses calculation**
* **Billing and payment history tracking**

<h4>1. User based bill management</h4>

The name that the user chooses is unique in the database. 
Every bill and payment that is being stored will be associated with the specific name given.

<h4>3. Monthly expenses calculation</h4>

Searches the database for the month and year that the user has chosen and calculates their monthly expenses.

<h4>2. Billing and payment history tracking</h4>

Storage and retrieval of the user's information as well as their bills.
Maintain user's records with details such as type of bill(Water, Electricity, Internet), provider, amount payed, due_date and any additional relevant data.

## Getting started

## Prerequisites

1. Python 3.X installed on your system.
2. All the required python libraries listed in libraries.txt
3. Mysql 8.0

## Installation

1. Download the repository and extract all the files.

2. Make sure you have all the prerequisites:
   - Python 3.x
   - Required Python libraries
   - MySQL 8.0 installed

3. Set up MySQL:

 **On Linux / Mac** 
 
   * Open a terminal and run:
     ```bash```
     mysql -u your_username -p < project.sql

   * Replace your_username with your MySQL username.

   * Enter your MySQL password when prompted.

 **On Windows**
   * Make sure MySQL is added to your system PATH (MySQL’s bin folder).
   * Open Command Prompt and run:
   ```cmd```
   mysql -u your_username -p < project.sql

4. The database Bills is now ready, and all tables are created.

## Use

1. Write your name to store all the bills and payments specifically to that user only.

2. Calculate monthly expenses of a chosen month and year.

3. Storage and retrieval of the user's information as well as their bills.
