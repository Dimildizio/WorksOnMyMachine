import pandas as pd
from model import predict

from data_encoder import encode_data

def process(title: str, sex: str, pclass: int, age: int, deck: str, fare: float, siblings: int,
            spouse: int, relatives: int, embarked: str):
    encoded_df = encode(title, sex, deck, embarked)

    return get_model_result()

def encode(title: str, sex: str, deck: str, embarked: str):
    to_encode = pd.DataFrame({'Sex': sex, 'Title': title, 'Deck': deck, 'Embarked': embarked})
    encoded_df = encode_data(to_encode)
    return encoded_df

def get_model_result(*args):
    return predict(*args)
