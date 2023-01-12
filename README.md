# Django-BankingApp-Deployment
Deploying the Python banking application on Docker containers using a CI/CD pipeline

------------
#### Deploy Application with Docker:

To create an image from a **Dockerfile**, use the following command: 

`docker build -t bankingapp-image .`

Command to verify the Docker images:

`docker image ls`

Create a container for the banking application by executing the below command:

`docker run --name bankingapp-container -d -p 8000:8000 bankingapp-image`

Command to verify the Docker containers:

`docker container ls`

 Cmmand to list the running containers:
 
` docker ps`

The application should be running at the following URL:

**http://localhost:8000/bankingadmin** : Admin Module

**http://localhost:8000/bankinguser/** : End-user Module


------------

#### Deploy Application with Jenkins CI/CD Pipeline:

Install the following plugins on Jenkins:
1. Python
2. Pyenv Pipeline

Execute the below command on the terminal window to access Docker in Jenkins and restart the lab instance:

`sudo usermod -a -G docker jenkins `
 
 
> **Note:** Please update the Python virtual environment path as per your system location while deploying the app locally without Docker; otherwise, the pipeline will fail.

Before running the pipeline with updated steps for Docker, make sure to check if any Docker images or containers exist. You can use the below command to delete all images and containers:

To kill all the active Docker containers:

`sudo docker stop $(sudo docker ps -a -q)`

To delete all images:

`sudo docker rm $(sudo docker ps -aq)`

Your CI/CD pipeline should complete all stages successfully, and the banking application should be available at **http://localhost:8000**.






