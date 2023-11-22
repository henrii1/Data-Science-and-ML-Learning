# requirement.txt

fastapi
uvicorn[standard]
pydantic[email]
python-multipart
python-jose[cryptography]
passlib[bcrypt]
SQLAlchemy

# Mainfile: main.py

from datetime import datetime, time, timedelta
from enum import Enum
import time
from typing import Literal, Union
from uuid import UUID

from fastapi import (
    Body,
    Depends,
    FastAPI,
    Query,
    Path,
    Cookie,
    Header,
    status,
    Form,
    File,
    UploadFile,
    HTTPException,
    Request,
    BackgroundTasks,
)
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field, HttpUrl, EmailStr
from passlib.context import CryptContext
from jose import jwt, JWTError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import HTMLResponse

app = FastAPI()

@app.get("/")
async def get():
    return {"message": "hello world"}

'''
on the command line enter 'uvicorn main:app'  main==filename, app==fastapi instance.
other alternatives 'uvicorn main:app --reload' == helps when you make changes and want to see them
alternative 2" 'uvicron main:app --port=9000' == assigning a port. without this, it defaults to 8000

'localhost:8000/docs': an interractive interface created by fastapi one can assess each route command
'''
@app.post("/")
async def post():
    return {"message": 'hello from the post route'}

@app.put("/")
async def put():
    return {"message": 'hello from the put route'}

@app.get("/items")
async def list_items():
    return {"message": 'list items route'}    # the ./items url should work too

@app.get("/items/{item_id}")
async def get_items(item_id: int):
    return {"item_id": item_id}     # the ./items/5 should work, prints 'item_id: 5' other data type won't


# Type of route commands
@app.get("/items/{item_id}")  # Retrieve data
@app.post("/items/")            # creates new data
@app.put("/items/{item_id}")    #updates existing data
@app.delete("/items/{item_id}") #delete existing data
@app.options("/items/")         #describes a communication
@app.head("/items/")            #Retrive head without the body
@app.patch("/items/{item_id}")  #partially update existing data
@app.copy("/items/{item_id}")   #copy a resource to a new location
@app.link("/items/{item_id}")   #establish linkes between resources
@app.unlink("/items/{item_id}") #remove links between resources


# using specific types
from enum import Enum

class FoodEnum(str, Enum):
    fruits = 'fruits'
    vegetables = 'vegetables'
    diary = 'dairy'

@app.get("/foods/{food_name}")
async def get_food(food_name: FoodEnum):
    if food_name == FoodEnum.vegetables:
        return {"food_name": food_name, "message": "you are healthy"}

    if food_name.value == "fruits":
        return {
            "food_name": food_name,
            "message": "you are still healthy, but like sweet things",
        }
    return {"food_name": food_name, "message": "i like chocolate milk"}


# on the browser, localhost:8000/foods/{food_name} or localhost:8000/foods/docs

# if food_name is either fruits, vegetable or diary, the message under will print. in docs, it will be interractive.
# sample message 'food_name': vegetable, "message": 'you are healthy'


'''Querying Parameters'''   # they are not defined in the get, only in the function. Path parameters are defined in both

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/items")     
async def list_items(skip: int = 0, limit: int = 10):       # variables are only passed in here
    return fake_items_db[skip : skip + limit]  #localhost:8000/items?skip=2, or localhost:8000/items?limit=1   [skip: skip + limit] is indexing


@app.get("/items/{item_id}")  # path parameter is passed here. query parameters are also passed in inside function get_item
async def get_item(
    item_id: str, sample_query_param: str, q: str | None = None, short: bool = False   #str | None=None is a hint type. read as str or None but default is None. 
):
    item = {"item_id": item_id, "sample_query_param": sample_query_param}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {
                "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut consectetur."
            }
        )
    return item   # localhost:8000/items/food?q=world&short=1    path parameters are typed with slash, while the query ones use (? and &)
                    # the answer will be ('item:food, q: world, description:"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut consectetur.")
                    # NB: short=no, short=True, short=false will work


@app.get("/users/{user_id}/items/{item_id}")    # passing multiple path parameters
async def get_user_item(
    user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {
                "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut consectetur."
            }
        )
        return item
    


'''Request_Body'''

class Item(BaseModel):  # BaseModel was imported from pydantic. 'from pydantic import BaseModel'
    name: str           #NB: pydantic models do not require the self.name. they are automatically inferred.
    description: str | None = None
    price: float
    tax: float | None = None


