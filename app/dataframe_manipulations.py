"""dataframe_manipulations.py"""


def apply_all(data):
    df = data.copy()
    for func in [fill_na, get_title, get_family, get_fare_per_person, get_deck,
                 drop_useless, reassemble_order]:
        df = func(df)
    return df


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


def get_fare_per_person(df):
    df['PersonFare'] = df['Fare'] / df['Family_size']
    return df


def fill_na(df):
    df['Fare'].fillna(df['Fare'].mean(), inplace=True)
    df['Embarked'].fillna(df['Embarked'].mode()[0], inplace=True)
    return df


def reassemble_order(data):
    # Make sure columns a properly organized since catboost models are sensitive to the column order
    new_data = data[['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked', 'Title', 'Family_size',
                     'PersonFare', 'Deck']]
    return new_data
