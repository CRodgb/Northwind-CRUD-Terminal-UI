# Northwind-CRUD-Terminal-UI
This is a terminal-based Python application for managing the northwind database. It allows users to add customers, orders, print pending orders, remove orders, and ship orders, all from a simple interface.

## Features  
* Add new customers
* Create new orders (for single or multiple products)  
* View all pending (unshipped) orders  
* Remove Existing orders  
* Mark orders as "shipped", which validates inventory and updates the order status  

## Requirements    
### Software  
* Python 3.x  
* Running MySQL Server  
### Python Dependencies 
All Python packages are listed in the `requirements.txt`

## Setup & Installation
### 1. Clone the repository:  
```bash 
git clone https://github.com/your-username/northwind-crud-ui.git
cd northwind-crud-terminal-ui
```
### 2. Install Python Dependencies:
  ```bash
  pip install -r requirements.txt
  ```
### 3. Setup the database:
* MySQL server running on `localhost`
* Create a new, empty database named `northwind`
  ```sql
  CREATE DATABASE northwind;
  ```
* Import the schema and data from the `northwind.sql` file (provided in repo)
  ```bash
  mysql -u [your_mysql_username] -p northwind < northwind.sql
  ```
* Create the project-specific user:  
  * **Username:** nwcrud
  * **Password:** admin
* Grant `nwcrud` full privileges on the `northwind` database
### 4. Run the application:
  ```bash
  python main.py
  ```
