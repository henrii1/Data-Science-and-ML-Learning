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


# Infrastructure as code: Makefile, github actions, Dockerfile.
#cloud environment: AWS cloud9, github codespaces
# using codespace
# setup codespace from the code part of github

# setup virtual env
which virtualenv
virtualenv ~/.venv
source ~/.venv/bin/activate
which python

# persist the virtual environment even after loading a new terminal
vim ~/.bashrc
# at the bottom of the file enter the following
source ~/.venv/bin/activate # then close vim  ':wq!"

pip freeze | less        # used to see all the installed packages.
#files to create
Makefile
requirements.txt

#makefiles are simple text files that execute unix-like commands, they define dependencies among components, very similar to a dockerfile
install:
      pip install --upgrade pip  &&\
          pip install -r requirements.txt

test:
        python -m pytest -vv test_hello.py

format: 
        black *.py

lint:
        pylint --disable=R,C hello.py        # disable error levels less than warning (there are two less by default represented by R,C)

all: install lint test format

# Does formatting and installation: Cli code
make install, make format, make test, make lint, make all (does everything). # these are the steps we defined. They are the usual steps for software dev.
# for instance we would have done pip install -r requirements.txt, but we did make install.
# pylint is a linting tool, black is for formatting.

# for codespace most times install ipython so that you can interract with the terminal like you would on vscode
# Noah Gift, Alex Odeza

# cloud environments are important because they give you an environment that will be similar to that of deployment


#Noah gift

#linting, testing and formatting actions: %pytest (wildcard)
#hugging face text summarization model used with gradio and deployed to huggingface spaces. CI was set to huggingface too: hugging-face-demo, huggingface(notice the extra thing added to the readme)
# FastAPI app deployed to amazon : FastAPI

# 3 most important files: Dockerfile, Makefile, requirements.txt
# greedy algorithm and traveling salesman problem: heuristics

#devcontainer config: stores codespace configurations. right click extensions and add to .devcontainer
nvidia-smi    # shows gpu info 
htop          # show codespace storage info

#git copilot labs extension is used to translate code from one language to another

#making your python files directly executable
#!/user/bin/env python   # write this within the file. the first line. hash included

#cli scripts
chmod +x filename.py

#run
./filename.py

#using the click module to build command line script(tool): devops-skills-with-github

# NB: sdks are platforms where you can build, train and deploy your ml models such as azure machine learning and amazon sagemaker
# NB: specific services for serverless computing are Azure Functions and Amazon Lambda.

# Basic workflow with Amazon ECR and ECS:
#> create code and test using cloud env like codespace and create the docker image(github actions) and pus to Amazon Elastic Container Repo
#> then link to Amazon Elastic Container Service (configure properly for deployment). then deploy the service.

#AWS lambda functions: we create them like normal functions, we just need to select the language and write the function
# Step functions are used to combine multiple lambda functions together.

#setting up and using azure databricks: Noah Gift: databricks repo---databricks is used for analysing data for data science and ML

# AWS Glue is used to consolidate multiple data sources together.
# NB: A JOB refers to the execution of a specific task, workloads are a specific set of tasks or activities that needs to be performed by a system

#linting code after writing helps us identify all errors and logs before we run them. linting checks the syntax, test files test the logic.
# files: Makefile (they only work on unix, which is why u should use cloud dev environments like codespace), test.py (test logic), requirements.txt, Dockerfile.
# Click module is used for creating command line tools. take an example from Noah Gift or from the click documentary. fire library is the easiest  way to create a command line tool.
# indentation problems are fixed with 'black' the formatting tool. it is a very nice idea to use makefiles.

#for ECR, the dockerfile should be 'FROM public.ecr.aws/lambda/python3.8' 


'''Deploying a microservice from scratch with AWS'''  #From-Zero-To-Deploy    Noah Gift
#create requirements.txt, Makefile, test, Dockerfile, etc
#write code and push to github
# setup codespace, use it to lint, format and test code (u can write all the code here too--consider copilot)
# clone code to Amazon cloud 9  (you can write all the code here too)
# create an Amazon ECR repository, create docker image and push to the repo. use Amazon code build to continuously push the latest version of your code to ECR. use amazon lambda repository for bigger images
# use Amazon App Runner to deploy as a microservice. (You'll be able to see the routes and can check out response and all from the swagger docs)

#NB: the predict function is set as a route, then some code is added to it to facilitate it, check Noah Gift repos(Form-zero-to-deploy, mastering functions)
#NB: check the python version in your environment to set docker and github actions.

#'command palete' enter configure dev container features and select github codespace configuration.
import ipdb; ipdb.set_

# repos: devops-skills-with-github, Function from zero
# Bash APIs can be developed to test out soe models using AWS cloud.


'''Course 3: MLOps Platfroms'''

#Amazon Sagemaker studio lab: something like google colab, it also offers a shell.
nvidia-smi -l1     # shows gpu configurations

#Aws Cloud Shell: a command line that is integrated inside the AWS ecosystem
#> you can change the shell environment to bash, powershell etc. To work with files, you'll have to upload them.
#> There is a way to upload multiple files. you can download files as well. There is also AWS cloud9 (like vscode)

# on Aws cloud shell: 
aws comprehend help   #shows all the ml services that it can perform by default.
aws text-detection help # shows all the methods associated with text-detection

# Cloud9: resource like vscode
aws s3 ls   # list all the service buckets you have

#AWS has a lot of storage mediums for any kind of data, and any kind of job

# Amazon s3: (Simple Storage System)
#> a fundamental storage container that stores objects (text, videoes etc). It is like a top level folder or directory in which we store data
#> important and attempts to correctly manage buckets for all the various Amazon services.
aws s3 cp help  # provides commands for copying from shell or cloud9 to a bucket.

# you can query s3 files with SQL

#Working with Batch and stream data
#STREAM: Kinesis, Amazon MSK Kafika
#BATCH: AWS Glue, AWS Batch AWS Step Functions

#AWS batch is used to partition the GPU for the amount of jobs it can do per time. it also does general batching
#AWS Glue: a serverless (Extract Transform Load) ETL system. you can point it to multiple datasources for it to consolidate or integrate. then store in a bucket in s3
#AWS Athena: is used to query data available in the amazon ecosystem. SQL queries.
#EMR Studio: creates a flexible environment where u can set how many gpus, and clusters to run your notebooks, depending on the job.

#Sagemaker has a robust documentation of the algorithms available within and their uses. It purports to abstract the native code-wise model building process by automation

#AutoML is a tool that helps with choosing the right machine learning model for a task as well as the hyperparameters.

#Amazon Sagemaker Canvas: import data from local or s3 bucket, it provides visualization icons like excel, you could also type in formulas, without coding.
#>select the data and click build a model. it scans and automatically selects a model to build with, u can see the metrics for each.

#AWS EC2 (Elastic compute cloud): is a service that provides resizable compute capacity in the cloud for running virtual environments

#ECS and App Runner both deploy but ECS if for only containerized applications and utilizes EC2. App runner is for ease of use, for both containerized and non-containerized applications.
#> you won't also need to worry about setting up much IAC for managing compute and clusters.

#For ECR and App runner, running fastAPI apps, check vid "Running Pytorch with Aws App: course 3.4"




