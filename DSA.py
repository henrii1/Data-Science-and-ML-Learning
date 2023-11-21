# python
groceries = [] # this evaluates to false when there isn't any value within
if groceries:
    print('done') # doesn't print because it evaluates to false

# in interger is 0, it evaluates to false.

# Exceptions

#raise RuntimeError('error')
try:
    results = 14/0
except ZeroDivisionError: # we want the except to function specific to ZeroDivisionError
    results = 14/2

# except Exception: Catches all types of exceptions
except Exception as e;
    print({str(e)})

# we can also pass multiple exceptions to an except
except(ZeroDivisionError, TypeError):

# .items(), .keys(), .values() method is specifically used with dictionaries in python 

#finding the methods available to an object. List, tuple, dictionary etc
for method in dir(tuple()): # this could be any other object.
    if method.startswith('__'):
        print(method)


# lists
 
# insert method
names = []
names.append('sugar') # adds sugar to end
names.insert(1, "sugar") # adds sugar to index 1

shopping = []
shopping.append(["sugar", 'salt']) # yeilds a nested list
shopping.extend(["sugar", 'salt']) # yeilds an extended list

shopping.pop(1) # removes from the list using index
shopping.remove('salt')  # use remove to specify the value

# Dictionaries
contact = {}
contact['height'] # height is meant to be the key
print(contact['height']) # should print the value associated with this key

# using the .get() method will return None if key isn't found.
result = contact.get('height')
print(result)

result = contact.get('height', '6ft')
print(result) # if result is None, the .get method assigns default value '6ft'

result.pop("age") # pops out the value and key 

#functions

# unpacking arguments '*args' converts to a tuple the parameters are positional arguments
# unpacking '**Kwargs' unpacks to a dictionary enter the parameters as keyword arguments to store

#classes

class cars(): # basic class
    pass

car = cars() # instantiating the class

dir(car) # lists all the default methods associated with this class object

class car ():
    def __init__(self, brand):
        print(f"brand is {brand}") # parameters can be used directly to perform operations
        self.car_brand = brand  # variables however must be associated to the class as a class attribute
    def count(self, val):  # class methods must be on the same line level as the __init__ and must be associated with the class
        print(self.car_brand) # within the __init__ method, we can print brand but without, we'll have to assign it to a class attribute 'self.car_brand'
        counting = val # within a normal function, we can assign without referring to the class
        return val # used within the function and never without.
    def repeat(self, num):
        recursion = self.count(num) # using a function within a function requires referring to the class


# Generally, if you want a variable to be reusable outside the class method it was defined, define it as a class attribute using the 'self.name' = value
#NB: we can use a function defined above in one defined below

def expense(self, amount):
    'do something'
    self.report() #report is used here but defined below
def report(self):
    print(f"some things")


#inheritance
class pet:
    def eat(self):
        self.food = self.food - self.appetite # we didn't define the class attributes, we just defined the operation
        print(self.food) 

class dog(pet):
    def __init__(self, food, appetite):
        self.food = food                 # we defined the class attribute after inheritance
        self.appetite = appetite

#print all the methods of a class
dogs = dog()

for attribute in dir(dogs):
    if attribute.startswith("__"):
        continue
    print(attribute)  # printing all attribute except those starting with '__'


# python modules and packages
pwd # prints the working directory
touch pandas.py # creates a file
mkdir pack 
cd pack 
cat __init__.py
cat module.py


# import modules
import pandas
from pandas import x

# from packages (the __init__.py file tells python that this directory is a package)
import pack.module # importing a module within a package

pack.module.func() # using a function from the module within a package

# another way is to import modules within the __init__.py file. that way, when the package is imported, modules automatically become available


import sys

def main(arguments):
    print("hooked")
    for argument in arguments:
        print(argument)

if __name__ == '__main__': # checks if script is being run as a main program and not imported as a module
    main(sys.argv) #prints 'hooked' the 'file_name' then all comand line arguments passed to in on the command line.


# virtual environments in python (useful for installing dependencies) the following are command line or power shell code.

python3 -m venv myenv # venv is a new environment
tree myenv #lists all python packages and modules in this environment
which python # shows the directory of the python and includes the virtual environment if within.
# activating environment for cmd
myenv\Scritps\activate   
# activating environment for powershell
.\myenv\Scripts\Activate

echo 'flask' >requirements.txt # writes 'flask' into the requirement.txt file

pip install -r requirement.txt # installing all in the requirement.txt file

deactivate # used to deactivate the virtual environment hence all installed or imported won't be available anymore.


# Testing (writing and executing them)
cd preferred_directory #
cd - # takes you to the previous directory.

%%writefile addition.py 
def add(a,b):
    return(a + b)
def sub(a, b):
    return(a - b)

%%writefile test_addition.py 
pip install pytest
import addition
import pytest 
def test_add():
    assert addition.add(4, 5) == 9
