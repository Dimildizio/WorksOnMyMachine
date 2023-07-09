"""
data_encoder.py

This module contains functions for encoding categorical data using scikit-learn's LabelEncoder and saving the
encoders as pickle files.
Script for model training. Requires sklearn which is not included in Docker files additionally installed.

Functions:
- create_encoder(data): Create encoders for categorical columns in the input data and save them as pickle files.
- encode_data(data): Encode categorical data using the saved encoders.
- get_encoder(): Load the saved encoders from the pickle files.
"""


import pickle
from sklearn.preprocessing import LabelEncoder


def create_encoder(data):
    """
    Create multiple (for each categorical column in the input DataFrame) encoders and save them as pickle files.
    Parameters:
    - data (pandas.DataFrame): The input data containing categorical columns.
    Returns:
    - encoded (pandas.DataFrame): The encoded data.
    """

    encoders = {}
    encoded = data.copy()
    for col in encoded.columns:
        encoder = LabelEncoder()
        encoded[col] = encoder.fit_transform(encoded[col])
        encoders[col] = encoder
    with open('encoder.pk1', 'wb') as f:
        pickle.dump(encoders, f)
    return encoded


def encode_data(data):
    """
    Encode categorical data using the saved encoders.
    From the start of the project pickle were saved as .pk1 instead of .pkl, so it will be continued.
    Parameters:
    - data (pandas.DataFrame): The input data to be encoded.
    Returns:
    - encoded_data (pandas.DataFrame): The encoded data.
    """

    encoders = get_encoder()
    for col, le in encoders.items():
        data[col] = le.transform(data[col])
    return data


def get_encoder() -> dict:
    """
    Load the saved encoders from the pickle files.
    Returns:
    - encoders (dict): A dictionary containing the loaded encoders.
    """

    with open('encoder.pk1', 'rb') as f:
        encoders = pickle.load(f)
    return encoders
