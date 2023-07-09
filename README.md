# WorksOnMyMachine

## Goal
This repository provides a dockerized implementation of a FastAPI and Flaskproject, using the Titanic Kaggle competition as an example and catboost model optimized to ONNX for faster inference. It aims to serve as a learning resource for Docker, Flask, ML optimization, CSS, web animation, webdev and FastAPI integration.

## Requirements
To use this project, you need to have the following installed on your system:

> Docker: Install **Docker**

> Docker Compose (optional): Install **Docker Compose** (not required but recommended)

> **Note**: The original model is Catboost but due to the size of the library it's not included into the Docker image. Instead it's converted to ONNX and used on inference. If you wish to retrain the model or run the training part of the code, you need to install Catboost manually.  


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

Open a web browser and visit http://localhost:8000 to access the FastAPI application. If you are using Docker Compose, you can also access the Flask application at http://localhost:5000. The latter is preferred since the webpage will show up all fancy and shiny.

## Usage 

>Run the docker-compose.yml and proceed to localhost:5000 

> Fill in the webform and learn your fate on Titanic.
![image](https://github.com/Dimildizio/WorksOnMyMachine/assets/42382713/fbdbfa99-16aa-493a-b6f6-6e029365abbe)

> Bonus points if you find the easter eggs hidden on each page.

> Double points for finding the secret page.  


## Customization
If you wish to customize the FastAPI implementation or use your own dataset, you can modify the following files:

> app/main.py: This file contains the FastAPI routes and logic. You can update the implementation according to your requirements.
 
> app/models.py: Here, you'll be able modify the data models used in the project. It will provide a simplified model for the Titanic dataset.

> data/train.csv and data/test.csv: These files contain the example Titanic dataset used in the project. If you want to use your own dataset, you can replace these files with your own CSV file. Ensure that the column names and types match the ones expected by the FastAPI implementation.

If you with to change the pictures and animation on the webpage:

> app/flask_app/templates and app/flask_app/static: for pictures and css. Duplicated if you wish to run an html page without using url_for for css styles with flask. 

## Contributing
Contributions to this project are welcome! If you have any improvements or suggestions, feel free to open an issue or submit a pull request.

## License
This project is licensed under the MIT License. Feel free to use, modify, and distribute it as per the terms of this license.
