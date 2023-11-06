create database mydb; /*employees creates the database*/
use mydb; # uses the database
drop database mydb; # drops the database
alter database mydb read only = 1; # make the database readonly
alter database mydb read only = 0; # readonly can be dropped using this.

# creating tables
create table employees (
    employee_id int,
    first_name varchar(50),
    last_name varchar(50),
    hourly_pay decimal(5, 2), /*max digit is 5, decimal is 2*/
    hire_date date
);
use mydb;
drop database mysql;
select * from employees;
rename table employees to workers;

alter table employees
add phone_number varchar(15);

alter table employees
rename phone_number to email;

alter table employees
modify email varchar(100);

alter table employees
modify email varchar(100)
after last_name; # make the email colunm come after the last name

alter table employees
modify email varchar(100)
first;

alter table employees
drop column email;

# inserting values into tables

insert into employees
values  (1, 'Eugene', 'Krabs', 25.00, 2023-01-02),
		(2, 'spuidward', 'tentacles', 15.00, 2023-01-03),
        (3, 'spongebob', 'Squarepant', 12.50, 2023-01-04),
        (4, 'Patrick', 'Star', 12.50, 2023-01-06),
        (5, 'Sandy', 'Cheeks', 17.25, 2023-01-06);
        
        
# insert into specific columns
insert into employees (employee_id, first_name, last_name)
values (6, "sheldon", 'Plankton');


select *
from employees
where hourly_pay >= 15; # != works too

select *
from employees
where hourly_pay is null; # for null and boolean us is and is not

# updating the value of a cell
select * from employees;
update employees
set hourly_pay = 10.25
where employee_id = 6; # where clause determines the cell

 
update employees
set hourly_pay = 10.25, # we can use null
	hire_date = '2023-01-07' # setting multiple fields
where employee_id = 6;

# without specifying the where, the update will happen across. where, specifies the cell.

delete from employees
where employee_id = 6; # specifying where we delete from

#redo and undo
set autocommit = off; # transcations don't save automatically
commit; 
Delete from employees;
rollback; # undo my delete changes
commit; # use commit to save the changes, they don't save automatically.
select * from employees;

create table test(
	my_date Date,
    my_time time,
    my_datetime datetime
    
);
select * from test;
insert into test
values(current_date(), current_time(), Now()); #current date, current time and current date and time

drop table test;

# unique constraint, ensuring that all values in a column are different
create table products (
	product_id int,
    product_name varchar(25) unique, # unique makes it impossible to enter the same product name twice
    price decimal (4, 2)
);

alter table products
add constraint
unique(product_name); # this is how to do it after being created.

select * from products;

insert into products
values  (100, 'hamburger', 3.99),
		(101, 'fries', 1.89),
        (102, 'soda', 1.00),
        (103, 'ice cream', 1.49);
        

# adding not null constraint. we can't enter a null value
create table products (
	product_id int,
    product_name varchar(25) unique, 
    price decimal (4, 2) not null # not null is added 
);        

alter table products
modify price decimal(4, 2) not null; # adding the not null after. 

# check constraints (at least a above or below a value)
create table employees (
    employee_id int,
    first_name varchar(50),
    last_name varchar(50),
    hourly_pay decimal(5, 2), /*max digit is 5, decimal is 2*/
    hire_date date,
    constraint chk_hourly_pay check(hourly_pay >= 10.00) #adding a check and gives it a name
);

alter table employees
add constraint chk_hourly_pay check(hourly_pay >= 10.00);

alter table employees
drop check chk_hourly_pay; # deleting a check
select * from employees;

# Default constraint
select * from products;

insert into products
values (104, 'straw', 0.00),
		(105, 'napkin', 0.00),
        (106, 'fork', 0.00),
        (107, 'spoon', 0.00);
        
delete from products
where product_id >= 104;

create table products (
    product_id int,
    product_name varchar(25),
    price decimal(4, 2) default 0 # this is how to make default values to zero
);

alter table products
alter price set default 0; # after table creation

insert into products (product_id, product_name)
values (104, 'straw'),
		(105, 'napkin'),
        (106, 'fork'),
        (107, 'spoon');
        
# ceating a transations table and recording the transaction with the actual date
create table transactions (
	transaction_id int,
    amount decimal(5, 2),
    transcation_date datetime default now()
);
select * from transactions;

insert into transactions (transaction_id, amount)
values (1, 4.99);

drop table transactions;

# primary key constraint
create table transactions (
	transaction_id int primary key,
    amount decimal(5, 2) 
);
select * from transactions;

alter table transactions
add constraint
primary key(transaction_id); # only one primary key can be added.

