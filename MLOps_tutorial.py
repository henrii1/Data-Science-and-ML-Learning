# install azure cli and enable tab completion

#CLI code
az -- version 

# list all the extensions added
az extension list
# installing the ml extension
az extension add -n ml -y # -n name, ml machine learning, -y yes.

az ml --help # returns a list of the functions that are available in azure ml studio.

az login # helps us login to azure ml from our browser.

az account list -o table # lists all the accounts and subscriptions we have


#installing all azureml dependencies and packages on your cli
cd path\to\directory
python -m venv env_name
cd env_name\Scripts
.\activate.bat   

pip install azureml-core  # installs all the dependencies  


# we can create a compute instance and a workspace in azure ml from the command line. Check Azure documentation.


# using HuggingFace Transformers for tasks
#requirements.txt
ipywidgets==version #required for ipynb
ipykernel==version  #required for ipynb
transformers==version #from hugging face transformers
datasets==version     #from hugging face dataset

#main.py
!pip install -r requirements.txt

from transformers import pipeline  # check hugging face documentary for more.

 # generator = pipeline('predefined_task', model='model_name')
generator = pipeline('text-generation', model'gpt2')
generator("Summarize: input_text") # input your text after the summarize.
generator("question: input_question")

 

# Hugging Face Datasets (using the same requirements.txt file as above)
from datasets import load_dataset, list_datasets

# Explore available datasets
available = list_datasets()
print(len(available))
print([i for i in available if '/' not in i]) # Prints a list of available datasets to choose from

# load the dataset dynamically by passing the name. 
movie_rationales = load_dataset("movie_rationales")
# Select the "train" dataset and then port it to pandas
train = movie_rationales["train"]
df = train.to_pandas()


'''Additional files within an application directory

__init__.py: helps to designate that a directory is a python package
             for instance if there is an app.py file within the directory named 'package' and
             there is a function named 'main', we can access that function using 'package.app.main'
             or from package import __. create one using touch or cat
    
requirements.txt: a file that contains all the dependencies needed. install using pip as 'pip install -r requirements.txt'

setup.py: It is relevant for packaging and distribution projects across environments. helps to preserve functionality
           check below for example script.

.github: Workflows contain actions (CI/CD) and can be created automatically on GitHub or locally through the CLI by writing a .yml script. 
         Workflows define the actions that will be carried out for CI/CD. They work on GitHub for continuous deployment. 
         The deployment environment (container registry for docker image) is also configured within workflows for CD. Workflows define the steps to 
         perform when an action is triggered such as 'push,' is performed.

.vscode: stores customized vscode configuration. it is created automatically when some configurations are changed, it can be created  manually on the CLI.

__pycache__ directory: is a product of python bytecode compilation whenever imports are made. this helps to speed up the process, by checking the cache whenver
                       the same operation is to be carried out again.

Dockerfile: contains the set of instructions to build a docker image. a docker image (converted from the code directory) is a lightweight package that contains 
            everything needed to run a software, including code, runtime, dependencies etc. it essentially convert the code dir into a package. called containerization.
            below is a sample Dockerfile

.gitattribute: helps track large files. It is automatically created when cloning from huggingface. Just use git add .gitattributes to include before pushing back to space.

Test Directory: create an app directory for application, tests directory for tests and other dependencies.
'''


'''Using setup.py for packaging and distributing projects'''
from setuptools import setup, find_packages

# Read the dependencies from requirements.txt
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='your_project_name',
    version='0.1',
    packages=find_packages(),
    install_requires=requirements, # we could also load in as install_requires = ['gradio', 'pytorch==3.3']
    entry_points={
        'console_scripts': [
            'your_script_name = your_package.module:main_function', # Jformat = jformat.main:main (jformat.py is the file name, we defined the main function within)
        ],
    },
    # Other metadata such as author, description, license, etc.
)


# after activating your virtual environment and going into the directory

python setup.py develop # it will also install all the dependencies.



'''an __init__.py file is used to convert a directory to a package and can be empty. below is a sample code'''

# This can be an empty file for simple packages

# You might include package-level initialization code here
print("Initializing the package!")

# Define variables or constants that should be available to the package's modules
PACKAGE_NAME = "my_package"
VERSION = "1.0"


'''.gitignore file: create to ignore tracking some directories'''
touch .gitignore
# Type text of things not to track. find a detailed .gitignore file with alfredodeza


'''creating a sample Dockerfile'''
touch Dockerfile #creates the file. then within, enter what is below

# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the application files to the container
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "app.py"]

'''CMD part for docker'''
docker build -t your-image-name # building the docker image

docker run -p 4000:80 your-image-name #run the docker image locally for testing it (this will provide a url you can checkout). or deploy to cloud (serverless)
# deploying can be on a server. serverless methods utilize amazon ecs, google kubernetes engine, microsorf azure contaner instance. one of the ffg.

'''IF YOU ARE using CD DEPLOYING USING GITHUB ACTIONS, HERE ARE THE STEPS AFTER CREATING YOUR DOCKER FILE'''
docker build -t your-image-name  # build the docker image

# Tag your image with the repository url. if it is docker hub, add your username also
docker tag your-image-name username/your-image-name 

# Push the docker image to the container registry like docker hub.
docker push username/your-image-name

# deploy the docker image in the registry to you serverless cloud. process differs depending on the cloud service

# Define within github workflows to build the docker image and push to container registry whenever there is an update. push entire code to hub also
# (eg)
name: Deploy to Docker Hub

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v2

      - name: Set up Docker
        uses: actions/setup-docker@v2

      - name: Build and Push Docker Image
        run: |
          docker build -t username/your-image-name .
          docker tag username/your-image-name username/your-image-name:latest
          docker push username/your-image-name:latest
        env:
          DOCKER_USERNAME: ${{ secrets.DOCKER_USERNAME }} # use secrets to hide sensitive info
          DOCKER_PASSWORD: ${{ secrets.DOCKER_PASSWORD }}

# with this, anytime a change is made to the code as specified in workflow, the registry is updated 
# and it reflects on the deployed software because the software points to the register.


'''Typical structure of an application directory'''

myapp/
|-- app/
|   |-- __init__.py
|   |-- module1.py
|   |-- module2.py
|   |-- ...
|-- tests/
|   |-- __init__.py
|   |-- test_module1.py
|   |-- test_module2.py
|   |-- ...
|-- requirements.txt
|-- Dockerfile
|-- .gitignore
|-- .github/
|   |-- workflows/
|       |-- your-ci-cd-workflow.yml
|-- .vscode/
|   |-- settings.json
|-- setup.py
|-- ...


# FastAPI and Flask are frameworks that help you package models with interractive UI's
# You can use them to link html pages and models. They define the data transfer logic.

on CLI we run the app. python app.py. # output listens on port ---







