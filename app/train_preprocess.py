import pandas as pd
from data_encoder import create_encoder, encode_data
from predict_age_model import age_predictor
from dataframe_manipulations import apply_all


def cut_outlier(data):
    data = data[data['Age'] < 70]
    data = data[data['PersonFare'] < 300]
    return data


def predict_age(train, test):
    df_train = load_encoder(train.copy().drop('Survived', axis=1))
    df_test = load_encoder(test.copy())
    return age_predictor(df_train, df_test, train['Survived'])


def train_encoder(cols=['Sex', 'Title', 'Deck', 'Embarked']):
    # Concatenates train and test datasets and train the encoder on both
    train = pd.read_csv('data/train.csv')
    test = pd.read_csv('data/test.csv')

    df = pd.concat([train.drop('Survived', axis=1), test], axis=0)
    df = apply_all(df)
    part_1 = df[cols]
    part_2 = df.drop(cols, axis=1)

    part_1_encoded = create_encoder(part_1)
    df = pd.concat([part_1_encoded, part_2], axis=1)
    return df


def load_encoder(data):
    transformed_data = apply_all(data)
    return encode_data(transformed_data)


if __name__ == '__main__':
    train_encoder()