def test_sub():
    assert addition.sub(4, 5) == -1

#running the test_addition.py file should show two passed or 1 passed and one failed.

# Using Unitest
import unittest
class TestExm(unitest.TestCase): # Interit the base class'unitest.TestCase'
    def test_assertion(self):
        self.assertEquals('some string', 'others') #checking equals. you can add functions to this method
        # we can also use self.assertNotAlmostEqual

unitest.main(argv=[''], verbosity = 2, exit = False)

# fails because 'some string' != 'others'
# NB: name your test directory with 'tests' so as not to collide with inbuilt dirs
# test files and test functions should be prefixed with 'test_'
# test classes should be prefixed with captial "T" eg 'TestClass'
# test directories are like packages and will require the '__init__.py' file

#cmd or powershell
python -m venv pytest # creating a virtual environment named pytest

echo pytest >requirements.txt # write pytest into the requiremts.txt file
pip install -r requirements.txt

cd test_directory
pytest # by calling pytest in the test directory, the test is ran.
# for pytest to run the file, it has to abide by the test naming convention.

# if this is the test file that gets ran, notice that it follows the conventions and has no other thing inside except test functions.
def test_add():
    assert addition.add(4, 5) == 9
def test_sub():
    assert addition.sub(4, 5) == -1

# if there are other statements that aren't test functions, use pytest filename.py to run the test
# use pytest -vvv filename.py to see the entire script when running your code

# Test Classes
class TestStrToInt:
    def setup(self):
        print('\n this is setup')
    def teardown(self):
        print('\nthis is teardown')
    def setup_class(cls):
        print('\nthis is setup class')
    def teardown_class(cls):
        print('\nthis is teardown class')
    def test_rounds_down(self):  # all above are setup. this is the first test
        result = str_to_int('1.99') #str_to_int is the function that converts str to int. I didn't define.
        assert result == 1   
    def test_round_down_lesser(self): # second test.
        result = str_to_int('2.2')
        assert result == 2


# parameterizing test 
# we have a function 'str_to_bool' that converts 'yes', 'y' or '' to True.

#normal method
def test_str_yes():
    result = str_to_bool('yes')
    assert result == True

def test_str_y():
    result = str_to_bool('y')
    assert result == True

    ...

# using parameterization, we use pytest decorator to wrap extra capabilities

@pytest.mark.parametrize('value', ['y', 'yes','']) # making this iterable
def test_is_true(value):
    result = str_to_bool(value)
    assert result is True

# output 'F..' means 1 failure and 2 passing


# seting a debugger to better understand the cmd test output
pytest --pdb  -v test_file.py # on command line. -v is verbosity. you can use -vvv to increase this

# enter 'h' to see what command line functions you have to better explain the failure, use 'l' to list the failure line in code
# to see all the methods available to you, use 'pytest --help'



# fixtures help avoid doing the def setup method by automatically figuring out the setup and avoiding test file path collitions
# remember, all files outputed from command line are saved to a location.
class TestFixtures:
  def test_write_yes(self, tmpdir): # specifying where the test output will be saved to
    path = str(tmpdir.join('test_value')) # joining the test_value str to the path
    write_integer('Yes', path) # this function writes the str 'yes' to the path. The function also uses the 'str_to_bool' function
    with open(path, r) as _f: 
      value = _f.read()
    assert value == 'True'


# Pandas 

# Activating python virtual environment on cmd
cd path\to\your\directory
python -m venv env_name
cd env_name\Scripts
activate

# on powershell
cd path\to\your\directory
python -m venv env_name
cd env_name\Scripts
.\activate.bat #.\ is a powershell read convention

# on bash
cd path\to\your\directory
python -m venv env_name
env_name/bin/activate

# Pandas
# you do not need to download the file from the internet, just pass the url and pandas will read
file_name = 'https://github.com/henrii1/wind-turbine-power-curve-modelling/raw/main/dataset/kelmarsh_02.xlsx'

import pandas as pd
read = pd.read_excel(file_name)
read.head(10)

# Converting the tables to markdown files for teaching etc
!pip install tabulate #required dependency
from pandas.io.clipboard import to_clipboard # i want the converted file to save to clipboard
md = read.to_markdown() #writing to markdown
to_clipboard(md, excel=True) #using 'to_clipboard', i want the file to paste as an excel table


#use queries with pandas
df.query('ratings > 30').head(10) # put all forms of queries into the brace. .head is for display
pab = df.query("region.str.contains('robles', na = False)", engine = 'python') # because string contains functions, you'll have to specify the engine

#changes to string
df['var_short'] = df['variety'].replace({'red wine': 'r', 'white wine': 'w'}) #replace red wine with r and white wine with w, store in var_short

#applying functions in pandas
def good_wine(value):
  if value > 94:
    return True
  return False

df['good'] = df['rating'].apply(good_wine) # Adds a new column called good, if ratings is greater than 94, it appends true.