insert into transactions
value (1001, 1.89); # we cannot have a non unique primary key
select * from transactions;

select amount
from transactions
where transaction_id = 1001;

#auto increment
drop table transactions;

create table transactions (
	transaction_id int primary key auto_increment,
    amount decimal(5, 2)
);
select * from transactions;

insert into transactions (amount)
value (4.99); # we can update from here. sql is like a macro recorder.
select * from transactions;

alter table transactions
auto_increment = 1000; # starts the incremetor from 1000

# foreign key constraint (used to link tables)

create table customers (
customer_id int primary key auto_increment,
first_name varchar(50),
last_name varchar(50)
);

insert into  customers (first_name, last_name)
values ('fred', 'fish'),
		('larry', 'lobster'),
        ('bubble', 'bass');
select * from customers;

drop table transactions;

create table transactions (
	transaction_id int primary key auto_increment,
    amount decimal (5, 2),
    customer_id int,
    foreign key (customer_id) references customers(customer_id) #assigns the id from customers table to the transactions table (customer_id column)

    );
    
    select * from transactions;
    
    alter table transactions
    drop foreign key transactions_ibfk_1; # this is the name assigned on the files menu
    
    alter table transactions
    add constraint fk_customer_id
    foreign key (customer_id) references customers(customer_id); # adding a foreign key after.alter
    
    delete from transactions;
    select * from transactions;
    
alter table transactions
auto_increment = 1000;

insert into transactions (amount, customer_id)
values 
          (4.99, 3),
          (2.89, 2),
          (3.38, 3),
          
          (4.00, 1);
select * from transactions;


delete from customers
where customer_id = 3; # wont work because it isn't the primary key


#joins

insert into transactions (amount, customer_id)
values 
          (1.00, null);

insert into customers (first_name, last_name)
values ('poppy', 'puff');

#inner join
select *
from transactions inner join customers # transactions will be on the left
on transactions.customer_id = customers.customer_id;

select transaction_id, amount, first_name, last_name
from transactions inner join customers # transactions will be on the left
on transactions.customer_id = customers.customer_id;

# left join (all data from left table. leave missing as null on right)
select transaction_id, amount, first_name, last_name
from transactions left join customers # transactions will be on the left
on transactions.customer_id = customers.customer_id;

# right join (all data from right table, matching from left)
select transaction_id, amount, first_name, last_name
from transactions right join customers # transactions will be on the left
on transactions.customer_id = customers.customer_id;

# functions in mysql
# count
select count(amount) 
from transactions;

select count(amount) as 'todays transactions'
from transactions;

select max(amount) as maximum # min, avg, sum
from transactions;

select * from employees;

#concatenation
select concat(first_name,' ', last_name) as full_name
from employees;

#logical operators in mysql
alter table employees
add column job varchar(25) after hourly_pay;
select *from employees;

update employees
set job = 'cook'
where employee_id = 3;

#and
select * 
from employees
where hire_date < '2023-01-5' and job = 'cook';

#or
select * 
from employees
where job = 'chasier' or job = 'cook'; 

#not
select *
from employees
where not job = 'manager'; 

#use between when working with the same column
select *
from employees 
where hire_date between '2023-01-04' and '2023-';
#where job in ('cook', 'cahier', 'janitor'); # using the 'in' operator

# wild card characters % _
select * from employees
where first_name like 's%'; # firstname begining with 's'

select * from employees
where last_name like '%w'; # last name ending with 'w'

select * from employees
where job like '_ook'; # contains the ook, only one character in front
# where hire_date like '____-__-03;

# order by clause
select * from employees
order by last_name desc; # asc for ascending (default) desc for desending

select * from transactions
order by amount, customer_id; # if there is a tie, another column to compare by.

#limit clause limit
select * from customers
order by last_name
limit 4;

# using limit offset
select * from customers
order by last_name
limit 4, 1; # displays the fourth row, only 1 row is displayed

#union
select first_name, last_name from employees
union
select first_name, last_name from customers; # if they are different colunm numbers pls specify the rows to union
# use union all when you want to include duplicates. normal union wouldn't allow that

#self join (joining another copy of a table to itself)
alter table customers
add referral_id int;
select * from customers;

update customers
set referral_id = 2
where customer_id = 4;
select * from customers;

select * 
from customers as a
inner join customers as b
on a.referral_id = b.customer_id;

select a.customer_id, a.first_name, a.last_name,
		concat(b.first_name, ' ', b.last_name) as 'referred_by'
from customers as a
inner join customers as b
on a.referral_id = b.customer_id;

