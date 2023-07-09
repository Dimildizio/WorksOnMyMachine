"""
model.py

This module contains functions for training and using a CatBoostClassifier model on the Titanic dataset.
Script for model training. Requires sklearn and catboost which are not included in Docker files additionally installed.


Functions:
- predict(data): Perform predictions using a trained CatBoostClassifier model.
- xy_split(data): Split the input data into features (X) and labels (y).
- train_val(X, y): Split the data into training and validation sets.
- get_train_pool(data): Create training and validation Pools for CatBoostClassifier.
- predict_me(parameters, train_pool, val_pool, x_val, y_val): Train a CatBoostClassifier model and make predictions
on the validation set.
- find_best_params(data): Perform grid search to find the best hyperparameters for CatBoostClassifier.
- prepare_train(data, best_result=False): Prepare the training data, perform hyperparameter search (optional),
and train a CatBoostClassifier model.
- train_model(train_df, test_df): Perform data preprocessing, train a CatBoostClassifier model, and return
the trained model.
- create_model(): Load the train and test datasets, train a CatBoostClassifier model, and save it to a file.
- save_onnx_model(): Load a trained CatBoostClassifier model and save it in ONNX format.
- load_model(): Load a trained CatBoostClassifier model from a file.
"""

import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from train_preprocess import predict_age, cut_outlier
from catboost import Pool, CatBoostClassifier


def predict(data: Pool):
    """
    Perform predictions using a trained CatBoostClassifier model.
    Parameters:
    - data (Pool) : The data to make predictions on.
    Returns:
    - model_result: The prediction results.
    """

    model = load_model()
    model_result = model.predict(data)
    return model_result


def xy_split(data: pd.DataFrame) -> tuple:
    """
    Split the input data into features (X) and labels (y).
    Parameters:
    - data: The input data.
    Returns tuple:
    - X: The features.
    - y: The labels.
    """

    X = data.drop('Survived', axis=1)
    y = data['Survived']
    return X, y


def train_val(X, y) -> tuple:
    """
    Split the data into training and validation sets.
    Parameters:
    - X: The features.
    - y: The labels.
    Returns:
    - tuple: A tuple containing the training and validation sets.
    """

    return train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)


def get_train_pool(data: pd.DataFrame) -> tuple:
    """
    Create training and validation Pools for CatBoostClassifier.
    Parameters:
    - data (pd.DataFrame): The input data.
    Returns:
    - tuple: A tuple containing the training pool, validation pool, features (X) of the validation set,
      and labels (y) of the validation set.
    """

    X, y = xy_split(data)
    X_train, X_val, y_train, y_val = train_val(X, y)
    train_pool = Pool(data=X_train, label=y_train)
    val_pool = Pool(data=X_val, label=y_val)
    return train_pool, val_pool, X_val, y_val


def predict_me(parameters: dict, train_pool, val_pool, x_val, y_val) -> CatBoostClassifier:
    """
    Train a CatBoostClassifier model and make predictions on the validation set.
    Parameters:
    - parameters (dict): The hyperparameters for training the CatBoostClassifier model.
    - train_pool: The training pool.
    - val_pool: The validation pool.
    - x_val: The features of the validation set.
    - y_val: The labels of the validation set.
    Returns:
    - model: The trained CatBoostClassifier model.
    """

    model = CatBoostClassifier(**parameters)
    model.fit(train_pool, eval_set=val_pool, early_stopping_rounds=50, verbose=False)
    y_pred = model.predict(x_val)
    acc = accuracy_score(y_pred, y_val)
    print(f"Accuracy: {acc:.3f}%")
    return model


def find_best_params(data) -> dict:
    """
     Perform grid search to find the best hyperparameters for CatBoostClassifier.
     Parameters:
     - data: The input data.
     Returns:
     - dict: The best hyperparameters.
     """

    params = {'iterations': [100, 200, 300],
              'depth': [4, 5, 6, 8],
              'learning_rate': [0.01, 0.04, 0.004],
              'l2_leaf_reg': [1, 3, 5, 7]}
    grid_search = CatBoostClassifier().grid_search(params, data, cv=5, stratified=True,
                                                   shuffle=True, partition_random_seed=0, refit=True)
    return grid_search['params']


def prepare_train(data, best_result=False) -> CatBoostClassifier:
    """
    Prepare the training data, perform hyperparameter search (optional), and train a CatBoostClassifier model.
    Parameters:
    - data: The training data.
    - best_result: Whether to use the best hyperparameters found through grid search. If not empty use given.
    Returns:
    - model: The trained CatBoostClassifier model.
    """

    train_pool, val_pool, X_val, y_val = get_train_pool(data)
    print(X_val.columns)
    print(X_val.head(2))
    best_result = best_result if best_result else find_best_params(train_pool)
    model = predict_me(best_result, train_pool, val_pool, X_val, y_val)
    return model


def train_model(train_df: pd.DataFrame, test_df: pd.DataFrame) -> CatBoostClassifier:
    """
    Perform data preprocessing, train a CatBoostClassifier model, and return the trained model.
    Parameters:
    - train_df: The training DataFrame.
    - test_df: The test DataFrame.
    Returns:
    - model: The trained CatBoostClassifier model.
    """

    train_df, test_df = predict_age(train_df, test_df)
    train_df = cut_outlier(train_df)
    best_params = {'depth': 5, 'l2_leaf_reg': 7, 'iterations': 100, 'learning_rate': 0.04}
    model = prepare_train(train_df, best_params)
    return model


def create_model() -> None:
    """
    Load the train and test datasets, train a CatBoostClassifier model, and save it to a file.
    """

    train_df = pd.read_csv('data/train.csv')
    test_df = pd.read_csv('data/test.csv')
    os.makedirs('models', exist_ok=True)
    model = train_model(train_df, test_df)
    model.save_model('models/titanicboost.cbm')


def save_onnx_model() -> None:
    """
    Load a trained CatBoostClassifier model and save it in ONNX format.
    """
    model = load_model()
    model.save_model("models/titanicboost.onnx",
                     format="onnx",
                     export_parameters={
                        'onnx_domain': 'ai.catboost',
                        'onnx_model_version': 1,
                        'onnx_doc_string': 'model for titanic binary classification',
                        'onnx_graph_name': 'titanic_binary_catboost_classification'})


def load_model() -> CatBoostClassifier:
    """
    Load a trained CatBoostClassifier model from a file.
    Returns:
    - model: The loaded CatBoostClassifier model.
    """

    model = CatBoostClassifier()
    model.load_model('models/titanicboost.cbm')
    return model


if __name__ == '__main__':
    create_model()
    save_onnx_model()
