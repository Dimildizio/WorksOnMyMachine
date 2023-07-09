"""
onnx_model.py

This module contains functions for performing inference using an ONNX model.

Functions:
- apply_encoder(data): Apply encoding transformations to the input data using pre-trained encoders.
- onnx_inference(df): Perform inference using an ONNX model on the input DataFrame.
- get_onnx_model(): Load the ONNX model for inference.
- prepare_onnx_vals(df): Prepare the input DataFrame for ONNX inference.
- run_onnx(model, values): Run the ONNX model with the prepared input values and obtain the predictions.
- onnx_pred_info(model, vals): Print information about the ONNX model predictions.
"""

import onnxruntime
import pickle
from dataframe_manipulations import apply_all


def apply_encoder(df):
    """
    Apply encoding transformations to the input data using pre-trained encoders.
    Parameters:
    - data (pandas.DataFrame): The input DataFrame.
    Returns:
    - transformed_data (pandas.DataFrame): The transformed DataFrame.
    """

    transformed_data = apply_all(df)
    with open('encoder.pk1', 'rb') as f:
        encoders = pickle.load(f)
    for col, le in encoders.items():
        transformed_data[col] = le.transform(transformed_data[col])
    return transformed_data


def onnx_inference(df):
    """
    Perform inference using an ONNX model on the input DataFrame.
    Parameters:
    - df (pandas.DataFrame): The input DataFrame.
    Returns:
    - result: The inference result - an array with result.
    """

    values = prepare_onnx_vals(df)
    model = get_onnx_model()

    onnx_pred_info(model, values)
    result = run_onnx(model, values)
    return result[0]  # First value since we need only one


def get_onnx_model():
    """
    Load the ONNX model for inference. Duh.
    Returns:
    - model: The loaded ONNX model. For inference.
    """

    return onnxruntime.InferenceSession('models/titanicboost.onnx')


def prepare_onnx_vals(df):
    """
    Prepare the input DataFrame for ONNX inference.
    Parameters:
    - df (pandas.DataFrame): The input DataFrame.
    Returns:
    - values: The prepared input values extracted from DataFrame.
    """

    return df.values.astype('float32')


def run_onnx(model, values):
    """
    Run the ONNX model with the inputs.
    Parameters:
    - model: The ONNX model.
    - values: The prepared input values.
    Returns:
    - label: The predicted label.
    """

    label = model.run(['label'], {'features': values})
    return label


def onnx_pred_info(model, vals) -> None:
    """
    Print information about the ONNX model prediction probabilities.
    Parameters:
    - model: The ONNX model.
    - vals: The input values.
    Returns:
    - None
    """

    predictions = model.run(['probabilities'], {'features': vals})
    print('all predictions', predictions)
