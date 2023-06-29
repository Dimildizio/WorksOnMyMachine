import pandas as pd
from data_encoder import create_encoder, encode_data


def get_title(df):
    df['Title'] = df['Name'].str.extract(' ([A-Za-z]+)\.', expand=False)
    df['Title'] = df['Title'].replace(['Dr', 'Col', 'Sir', 'Major', 'Master'], 'Mr')
    df['Title'] = df['Title'].replace(['Capt', 'Don', 'Jonkheer'], 'Rev')
    df['Title'] = df['Title'].replace(['Ms', 'Lady', 'Mlle', 'Countess', 'Mme', 'Dona'], 'Rev_fem')
    return df


def get_family(df):
    df['Family_size'] = df['Parch']+df['SibSp'] + 1
    return df


def get_deck(df):
    df['Cabin'].fillna('Z', inplace=True)
    df['Deck'] = df['Cabin'].str.extract(r'([A-Za-z]+)')
    return df


def drop_useless(df):
    df = df.drop(['PassengerId', 'Name', 'Cabin', 'Ticket'], axis=1)
    return df


def get_age_buckets(df):
    # labels are 'Child', 'Young Adult', 'Adult', 'Senior'
    df['AgeBucket'] = pd.cut(df['Age'], bins=[0, 18, 30, 50, 80], labels=[1, 2, 3, 4])
    # print('empty buckets: ', df[df['AgeBucket'].isna()])
    df['AgeBucket'] = df['AgeBucket'].astype('int16')
    return df


def get_fare_per_person(df):
    df['PersonFare'] = df['Fare'] / df['Family_size']
    return df


def fill_na(df):
    df['Fare'].fillna(df['Fare'].mean(), inplace=True)
    df['Embarked'].fillna(df['Embarked'].mode()[0], inplace=True)
    return df


def apply_all(data):
    df = data.copy()
    for func in [fill_na, get_title, get_family, get_fare_per_person, get_deck,
                 drop_useless]:  # , predict_age, get_age_buckets, change_dtypes]:
        df = func(df)
    return df


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

