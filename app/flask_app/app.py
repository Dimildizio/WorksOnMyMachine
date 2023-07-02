import requests
import os
from flask import Flask, request, render_template
from random import randint


app = Flask(__name__)


@app.route('/')
def parameter_selection():
    return render_template('parameter_selection.html')


@app.route('/prediction', methods=['POST', "GET"])
def prediction():
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

    if 'DOCKER_ENV' in os.environ:
        url = 'http://worksonmymachine-backend-1:8000/prediction'   # If ran through docker
    else:
        url = 'http://localhost:8000/prediction'  # If direct run without docker
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
    print("Rendering predicted_fate.html template")

    return render_template('predicted_fate.html', message=message, fate=fate)


if __name__ == '__main__':
    print('I am running')
    app.run()


