# WorksOnMyMachine

## Goal
This repository provides a dockerized implementation of a FastAPI project, using the Titanic Kaggle competition as an example. It aims to serve as a learning resource for Docker and FastAPI integration.

## Requirements
To use this project, you need to have the following installed on your system:

> Docker: Install Docker

> Docker Compose (optional): Install Docker Compose (not required but recommended)

## Getting Started
To get started with this project, follow the steps below:

> Clone the repository: git clone https://github.com/Dimildizio/WorksOnMyMachine.git

> Go to project dir: cd WorksOnMyMachine

> Build Docker image: docker build -t worksonmymachine .

> Run docker container: docker run -p 8000:8000 WorksOnMyMachine

## Usage 

In further development proccess buttons or checkboxes could be created to represent a particular passenger's features. Upon click the code will predict the chance of survival. 

## Customization
If you wish to customize the FastAPI implementation or use your own dataset, you can modify the following files:

> app/main.py: This file contains the FastAPI routes and logic. You can update the implementation according to your requirements.

> app/models.py: Todo. Here, you'll be able modify the data models used in the project. It will provide a simplified model for the Titanic dataset.

> data/titanic.csv: This file contains the example Titanic dataset used in the project. If you want to use your own dataset, you can replace this file with your own CSV file. Ensure that the column names and types match the ones expected by the FastAPI implementation.

## Contributing
Contributions to this project are welcome! If you have any improvements or suggestions, feel free to open an issue or submit a pull request.

## License
This project is licensed under the MIT License. Feel free to use, modify, and distribute it as per the terms of this license.
