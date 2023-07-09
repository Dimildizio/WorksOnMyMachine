"""
predict_age_model.py

This module contains functions for predicting missing 'Age' values using a RandomForestRegressor model.
Script for model training. Requires sklearn and which is not included in Docker files additionally installed.

Functions:
- age_pred(model, data): Predict missing 'Age' values using a trained model and update the corresponding rows
  in the DataFrame.
- age_predictor(train, test, target): Train a RandomForestRegressor model on the combined train and test DataFrames
  to predict missing 'Age' values.
"""

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from typing import Tuple


def age_pred(model, data: pd.DataFrame) -> pd.DataFrame:
    """
    Predict missing 'Age' values using a trained model and update the corresponding rows in the DataFrame.
    Parameters:
    - model: The trained model used for prediction.
    - data (pandas.DataFrame): The input DataFrame.
    Returns:
    - data (pandas.DataFrame): The DataFrame with updated 'Age' values.
    """

    missing = data['Age'].isnull()
    y_pred = model.predict(data.loc[missing].drop(['Age'], axis=1))
    data.loc[missing, 'Age'] = y_pred
    return data


def age_predictor(train: pd.DataFrame, test: pd.DataFrame, target: pd.Series) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Train a RandomForestRegressor model on the combined train and test DataFrames to predict missing 'Age' values.
    Parameters:
    - train (pandas.DataFrame): The training DataFrame.
    - test (pandas.DataFrame): The test DataFrame.
    - target (pandas.Series): The 'Survived' column from the training DataFrame.
    Returns:
    - tuple: A tuple containing the updated training DataFrame and the updated test DataFrame.
    """

    together = pd.concat([train, test], axis=0).dropna(subset=['Age'])
    y = together['Age']
    X = together.drop('Age', axis=1)

    model = RandomForestRegressor()
    model.fit(X, y)

    test = age_pred(model, test)
    train = age_pred(model, train)
    train['Survived'] = target
    return train, test