@app.post("/items")      #post request sends data. the data isn't included in the url like the get.
                         # url stays same 'localhost:8000/items' items are within the class object.
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


@app.put("/items/{item_id}")    #put request makes updates or requests data(as get) if data doesn't exist in that path. it can take in parameters and
                                #it can also update request updates to the request body. (i.e): 'localhost:8000/items/food' food is a path parameter, q is a query parameter, Items is a class object.
                                # if we don't set our query parameters to none 'q:str | None = None' they'll be required.
async def create_item_with_put(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result

'''query Parameters string'''  # to go to a method definition (the class definition) in vscode, right click the method or press F12, press ALT + F12 for documentation

@app.get("/items")
async def read_items(
    q: str               # for multiple values 'q: list[str]' signifying that q is a list of strings.
    | None = Query(      # Query function is imported from FastAPI, it is used for data validation. do not enter values less than 3 or greater than 10, check docs for more
        None,            # to define query without a default value (None in our case) use '...'. i.e: q: str = Query(..., min_length=)
        min_length=3,
        max_length=10,
        title="Sample query string",
        description="This is a sample query string.",
        alias="item-query",         #sets the new name of q, url will be 'localhost:8000/items?item-query=food' we don't use item-query above directly because python doesnt work well with '-'
    )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/items_hidden")
async def hidden_query_route(
    hidden_query: str | None = Query(None, include_in_schema=False)
):
    if hidden_query:
        return {"hidden_query": hidden_query}
    return {"hidden_query": "Not found"}


'''Path Parameters Numeric'''

@app.get("/items_validation/{item_id}")
async def read_items_validation(
    *,                                                                            #generally we can't have positional arguments after keyword arguments. but if we use the '*' for unpacking positional
                                                                                  # argument, python assumes all the arguments afterwards are keyword arguments. regardless of if it isn't
    item_id: int = Path(..., title="The ID of the item to get", gt=10, le=100),   # Path works similar to query but for path parameters. 'from FastAPI import Path'
    q: str = "hello",
    size: float = Query(..., gt=0, lt=7.75)
):
    results = {"item_id": item_id, "size": size}
    if q:
        results.update({"q": q})
    return results


'''Body Fields'''

class Item(BaseModel):
    name: str
    description: str | None = Field(                              #'Field' works like Query or Path but it is imported from 'pydantic'
        None, title="The description of the item", max_length=300
    )
    price: float = Field(..., gt=0, description="The price must be greater than zero.") # 'ge' = greater than or equal to, 'le' is same
    tax: float | None = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item = Body(..., embed=True)):   #Body is imported from FastAPI. normally, we'll have to use class __(BaseModel) to set a request body parameter.
    results = {"item_id": item_id, "item": item}                           #Alternatively, we could use 'Body' to set it.
    return results



'''Nested Models'''

class Image(BaseModel):
    url: HttpUrl                             # HttpUrl is imported from pydantic. the value entered must be a url otherwise it will raise an error
    name: str


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = []
    image: list[Image] | None = None


class Offer(BaseModel):
    name: str
    description: str | None = None
    price: float
    items: list[Item]


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results


@app.post("/offers")
async def create_offer(offer: Offer = Body(..., embed=True)):
    return offer


@app.post("/images/multiple")
async def create_multiple_images(images: list[Image]):
    return images


@app.post("/blah")
async def create_some_blahs(blahs: dict[int, float]):      # 'dict[int, float]' says key and value should be int and float respectively
    return blahs

'''Declare Request'''

class Item(BaseModel):
    name: str                                              # using the 'Field' module from pydantic will look like name: str = Field(..., example ='food', description = 'what i want')
    description: str | None = None
    price: float
    tax: float | None = None

    # class Config:                                         # using 'class Config' we can set the default values of our request body. another way is to use 'Field' module from pydantic                                       
    #     schema_extra = {                                  
    #         "example": {
    #             "name": "Foo",
    #             "description": "A very nice Item",
    #             "price": 16.25,
    #             "tax": 1.67,
    #         }
    #     }


@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Item = Body(               # using Body on the class object is another way to define the response body
        ...,
        examples={                   # examples gives the option of displaying either of the main keys in the dictionary
            "normal": {              # each key must be entered as 'summary, description and value'. Only the value shows in code window others qualify the value.
                "summary": "A normal example",
                "description": "A __normal__ item works _correctly_",
                "value": {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 16.25,
                    "tax": 1.67,
                },
            },
            "converted": {
                "summary": "An example with converted data",
                "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
                "value": {"name": "Bar", "price": "16.25"},
            },
            "invalid": {
                "summary": "Invalid data is rejected with an error",
                "description": "Hello youtubers",
                "value": {"name": "Baz", "price": "sixteen point two five"},
            },
        },
    ),
):
    results = {"item_id": item_id, "item": item}
    return results

