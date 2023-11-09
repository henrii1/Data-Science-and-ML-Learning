!pip install mysql-connector
!pip show mysql-connector # shows the version installed
!pip install --upgrade mysql-connector # use -U for short
!pip list # lists all installed packages
!pip freeze >requirements.txt # tells pip to save all libraries present in your coding environment to the requirement.txt file
!pip uninstall mysql-connector # uninstalling packages

# connecting python to mysql
!pip install mysql-connector 
import mysql.connector as connector

connection = connector.connect(user = 'Emerald', password = 8687, port = 3306, 
                               host = 'localhost', database = 'mydb') # establishing a connection host could be localhost

# using the errorcode library to handle mysql exceptions
import mysql.connector as connector
from mysql.connector import errorcode

try:
    connection = connector.connect(user = 'root', password = 8687, database = 'mydb')
except connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print('connection user or password are incorrect')
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print('database does not exist')
    else:
        print(err)

#use python to create database and tables after connection creation
cursor = connection.cursor() # points to where the required data is stored in the database

create_database_query = """ CREATE DATABASE little_lemon""" # assign string sql queries to python variables
cursor.execute(create_database_query)

use_database = """ use little_lemon"""
cursor.execute(use_database)

create_table = """
create table bookings (
itemID int primary key auto_increment,
name varchar(50),
type varchar(50),
price int,
)
"""
cursor.execute(create_table)

# using cursors to point to data and transfer to other variables
DECLARE guest_booking_details CURSOR  # declaring a cursor
select * from guest_bookings         #sql statement within cursor

OPEN guest_booking_details           #opening the cursor

FETCH guest_booking_details INTO booking_data # fetch results and store in python variable. booking_data is a python variable


# cursor classes
buffered_cursor = connection.cursor(buffered = True) # for buffered cursor
raw_cursor = connection.cursor(raw = True) # for raw cursor
dictionary_cursor = connection.cursor(dictionary = True) # for dictionary cursor

select_smth = 'select * from orders'

# use multiple cursors for different use cases
buffered_cursor.execute(select_smth) 
cursor.execute(select_smth)


# executing crud operations with python

import mysql.connector as connector
connection = connector.connect(user = 'root', password = 8687)

cursor = connection.cursor()


create_database_query = """ CREATE DATABASE little_lemon""" # assign string sql queries to python variables
cursor.execute(create_database_query)

use_database = """ use little_lemon"""
cursor.execute(use_database)

create_table = """
create table bookings (
itemID int primary key auto_increment,
name varchar(50),
type varchar(50),
price int,
)
"""
cursor.execute(create_table)

my_sql_insert_query = """ 
insert into bookings (itemID, name, type, price)
values (1, 'gh', 'er', 244)

"""
cursor.execute(my_sql_insert_query)
connection.commit()

# reading the data from the database
read_data_query = """ select * from bookings """
cursor.execute(read_data_query)
cols = cursor.column_names
results = cursor.fetchall() # fetches all results as tuple. will change for other cursor types
print(cols) # prints the columns on the table
print(results) # prints the table data as tuples

for result in results:
    print(result)     #orders each result in a new line.



# update and deleting operations
update_booking = """
update bookings
set TableNo = 10
where boodkingID = b
"""
cursor.execute(update_booking)

connection.commit()
 # write all other sql code in python using these methods.

#using datatime in python
import datetime as dt
current_time = dt.datetime.now()
print(current_time) # date and time
print(current_time.date()) # date
print(current_time.time()) # time

#function2
week = dt.timedelta(days = 7)
print(week) # returns the date 7 days from now

# solving a datetime problem
import mysql.connector as connector
connection = connector.connect(user = 'root', password = 8687)
cursor = connection.cursor()
cursor.execute('use little_lemon')

import datetime as dt
select_stmt = """ select * from bookings"""
cursor.execute(select_stmt)
print(cursor.column_names)

for row in cursor:
    booking_id = row[0]
    booking_slot = row[4]
    new_booking_slot = booking_slot + dt.timedelta(hours = 1) # one hour ahead of what is stored
    print('booking_id {} is moved from {} to{}' .format(booking_id, booking_slot, new_booking_slot))


# using stored procedures on python do not use the delimiter option because the string typically doesn't include a semicolon

stored_procedure = """something"""

cursor.execute(stored_procedure)
cursor.callproc("procedure_name")
results = next(cursor.stored_results())
dataset = results.fetchall()

for data in dataset:
    print data