"""
train_preprocess.py

This module contains functions for preprocessing the training data.
Script for model training. Requires sklearn and catboost which are not included in Docker files additionally installed.

Functions:
- cut_outlier(data): Remove outliers from the input DataFrame based on the 'Age' and 'PersonFare' columns.
- predict_age(train, test): Predict missing 'Age' values in the DataFrame using a model trained  on the
  train+test DataFrames.
- train_encoder(cols=['Sex', 'Title', 'Deck', 'Embarked']): Train an encoder on the specified columns of the
  concatenated train and test datasets.
- load_encoder(data): Apply preprocessing steps to the input DataFrame and encode the transformed data using a
  trained encoder.
"""

import pandas as pd
from data_encoder import create_encoder, encode_data
from predict_age_model import age_predictor
from dataframe_manipulations import apply_all
from typing import Tuple


def cut_outlier(data: pd.DataFrame) -> pd.DataFrame:
    """
    Remove outliers from the input DataFrame based on the 'Age' and 'PersonFare' columns.
    Parameters:
    - data (pandas.DataFrame): The input DataFrame.
    Returns:
    - data (pandas.DataFrame): The DataFrame with outliers removed.
    """

    data = data[data['Age'] < 70]
    data = data[data['PersonFare'] < 300]
    return data


def predict_age(train: pd.DataFrame, test: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Predict missing 'Age' values in the DataFrame using a model trained on both concatenated test and train DataFrame.
    Parameters:
    - train (pandas.DataFrame): The training DataFrame.
    - test (pandas.DataFrame): The test DataFrame.
    Returns:
    - age_predictions (pandas.Series): The predicted 'Age' values for the DataFrame.
    """

    df_train = load_encoder(train.copy().drop('Survived', axis=1))
    df_test = load_encoder(test.copy())
    return age_predictor(df_train, df_test, train['Survived'])


def train_encoder(cols: list = ['Sex', 'Title', 'Deck', 'Embarked']) -> pd.DataFrame:
    """
    Train an encoder on the specified columns of the concatenated train and test datasets:
    - Drop target value for train
    - Combine test and train
    - Apply necessary transformations to columns
    - Train encoder model
    - Reassemble the datasets
    Parameters:
    - cols (list): The list of column names to use for training the encoder.
                    Default is ['Sex', 'Title', 'Deck', 'Embarked'].
    Returns:
    - df (pandas.DataFrame): The concatenated DataFrame with encoded columns.
    """

    train = pd.read_csv('data/train.csv')
    test = pd.read_csv('data/test.csv')

    df = pd.concat([train.drop('Survived', axis=1), test], axis=0)
    df = apply_all(df)
    part_1 = df[cols]
    part_2 = df.drop(cols, axis=1)

    part_1_encoded = create_encoder(part_1)
    df = pd.concat([part_1_encoded, part_2], axis=1)
    return df


def load_encoder(data) -> pd.DataFrame:
    """
    Apply preprocessing steps to the input DataFrame and encode the transformed data using a trained encoder.
    Parameters:
    - data (pandas.DataFrame): The input DataFrame.
    Returns:
    - transformed_data (pandas.DataFrame): The transformed and encoded DataFrame.
    """

    transformed_data = apply_all(data)
    return encode_data(transformed_data)


if __name__ == '__main__':
    train_encoder()