# views are not tables but the take a snap shot of the table

create view employee_attendance as # notice the as ended this line
select first_name, last_name
from employees;

select * from employee_attendance
order by last_name asc;

drop view employee_attendance;

alter table customers
add column email varchar(50);

update customers
set email = 'eeass@gmail.com'
where customer_id = 4;

create view customer_emails as
select email 
from customers;

select * from customer_emails;

# indexes (BTree data structure)

show indexes from customers;
select * from customers;


create index last_name_idx
on customers(last_name); # creaating an index for last name

# multiple indexes
create index last_name_first_name_idx
on customers(last_name, first_name);

show indexes from customers;

# droping index
alter table customers
drop index last_name_idx;


# subqueries. query within another query
select first_name, last_name, hourly_pay, 
(select avg(hourly_pay) from employees) as avg_pay
from employees;

select first_name, last_name, hourly_pay
from employees
where  hourly_pay > (select avg(hourly_pay) from employees);

select * from transactions;

select first_name, last_name
from customers
where customer_id in
(select distinct customer_id
from transactions
where customer_id is not null);
select * from transactions;


alter table transactions
add column order_date date;

update transactions
set order_date = '2023-01-03'
where transaction_id is null;

# using group by
select sum(amount), order_date
from transactions
group by order_date;

select sum(amount), customer_id

# NB: we can't use a where with group by

select count(amount), customer_id
from transactions
group by customer_id
having count(amount) > 1; # use 'having' instead of where


# roll up clause --shows grand total
select sum(amount), order_date
from transactions
group by order_date with rollup; # displays the grand total

# on delete set null, on delete cascade
select * from customers;
delete from customers
where customer_id = 4;

set foreign_key_checks = 1; # foreign keys cannot be deleted.

insert into customers
values (4, 'Poppy', 'Puff',2,  'PPuff@gmail.com');


create table transactions (
	transaction_id int primary key,
    amount decimal(5, 2), 
    customer_id int,
    order_date date,
    foreign key(customer_id) references customers(customer_id)
    on delete set null); # how to set it in table definition.

alter table transactions
drop foreign key fk_customer_id;

alter table transactions
add constraint fk_customer_id
foreign key(customer_id) references customers(customer_id)
on delete set null; # adding on delete after table creation

alter table transactions
add constraint fk_transactions_id
foreign key (customer_id) references customers(customer_id)
on delete cascade;

# stored procedure (like a function)
DELIMITER $$  #changing a delimeter to something else
create procedure get_customers()
begin
select * from customers;
end$$
DELIMITER ; 

call get_customer();

DELIMITER $$ # change delimiter so that ';' dosen't terminate within the procedure
create procedure find_customer(in id int) # find customer by their id
begin
	select * from customers
    where customer_id = id;
end$$
DELIMITER ;

call find_customer(4); # 4 is the id

# triggers make changes automatically

alter table employees
add column salary decimal(10, 2) after hourly_pay;
select * from employees;

update employees
set salary = hourly_pay * 2080;
select * from employees;


#trigger
create trigger before_hourly_pay_update
before update on employees
for each row
set new.salary = (new.hourly_pay * 2080);

update employees
set hourly_pay = 50
where employee_id = 1;

update employees
set hourly_pay = hourly_pay + 1;

delete from employees
where employee_id = 6;

create trigger before_hourly_pay_insert
before insert on employees
for each row
set new.salary = (new.hourly_pay * 2080);

insert into employees
values(6, 'sheldon', 'Plankton', 10, null, 'janitor', '2023-01-07', 5);

create table expenses (
	expense_id int primary key,
    expense_name varchar(50),
    expense_total decimal(10, 2)
);
select * from expenses;

insert into expenses
values (1, 'salaries', 0),
		(2, 'supplies', 0),
        (3, 'taxes', 0);
        
update expenses
set expense_total = (select sum(salary) from employees)
where expense_name = 'salaries';

select * from expenses;

create trigger after_salary_delete
after delete on employees
for each row
update expenses
set expense_total = expense_total - old.salary
where expense_name = 'Salaries';

delete from employees
where employee_id = 6;
select * from expenses;

create trigger after_salary_insert
after insert on employees
for each row
update expenses
set expense_total = expense_total + new.salary
where expense_name = 'salaries';

insert into employees
values (5, 'sheldon', 'plankton', 10, null, janitor, '2023-01-01');

create trigger after_salary_update
after update on employees 
for each row
update expenses
set expense_total = expense_total + (new.salary - old.salary)
where expense_name = 'salaries';

update employees
set hourly_pay = 100
where employee_id = 1;
select * from expenses;
