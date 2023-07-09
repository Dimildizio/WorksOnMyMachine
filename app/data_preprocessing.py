"""
data_preprocessing.py

This module contains functions for preprocessing passenger data and generating text descriptions based on the
provided information from Flask and FastAPI.

Functions:
- process(title, name, surname, sex, pclass, age, cabin, fare, siblings, spouse, relatives, embarked, ticket):
    Preprocess passenger data, apply encoding transformations, perform inference, and generate a text description.
- process_text(fullname, sex, pclass, age, cabin, fare, siblings, spouse, relatives, embarked, ticket):
    Generate a text description based on the passenger information and print it into the console.
- get_model_result(*args):
    Perform inference using an ONNX model and return the prediction result.
"""

import pandas as pd
from onnx_model import onnx_inference, apply_encoder
from typing import Tuple


def process(title: str, name: str, surname: str, sex: str, pclass: int, age: int, cabin: str, fare: float,
            siblings: int, spouse: int, relatives: int, embarked: str, ticket: str) -> Tuple[int, str]:
    """
    Preprocess passenger data, apply encoding transformations, perform inference, and generate a text description.
    Assembles and disassembles the title, name and surname since the model and supporting functions were written for
    a straight line of text and the idea to create visual interface and Flask inputs appeared later.
    Parameters:
       - title (str): Passenger's title.
       - name (str): Passenger's name.
       - surname (str): Passenger's surname.
       - sex (str): Passenger's gender.
       - pclass (int): Passenger's class.
       - age (int): Passenger's age.
       - cabin (str): Code-number of Passenger's cabin.
       - fare (float): Price for the group ticket.
       - siblings (int): How many Passenger's siblings are with them.
       - spouse (int): Passenger's partner with them.
       - relatives (int): How many Passenger's children are onboard.
       - embarked (str): Port where the Passenger got on the ship.
       - ticket (str): Passenger's ticket number.
    Returns:
       - tuple: A tuple containing the prediction result (True or False) and the generated text description.
       """

    fullname = f'{name}, {title}. {surname}'
    to_encode = pd.DataFrame({'PassengerId': [9999], 'Name': [fullname], 'Sex': [sex], 'Cabin': [cabin],
                              'Embarked': [embarked], 'Fare': [fare], 'Ticket': [ticket], 'Age': [age],
                              'SibSp': [spouse+siblings], 'Parch': [relatives], 'Pclass': [pclass]})

    text = process_text(fullname, sex, pclass, age, cabin, fare, siblings, spouse, relatives, embarked, ticket)
    encoded_df = apply_encoder(to_encode)
    survived = get_model_result(encoded_df)
    return survived, text


def process_text(fullname: str, sex: str, pclass: int, age: int, cabin: str, fare: float, siblings: int,
                 spouse: int, relatives: int, embarked: str, ticket: str) -> str:
    """
    Generate a text description based on the passenger information.
    Parameters:
        - fullname (str): Passenger's full name.
        - sex (str): Passenger's gender.
        - pclass (int): Passenger's class.
        - age (int): Passenger's age.
        - cabin (str): Code-number of Passenger's cabin.
        - fare (float): Price for the group ticket.
        - siblings (int): How many Passenger's siblings are with them.
        - spouse (int): Passenger's partner with them.
        - relatives (int): How many Passenger's children are onboard.
        - embarked (str): Port where the Passenger got on the ship.
        - ticket (str): Passenger's ticket number.
    Returns:
        - str: The generated text description.
    """
    port = {'S': 'Southampton', 'C': 'Cherbourg', 'Q': 'Queenstown'}
    txt = (f'You are {fullname}, a {age} year old {sex}, {pclass} class passenger in cabin {cabin}.'
           f'\nYou got on Titanic at {port[embarked]} for {fare} pounds'
           f' {"with " if any([spouse, siblings, relatives]) else ""} '
           f'{"a spouse " if spouse else ""} {siblings if siblings else ""}{" siblings " if siblings else ""}'
           f'{relatives if relatives else ""}{" relatives" if relatives else ""}.'
           f'\nYour ticket is number {ticket}')
    print(txt)
    return txt


def get_model_result(*args) -> bool:
    """
    Perform inference using a machine learning model and return the prediction result.
    Parameters:
        - args: Arguments to be passed to the ONNX model.
    Returns:
        - bool: The prediction result (True or False).
    """

    predicted = onnx_inference(*args)[0]
    print('Congratulations, you have survived the Titanic catastrophy' if predicted else 'Sorry, you have died')
    return predicted


if __name__ == '__main__':
    print(process('Mrs', 'Claire', 'Labelle', 'female', 1, 30, 'A123', 30, 0, 0, 0, 'S', '113803'))
