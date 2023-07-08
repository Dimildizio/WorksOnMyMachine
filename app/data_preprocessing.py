import pandas as pd
from onnx_model import onnx_inference, apply_encoder


def process(title: str, name: str, surname: str, sex: str, pclass: int, age: int, cabin: str, fare: float,
            siblings: int, spouse: int, relatives: int, embarked: str, ticket: str):
    fullname = f'{name}, {title}. {surname}'
    to_encode = pd.DataFrame({'PassengerId': [9999], 'Name': [fullname], 'Sex': [sex], 'Cabin': [cabin],
                              'Embarked': [embarked], 'Fare': [fare], 'Ticket': [ticket], 'Age': [age],
                              'SibSp': [spouse+siblings], 'Parch': [relatives], 'Pclass': [pclass]})

    text = process_text(fullname, sex, pclass, age, cabin, fare, siblings, spouse, relatives, embarked, ticket)
    encoded_df = apply_encoder(to_encode)
    survived = get_model_result(encoded_df)
    return survived, text


def process_text(fullname: str, sex: str, pclass: int, age: int, cabin: str, fare: float, siblings: int,
                 spouse: int, relatives: int, embarked: str, ticket: str):
    port = {'S': 'Southampton', 'C': 'Cherbourg', 'Q': 'Queenstown'}
    txt = (f'You are {fullname}, a {age} year old {sex}, {pclass} class passenger in cabin {cabin}.\n'
           f'You got on Titanic at {port[embarked]} for {fare} pounds {"with " if any([spouse, siblings, relatives]) else ""} '
           f'{"a spouse " if spouse else ""} {siblings if siblings else ""}{" siblings " if siblings else ""}'
           f'{relatives if relatives else ""}{" relatives" if relatives else ""}.\n Your ticket is number {ticket}')
    print(txt)
    return txt


def get_model_result(*args):
    predicted = onnx_inference(*args)[0]
    print('Congratulations, you have survived the Titanic catastrophy' if predicted else 'Sorry, you have died')
    return predicted


if __name__ == '__main__':
    print(process('Mrs', 'Claire', 'Labelle', 'female', 1, 30, 'A123', 30, 0, 0, 0, 'S', '113803'))
