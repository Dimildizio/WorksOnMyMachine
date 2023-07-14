"""
app.py

This module contains the Flask application for handling parameter selection and making predictions.

Functions:
- parameter_selection(): Renders the parameter selection HTML template.
- prediction(): Handles the prediction request and renders the appropriate HTML template based on the prediction result.
- dicaprio(name, surname): Checks if the name and surname match "Jack Dawson" or "Leonardo DiCaprio" variations.
"""


import requests
import os
from flask import Flask, request, render_template
from random import randint


app = Flask(__name__, template_folder=os.path.join(os.getcwd(), 'templates'))


@app.route('/')
def parameter_selection() -> str:
    """
    Renders the parameter selection HTML template.
    Returns:
    - str: The rendered HTML template.
    """
    return render_template('parameter_selection.html')


@app.route('/prediction', methods=['POST', "GET"])
def prediction() -> str:
    """
    Handles the prediction request and renders the appropriate HTML template based on the prediction result.
    Returns:
    - str: The rendered HTML template.
    """

    title = request.args.get('title')
    name = request.args.get('name')
    surname = request.args.get('surname')
    sex = request.args.get('sex')
    age = int(request.args.get('age'))
    sibs = int(request.args.get('siblings'))
    spouse = int(request.args.get('spouse'))
    relatives = int(request.args.get('relatives'))
    pclass = int(request.args.get('pclass'))
    embarked = request.args.get('embarked')
    deck = request.args.get('deck')
    fare = 13.61
    ticket = randint(1, 3000)

    if sex == 'male' and dicaprio(name, surname):
        message = "Sorry, Leo there wasn't enough space on that door"
        # Change for other html page
        page = render_template('leo.html', message=message)
        return page

    url = 'http://worksonmymachine-backend-1:8000/prediction'
    params = {
        'title': title,
        'name': name,
        'surname': surname,
        'sex': sex,
        'pclass': pclass,
        'age': age,
        'cabin': deck,
        'fare': fare,
        'siblings': sibs,
        'spouse': spouse,
        'relatives': relatives,
        'embarked': embarked,
        'ticket': ticket}

    response = requests.get(url, params=params)

    result = response.json()
    message = result['Message']
    fate = result['Prediction']
    print("Rendering predicted fate template")
    print(fate)
    if fate:
        # Survived page
        page = render_template('fate_survived.html', message=message, fate=fate)
    else:
        # Change later for death page
        page = render_template('fate_died.html', message=message, fate=fate)
    return page


def dicaprio(name: str, surname: str) -> bool:
    """
    Checks if the name and surname match "Jack Dawson" or "Leonardo DiCaprio" variations.
    Parameters:
    - name (str): The passenger's name.
    - surname (str): The passenger's surname.
    Returns:
    - bool: True if the name and surname match "Jack Dawson" or "Leonardo DiCaprio" variations, False otherwise.
    """

    jack = name.lower() in ['jack', 'джек']
    dawson = surname.lower() in ['dawson', 'доусон', 'довсон', 'даусон', 'досон']
    leo = name.lower() in ['leo', 'leonardo', 'леонардо', 'лео']
    di = ''.join(surname.split()).lower() in ['dicaprio', 'дикаприо']
    return (leo and di) or (jack and dawson)


if __name__ == '__main__':
    print('I am running')
    app.run()