'''Extra Data Type'''

@app.put("/items/{item_id}")
async def read_items(
    item_id: UUID,                              # unique user identifier 'from uuid import UUID'
    start_date: datetime | None = Body(None),
    end_date: datetime | None = Body(None),        # 'from datetime import datetime, time, timedelta'
    repeat_at: time | None = Body(None),
    process_after: timedelta | None = Body(None),
):
    start_process = start_date + process_after
    duration = end_date - start_process
    return {
        "item_id": item_id,
        "start_date": start_date,                 
        "end_date": end_date,
        "repeat_at": repeat_at,
        "process_after": process_after,
        "start_process": start_process,
        "duration": duration,
    }

# on cli to get uuid to input, see the python code below
from uuid import uuid4
uuid4()
# output is a unique value that can be used as uuid


'''Cookie and Header Parameters'''

# in HTTP, headers are metadata that provide additional info about the message
# cookies are small info that server passes to our browser and back, to track sessions.

@app.get("/items")
async def read_items(
    cookie_id: str | None = Cookie(None),
    accept_encoding: str | None = Header(None),
    sec_ch_ua: str | None = Header(None),
    user_agent: str | None = Header(None),
    x_token: list[str] | None = Header(None),
):
    return {
        "cookie_id": cookie_id,
        "Accept-Encoding": accept_encoding,
        "sec-ch-ua": sec_ch_ua,
        "User-Agent": user_agent,
        "X-Token values": x_token,
    }

'''Response Model'''

# pydantic[email] was added to our requirements.txt    EmailStr was imported from pydantic (Email: EmailStr)--a class attribute or parameter
# 'response_model' helps us get more description in the response body

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float = 10.5
    tags: list[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=True)  # all unassigned variables shouldn't show in output
async def read_item(item_id: Literal["foo", "bar", "baz"]):
    return items[item_id]


@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    return item


class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class UserIn(UserBase):                       # this is typically how to hide passwords.
    password: str


class UserOut(UserBase):
    pass


@app.post("/user/", response_model=UserOut)   #UserOut inherited the UserBase hence the response model won't display password
async def create_user(user: UserIn):
    return user


@app.get(
    "/items/{item_id}/name",
    response_model=Item,
    response_model_include={"name", "description"},       # only those included will show in output
)
async def read_item_name(item_id: Literal["foo", "bar", "baz"]):          #'from typing import Literal' helps to valate that only our permitted value is used (foo, bar, baz)
    return items[item_id]


@app.get("/items/{item_id}/public", response_model=Item, response_model_exclude={"tax"})    #those excluded won't show even when assigned.
async def read_items_public_data(item_id: Literal["foo", "bar", "baz"]):
    return items[item_id]

'''Extra Models'''

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    pass


class UserInDB(UserBase):
    hashed_password: str


def fake_password_hasher(raw_password: str):
    return f"supersecret{raw_password}"


def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print("User 'saved'.")
    return user_in_db


@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved


class BaseItem(BaseModel):
    description: str
    type: str


class CarItem(BaseItem):
    type = "car"


class PlaneItem(BaseItem):
    type = "plane"
    size: int


items = {
    "item1": {"description": "All my friends drive a low rider", "type": "car"},
    "item2": {
        "description": "Music is my aeroplane, it's my aeroplane",
        "type": "plane",
        "size": 5,
    },
}


@app.get("/items/{item_id}", response_model=Union[PlaneItem, CarItem])         # 'from typing import Union'
async def read_item(item_id: Literal["item1", "item2"]):
    return items[item_id]


class ListItem(BaseModel):
    name: str
    description: str


list_items = [
    {"name": "Foo", "description": "There comes my hero"},
    {"name": "Red", "description": "It's my aeroplane"},
]


@app.get("/list_items/", response_model=list[ListItem])           #passing in the variable as the route. 'list_items'
async def read_items():
    return items


@app.get("/arbitrary", response_model=dict[str, float])
async def get_arbitrary():
    return {"foo": 1, "bar": "2"}


