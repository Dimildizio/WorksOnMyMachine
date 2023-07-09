"""
dataframe_manipulations.py

This module contains functions to manipulate and transform data within a DataFrame.

Functions:
- apply_all(data): Apply a series of transformations to the input DataFrame.
- get_title(df): Extract the title from the 'Name' column in the DataFrame and update it according to predefined rules.
- get_family(df): Calculate and add a 'Family_size' column to the DataFrame based on the 'Parch' and 'SibSp' columns.
- get_deck(df): Extract the deck information from the 'Cabin' column and create a new 'Deck' column in the DataFrame.
- drop_useless(df): Remove unnecessary columns from the DataFrame.
- get_fare_per_person(df): Calculate and add a 'PersonFare' column to the DataFrame by dividing 'Fare' by 'Family_size'.
- fill_na(df): Fill missing values in the 'Fare' and 'Embarked' columns with appropriate values.
- reassemble_order(data): Reorder the columns in the DataFrame to ensure compatibility with CatBoost models.

"""


def apply_all(data):
    """
    Apply a series of transformations to the input DataFrame.
    Parameters:
        - data (pandas.DataFrame): The input DataFrame.
    Returns:
        - df (pandas.DataFrame): The transformed DataFrame.
    """

    df = data.copy()
    for func in [fill_na, get_title, get_family, get_fare_per_person, get_deck,
                 drop_useless, reassemble_order]:
        df = func(df)
    return df


def get_title(df):
    """
    Extract the title from the 'Name' column in the DataFrame and update it according to predefined rules.
    Parameters:
        - df (pandas.DataFrame): The input DataFrame.
    Returns:
        - df (pandas.DataFrame): The DataFrame with the updated 'Title' column.
    """

    df['Title'] = df['Name'].str.extract(' ([A-Za-z]+)\.', expand=False)
    df['Title'] = df['Title'].replace(['Dr', 'Col', 'Sir', 'Major', 'Master'], 'Mr')
    df['Title'] = df['Title'].replace(['Capt', 'Don', 'Jonkheer'], 'Rev')
    df['Title'] = df['Title'].replace(['Ms', 'Lady', 'Mlle', 'Countess', 'Mme', 'Dona'], 'Rev_fem')
    return df


def get_family(df):
    """
    Calculate and add a 'Family_size' column to the DataFrame based on the 'Parch' and 'SibSp' columns.
    Parameters:
        - df (pandas.DataFrame): The input DataFrame.
    Returns:
        - df (pandas.DataFrame): The DataFrame with the added 'Family_size' column.
    """

    df['Family_size'] = df['Parch']+df['SibSp'] + 1
    return df


def get_deck(df):
    """
    Extract the deck information from the 'Cabin' column and create a new 'Deck' column in the DataFrame.
    Parameters:
        - df (pandas.DataFrame): The input DataFrame.
    Returns:
        - df (pandas.DataFrame): The DataFrame with the added 'Deck' column.
    """

    df['Cabin'].fillna('Z', inplace=True)
    df['Deck'] = df['Cabin'].str.extract(r'([A-Za-z]+)')
    return df


def drop_useless(df):
    """
    Remove unnecessary columns from the DataFrame.
    Parameters:
        - df (pandas.DataFrame): The input DataFrame.
    Returns:
        - df (pandas.DataFrame): The DataFrame with the unnecessary columns removed.
    """

    df = df.drop(['PassengerId', 'Name', 'Cabin', 'Ticket'], axis=1)
    return df


def get_fare_per_person(df):
    """
    Calculate and add a 'PersonFare' column to the DataFrame by dividing 'Fare' by 'Family_size'.
    Parameters:
        - df (pandas.DataFrame): The input DataFrame.
    Returns:
        - df (pandas.DataFrame): The DataFrame with the added 'PersonFare' column.
    """

    df['PersonFare'] = df['Fare'] / df['Family_size']
    return df


def fill_na(df):
    """
    Fill missing values in the 'Fare' and 'Embarked' columns with appropriate values.
    Parameters:
        - df (pandas.DataFrame): The input DataFrame.
    Returns:
        - df (pandas.DataFrame): The DataFrame with the missing values filled.
    """

    df['Fare'].fillna(df['Fare'].mean(), inplace=True)
    df['Embarked'].fillna(df['Embarked'].mode()[0], inplace=True)
    return df


def reassemble_order(df):
    """
    Reorder the columns in the DataFrame to ensure compatibility with CatBoost and it's onnx derivative models.
    Parameters:
        - data (pandas.DataFrame): The input DataFrame.
    Returns:
        - new_data (pandas.DataFrame): The DataFrame with the columns reordered.
    """

    new_data = df[['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked', 'Title', 'Family_size',
                   'PersonFare', 'Deck']]
    return new_data
