# WorksOnMyMachine

## Goal
This repository provides a dockerized implementation of a FastAPI project, using the Titanic Kaggle competition as an example. It aims to serve as a learning resource for Docker and FastAPI integration.

## Requirements
To use this project, you need to have the following installed on your system:

> Docker: Install **Docker**

> Docker Compose (optional): Install **Docker Compose** (not required but recommended)


## Getting Started
To get started with this project, follow the steps below:

> Clone the repository: git clone https://github.com/Dimildizio/WorksOnMyMachine.git

> Go to project dir: cd WorksOnMyMachine

> Build Docker image: docker build -t worksonmymachine .

> go to the flask_app subfolder: cd app/flask_app

> Build Docker image: docker build -t titanicflask -f Dockerfile_flask .

> Run docker container on port 8000 of you local machine: docker run -p 8000:8000 worksonmymachine

> Run docker containeron port 5000 of you local machine: docker run -p 5000:5000 titanicflask

**Note**: If you make any changes to the code or configuration files, you'll need to rebuild the respective Docker image(s) and restart the container(s).

(_Optional_) If you prefer to use Docker Compose, ensure that Docker Compose is installed. Then, run the following command to start both the FastAPI and Flask applications:

> docker-compose up

This will start the FastAPI application on http://localhost:8000 and the Flask application on http://localhost:5000, accessible from your local machine.

**Note**: If you make any changes to the code or configuration files, you can use the **docker-compose up --build** command to rebuild the Docker images and apply the changes.

Open a web browser and visit http://localhost:8000 to access the FastAPI application. If you are using Docker Compose, you can also access the Flask application at http://localhost:5000.

## Usage 

In further development proccess buttons or checkboxes could be created to represent a particular passenger's features. Upon a click the code will predict the chance of survival. 

## Customization
If you wish to customize the FastAPI implementation or use your own dataset, you can modify the following files:

> app/main.py: This file contains the FastAPI routes and logic. You can update the implementation according to your requirements.

> app/models.py: Todo. Here, you'll be able modify the data models used in the project. It will provide a simplified model for the Titanic dataset.

> data/train.csv and data/test.csv: These files contain the example Titanic dataset used in the project. If you want to use your own dataset, you can replace these files with your own CSV file. Ensure that the column names and types match the ones expected by the FastAPI implementation.

## Contributing
Contributions to this project are welcome! If you have any improvements or suggestions, feel free to open an issue or submit a pull request.

## License
This project is licensed under the MIT License. Feel free to use, modify, and distribute it as per the terms of this license.