'''Response Status'''

@app.post("/items/", status_code=status.HTTP_201_CREATED)  #status is imported from FastAPI, learn more about response code from HTTP documentation
async def create_item(name: str):
    return {"name": name}


@app.delete("/items/{pk}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(pk: str):
    print("pk", pk)
    return pk


@app.get("/items/", status_code=status.HTTP_302_FOUND)
async def read_items_redirect():
    return {"hello": "world"}

'''Form field'''

@app.post("/login/")
async def login(username: str = Form(...), password: str = Body(...)):      #Forms is imported from FastAPI, fields make our respons body like json, while forms make it like an excel cell.
    print("password", password)
    return {"username": username}


@app.post("/login-json/")
async def login_json(username: str = Body(...), password: str = Body(...)):
    print("password", password)
    return {"username": username}

'''Request Files'''
@app.post("/files/")
async def create_file(
    files: list[bytes] = File(..., description="A file read as bytes")        # bytes objects make it such that we can upload a file, 'File' and 'UploadFile' are imported from FastAPI
):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfile/")
async def create_upload_file(
    files: list[UploadFile] = File(..., description="A file read as UploadFile")     # 'UploadFile' also makes it possible to upload a file this is better because it can work with multiple file types
):                                                                                   # 'await file.read()' reads the content of the file.
    return {"filename": [file.filename for file in files]}


@app.get("/")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)


'''Request Forms and Files'''

@app.post("/files/")
async def create_file(
    file: bytes = File(...),
    fileb: UploadFile = File(...),
    token: str = Form(...),
    hello: str = Body(...),
):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
        "hello": hello,
    }

'''Handling Errors'''

items = {"foo": "The Foo Wrestlers"}


@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(                   # 'HTTPException' is imported from FastAPI
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "There goes my error"},
        )
    return {"item": items[item_id]}


class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name


@app.exception_handler(UnicornException)                                           # exception_handler is another kind of request for raising exceptions
async def unicorn_exception_handler(request: Request, exc: UnicornException):      # Request is installed from FastAPI, 
    return JSONResponse(                                                           # JSONResponse is installed from FastAPI.responses
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )


@app.get("/unicorns/{name}")
async def read_unicorns(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}


# @app.exception_handler(RequestValidationError)               # imported 'from FastAPI.exceptions import RequestValidationError'
# async def validation_exception_handler(request, exc):
#     return PlainTextResponse(str(exc), status_code=400)
#
#
# @app.exception_handler(StarletteHTTPException)               #HTTPException can also be imported from starlette, we just used an alias
# async def http_exception_handler(request, exc):
#     return PlainTextResponse(str(exc.detail), status_code=exc.status_code)
#
#
# @app.get("/validation_items/{item_id}")
# async def read_validation_items(item_id: int):
#     if item_id == 3:
#         raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
#     return {"item_id": item_id}


# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request: Request, exc: RequestValidationError):
#     return JSONResponse(
#         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#         content=jsonable_encoder({"detail": exc.errors(), "blahblah": exc.body}),           # from FastAPI.encoders import 'jsonable_encoder'
#     )
#
#
# class Item(BaseModel):
#     title: str
#     size: int
#
#
# @app.post("/items/")
# async def create_item(item: Item):
#     return item

@app.exception_handler(StarletteHTTPException)                  # HTTPException is imported from FastAPI, by hovering a module, vscode will tell what package to import if from.
async def custom_http_exception_handler(request, exc):
    print(f"OMG! An HTTP error!: {repr(exc)}")
    return await http_exception_handler(request, exc)           # from FastAPI.exception_handler import 'http_exception_handler'


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print(f"OMG! The client sent invalid data!: {exc}")
    return await request_validation_exception_handler(request, exc)   # from FastAPI.exception_handler import 'request_validation_exception_handler'


