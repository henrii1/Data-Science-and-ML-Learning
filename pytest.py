#pytest supports parameterized and fixture-based testing

my_func = _ # function
# using pytest raises: saying we are expecting a particular kind of error
def test_zero_divide():
    with pytest.raises(ZeroDivisionError):
        my_func.divide(10, 0) # dividing 10 by 0 should raise ZeroDivisionError but it won't
    
# we are kind of testing for negative conditions using pytest.raises.
        

"""Class based tests"""

#use the import file.module as file for pytest

class TestCircle:

   #setup method (sets arguments that persists throughout the class)
   def setup_method(self, method):
       print(f"setting up {method}") 
       self.circle = shapes.circle(10)  # 10 is the argument for radius, this will now persist throught out the class


    #teardown method (terminates whatever defined within setup)
   def teardown_method(self, method):
       del self.circle


"""Pytest Fixtures"""

#function
class shape:

    def area(self):
        pass

    def perimeter(self):
        pass

class Rectangle(shape):
    
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def area(self):
        return self.length * self.width
    
    def perimeter(self):
        return (self.length * 2) * (self.width)
    

 #test for class
"""NB: if we defined class based tests, we won't need to define fixtures, well just put fixtures within setup_method"""

#function based tests
@pytest.fixture
def my_rectangle():
    return Rectangle(10, 20)  # this arguments will persist throughout the functions that take my_rectangle as argument


def test_area(my_rectangle):
    rectangle = Rectangle(10, 20)
    assert rectangle.perimeter() == 10 * 20

"""NB: to persist fixtures throughout the test directory, create a conftest.py file and write all your @pytest.fixture function, then add them as function arguments when necessary"""
# we can even pass the parameters as class method arguments.



"""Pytest Marking and parameterizing"""4

import time

@pytest.mark.slow
def test_very_slow():
    time.sleep(10)
    result = my_functions.divie(10,20)
    assert result == 2

#ptest -m slow will only run tests marked slow
    
@pytest.mark.skip(reason="this feature is currently broken") # marked for skip
def skip_test():
    pass

@pytest.mark.xfail(reason="we cannot divide by zero")   # marked to fail
def fail_test():
    pass


#parameterizing

class square(Rectangle):

    def __init__(self, side_length):
        super().__init__(side_length, side_length) # inherits the variables within the init method of inherited class
        super().area()      # inherits the entire method called area. whatever the output of area is, that will be the output.


# trying out multiple values 
        
@pytest.mark.parametrize("side_length, expected_area", [(5, 25), (4, 16)]) # two values
def test_multiple_areas(side_length, expected_area):
    assert shape(side_length).area() == expected_area


"""mocking"""
# isolating the system that we are testing. testing functions without actually calling say a database or API

database = {
    1: "a",
    2: "b"
}

def get_user_from_db(user_id):
    return database.get(user_id)


# mocking test
import unittest.mock as mock

@mock.patch("filename.get_user_from_db")
def test_get_user_from_db(get_user_from_db):
    mock_get_user_from_db.return_value = "Mocked Alice"
    user_name = filename.get_user_from_db(1)

    assert user_name = "Mocked Alice"  # setup a mock value


# using mock for an acutal api (request)
@mock.pach("request_file.get_func")
def test_get_users(mock_get):
    mock_response = mock.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"id": 1, "name": "john"}  # dummy value passed into mock
    mock_get.return_value = mock_response # dummy passed into variable also
    data = file_name.get_func()
    assert data == {"id": 1, "name": "john"} 

#mocks are useful when the return value isn't deterministic
    
#using exception in classes
class Exc(Exception):
    pass
class b(Exc):
  def (self):
    if None:
        print("x")
    else:
        raise Exc


#setup vscode test using comand palette: configure tests python. then select pytest. after that, you can play the tests from the test icon
  