# online-bookstore

# Setup Instructions

1. Clone the Repository:
  git clone https://github.com/rakn7032/online-bookstore.git

2. Create and Activate Virtual Environment:
  python -m venv venv  # on mac
  source venv/bin/activate  # on mac

3. Install Dependencies:
  pip install -r requirements.txt

4. Create the PostgreSQL Database:
  Create a PostgreSQL database named “online_bookstore”  and a user named “admin1”
 with the password “admin@123”. 
Grant all privileges on the database to this user.

  Save the database details for later use in a settings.py
  
5. Configure settings.py file in project:
   
    DB_ENGINE='django.db.backends.postgresql'
    DB_NAME=’online_bookstore’
    DB_USER='admin1'
    DB_PASSWORD='admin@123'
    DB_HOST='localhost'
    DB_PORT='5432'

6. Apply Migrations:

  • python manage.py makemigrations
  • python manage.py migrate

# Api Endpoints

Access all API endpoints through the Postman collection link below. This collection provides comprehensive API documentation, including details on requests, responses, exceptions, and additional notes for each endpoint.

Postman Collection Link: https://documenter.getpostman.com/view/37485860/2sAXjRWVNx