@app.get("/blah_items/{item_id}")
async def read_items(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return {"item_id": item_id}

'''Path Operation Configuration'''

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()


class Tags(Enum):
    items = "items"
    users = "users"


@app.post(
    "/items/",
    response_model=Item,
    status_code=status.HTTP_201_CREATED,                  # we can also put the response_model, status_code in the decorator
    tags=[Tags.items],
    summary="Create an Item-type item",                   # 'tags' helps with organization for the docs
    # description="Create an item with all the information: "
    # "name; description; price; tax; and a set of "
    # "unique tags",
    response_description="The created item",
)
async def create_item(item: Item):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return item


@app.get("/items/", tags=[Tags.items])
async def read_items():
    return [{"name": "Foo", "price": 42}]


@app.get("/users/", tags=[Tags.users])
async def read_users():
    return [{"username": "PhoebeBuffay"}]


@app.get("/elements/", tags=[Tags.items], deprecated=True)
async def read_elements():
    return [{"item_id": "Foo"}]


'''JSON Compactible Encoder'''

class Item(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    tax: float = 10.5
    tags: list[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {
        "name": "Bar",
        "description": "The bartenders",
        "price": 62,
        "tax": 20.2,
    },
    "baz": {
        "name": "Baz",
        "description": None,
        "price": 50.2,
        "tax": 10.5,
        "tags": [],
    },
}


@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):
    return items.get(item_id)


@app.put("/items/{item_id}", response_model=Item)                 # put request replaces data
def update_item(item_id: str, item: Item):
    update_item_encoded = jsonable_encoder(item)
    items[item_id] = update_item_encoded
    return update_item_encoded


@app.patch("/items/{item_id}", response_model=Item)               # patch request partially modifies the data
def patch_item(item_id: str, item: Item):
    stored_item_data = items.get(item_id)
    if stored_item_data is not None:
        stored_item_model = Item(**stored_item_data)
    else:
        stored_item_model = Item()
    update_data = item.dict(exclude_unset=True)                   # exclude_unset doesn't show those values not reset or replaced.
    updated_item = stored_item_model.copy(update=update_data)
    items[item_id] = jsonable_encoder(updated_item)
    return updated_item

'''Dependencies Intro'''

async def hello():
    return "world"


async def common_parameters(
    q: str | None = None, skip: int = 0, limit: int = 100, blah: str = Depends(hello)
):
    return {"q": q, "skip": skip, "limit": limit, "hello": blah}


@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):     # 'Depend' is imported from FastAPI.  this is used to link variables to multiple request statements.
    return commons


@app.get("/users/")
async def read_users(commons: dict = Depends(common_parameters)):
    return commons

'''Classes As Dependencies'''

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit


@app.get("/items/{item_id}")
async def read_items(commons: CommonQueryParams = Depends()):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db[commons.skip : commons.skip + commons.limit]
    response.update({"items": items})
    return response

'''Sub-Dependencies'''

def query_extractor(q: str | None = None):
    return q


def query_or_body_extractor(
    q: str = Depends(query_extractor), last_query: str | None = Body(None)
):
    if q:
        return q
    return last_query


@app.post("/item")
async def try_query(query_or_body: str = Depends(query_or_body_extractor)):
    return {"q_or_body": query_or_body}


'''Dependencies in Path operation decorators'''

async def verify_token(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: str = Header(...)):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key


# app = FastAPI(dependencies=[Depends(verify_token), Depends(verify_key)])      # another way to define a dependency whose values we do not need.


@app.get("/items/", dependencies=[Depends(verify_token), Depends(verify_key)])  # Define a dependency in the decorator if you don't need their values within the function.
async def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]


@app.get("/users/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]


'''Security, First Steps'''

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")         # 'from FastAPI.security import OAuth2PasswordBearer' creates a login that is required before status_code == 200 (as a form)

fake_users_db = {
    "johndoe": dict(
        username="johndoe",
        full_name="John Doe",
        email="johndoe@example.com",
        hashed_password="fakehashedsecret",
        disabled=False,
    ),
    "alice": dict(
        username="alice",
        full_name="Alice Wonderson",
        email="alice@example.com",
        hashed_password="fakehashedsecret2",
        disabled=True,
    ),
}


def fake_hash_password(password: str):
    return f"fakehashed{password}"


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    return get_user(fake_users_db, token)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):                            # 'from FastAPI.security import OAuth2PasswordRequestForm' this retrieves the data entered into form
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)                                  # 'form_data.password' is the password retrieved from the authorization form
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def get_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}


'''Security, OAuth2 Beearer and JWT'''    #jwt is json web token, it is a hash identifier.

#installed dependencies: python-jose[cryptography], paslib[bcrypt]

from passlib.context import CryptContext               # Importation.
from jose import jwt, JWTError

SECRET_KEY = "thequickbrownfoxjumpedoverthelazydog"                      # should be done using 'openSSH'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$tJD64mRe0bd/UNdAANZtvuOnWDKScbVtXA9lB6X7arZxJQbAyMbd2",
        "disabled": False,
    }
}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive User")
    return current_user


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/users/me/items")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]


