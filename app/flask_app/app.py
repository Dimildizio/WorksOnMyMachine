from flask import Flask, request, render_template
import requests
from random import randint


app = Flask(__name__)


@app.route('/')
def parameter_selection():
    return render_template('parameter_selection.html')


@app.route('/prediction', methods=['GET'])
def prediction():
    title = request.args.get('title')
    name = request.args.get('name')
    surname = request.args.get('surname')
    sex = request.args.get('sex')
    age = request.args.get('age')
    sibs = request.args.get('siblings')
    spouse = request.args.get('spouse')
    relatives = request.args.get('relatives')
    pclass = request.args.get('pclass')
    embarked = request.args.get('embarked')
    deck = request.args.get('deck')
    fare = 13.61
    ticket = randint(1, 3000)

    url = 'http://localhost:8000/prediction'
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

    return render_template('predicted_fate.html', message=message, fate=fate)


if __name__ == '__main__':
    app.run()
