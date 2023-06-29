import pandas as pd
from model import predict

from train_preprocess import load_encoder


def process(title: str, name: str, surname: str, sex: str, pclass: int, age: int, cabin: str, fare: float,
            siblings: int, spouse: int, relatives: int, embarked: str, ticket: str):
    fullname = f'{name}, {title}. {surname}'
    to_encode = pd.DataFrame({'PassengerId': [9999], 'Name': [fullname], 'Sex': [sex], 'Cabin': [cabin],
                              'Embarked': [embarked], 'Fare': [fare], 'Ticket': [ticket], 'Age': [age],
                              'SibSp': [spouse+siblings], 'Parch': [relatives], 'Pclass': [pclass]})

    process_text(fullname, sex, pclass, age, cabin, fare, siblings, spouse, relatives, embarked, ticket)
    encoded_df = load_encoder(to_encode)
    return get_model_result(encoded_df)


def process_text(fullname: str, sex: str, pclass: int, age: int, cabin: str, fare: float, siblings: int,
                 spouse: int, relatives: int, embarked: str, ticket: str):
    port = {'S': 'Southampton', 'C': 'Cherbourg', 'Q': 'Queenstown'}
    txt = (f'You are {fullname}, a {age} year old {sex}, {pclass} class passenger in cabin {cabin}.\n'
           f'You got on Titanic at {port[embarked]} for {fare} pounds with {"a spouse " if spouse else ""}'
           f'{siblings if siblings else ""}{" siblings " if siblings else ""}{relatives if relatives else ""}'
           f'{" relatives" if siblings else ""}.\nYour ticket is number {ticket}')
    print(txt)


def get_model_result(*args):
    return predict(*args)


if __name__ == '__main__':
    print(process('Mrs', 'Claire', 'Labelle', 'female', 2, 32, 'C123', 17, 2, 0, 2, 'S', '113803'))