'''Middleware and CORS'''

#importation: from starlette.middleware.base import BaseHTTPMiddleware
# importation: from fastapi.middleware.cors import CORSMiddleware


# create a basic fastapi frontend app
# from terminal

npm init svelte fast-api-frontend
# choose skeleton project. u can choose demo app too.
# choose no for the option of typescript.
cd fast-api-frontend
npm install

# use 'npm run dev' to run the svelte frontend.



# https://github.com/jvp-design/fastapi-tutorial/tree/30-bigger_applications_multiple_files/fast-api-frontend
# frontend-api-directory was introduced.


class MyMiddleware(BaseHTTPMiddleware):                                #adds extra functionality to routes. in this case we are adding 'x-process-time'(time taken to process) to response body
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response


origins = ["http://localhost:8000", "http://localhost:3000"]
app.add_middleware(MyMiddleware)
app.add_middleware(CORSMiddleware, allow_origins=origins)

@app.get("/blah")
async def blah():
    return {"hello": "world"}


'''SQL Databases'''

# A directory is created for sql databases, it also contains __init__.py, signifying a package
# https://github.com/jvp-design/fastapi-tutorial/tree/30-bigger_applications_multiple_files/sql_app

!pip install SQLAlchemy
#file1: crud.py                                                         # helps in creating a query object.

from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

#file2: Database.py                                      #initialization of a sqllite database

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)      

Base = declarative_base()

#file3:main.py

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas                              # use '.' to import files (modules) from the previous directory
from .database import SessionLocal, engine                       # . database refers to the database.py module

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User, status_code=201)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item, status_code=201)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db, item=item, user_id=user_id)


@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items
 
#File4: model.py                                                # defining the tables, columns and relationship

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")                      #relationship to item table


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")                      # relationship to user table


#file5: schemas.py                                                          # creating the schema, config and login

from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []

    class Config:
        orm_mode = True




'''Bigger Application, multifiles'''

# https://github.com/jvp-design/fastapi-tutorial/tree/30-bigger_applications_multiple_files/sub_app

# this directory introduced multiple files. 


'''Background Tasks'''

import time


def write_notification(email: str, message=""):
   with open("log.txt", mode="w") as email_file:
         content = f"notification for {email}: {message}"
         time.sleep(5)
         email_file.write(content)


@app.post("/send-notification/{email}", status_code=202)
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}


def write_log(message: str):
    with open("log.txt", mode="a") as log:
        log.write(message)


def get_query(background_tasks: BackgroundTasks, q: str | None = None):
    if q:
        message = f"found query: {q}\n"
        background_tasks.add_task(write_log, message)
    return q


@app.post("/send-notification/{email}")
async def send_notification(
    email: str, background_tasks: BackgroundTasks, q: str = Depends(get_query)
):
    message = f"message to {email}\n"
    background_tasks.add_task(write_log, message)
    return {"message": "Message sent", "query": q}


'''Metadata and Docs URLs'''

from FastAPI.staticfiles import StaticFiles

description = """
ChimichangApp API helps you do awesome stuff. 🚀

## Items

You can **read items**.

## Users

You will be able to:

* **Create users** (_not implemented_).
* **Read users** (_not implemented_).
"""

tags_metadata = [
    dict(
        name="users",
        description="Operations with users. The **login** logic is also here.",
    ),
    dict(
        name="items",
        description="Manage items. So _fancy_ they have their own docs.",
        externalDocs=dict(
            description="Items external docs", url="https://www.jvp.design"
        ),
    ),
]


app = FastAPI(
    title="ChimichangApp",
    description=description,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact=dict(
        name="Deadpoolio the Amazing",
        url="http://x-force.example.com/contact",
        email="dp@x-force.example.com",
    ),
    license_info=dict(
        name="Apache 2.0", url="https://www.apache.org/licenses/LICENSE-2.0.html"
    ),
    openapi_tags=tags_metadata,
    openapi_url="/api/v1/openapi.json",
    docs_url="/hello-world",
    redoc_url=None,
)


@app.get("/users", tags=["users"])
async def get_users():
    return [dict(name="Harry"), dict(name="Ron")]


@app.get("/items/", tags=["items"])
async def read_items():
    return [dict(name="wand"), dict(name="flying broom")]

