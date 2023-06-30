import random
import pandas as pd
from catboost import Pool, CatBoostClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from train_preprocess import predict_age, cut_outlier


def predict(data):
    return random.random() > 0.7


def xy_split(data):
    X = data.drop('Survived', axis=1)
    y = data['Survived']
    return X, y


def train_val(X, y):
    return train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)


def get_train_pool(data):
    X, y = xy_split(data)
    X_train, X_val, y_train, y_val = train_val(X, y)
    train_pool = Pool(data=X_train, label=y_train)
    val_pool = Pool(data=X_val, label=y_val)
    return train_pool, val_pool, X_val, y_val


def predict_me(parameters, train_pool, val_pool, x_val, y_val):
    model = CatBoostClassifier(**parameters)
    model.fit(train_pool, eval_set=val_pool, early_stopping_rounds=50, verbose=False)
    y_pred = model.predict(x_val)
    acc = accuracy_score(y_pred, y_val)
    print(f"Accuracy: {acc:.3f}%")
    return model


def find_best_params(data):
    params = {'iterations': [100, 200, 300],
              'depth': [4, 5, 6, 8],
              'learning_rate': [0.01, 0.04, 0.004],
              'l2_leaf_reg': [1, 3, 5, 7]}
    grid_search = CatBoostClassifier().grid_search(params, data, cv=5, stratified=True,
                                                   shuffle=True, partition_random_seed=0, refit=True)
    return grid_search['params']


def prepare_train(data, best_result=False):
    train_pool, val_pool, X_val, y_val = get_train_pool(data)
    best_result = best_result if best_result else find_best_params(train_pool)
    model = predict_me(best_result, train_pool, val_pool, X_val, y_val)
    return model


def train_model(train_df, test_df):
    train_df, test_df = predict_age(train_df, test_df)
    train_df = cut_outlier(train_df)
    best_params = {'depth': 5, 'l2_leaf_reg': 7, 'iterations': 100, 'learning_rate': 0.04}
    model = prepare_train(train_df, best_params)
    return model


if __name__ == '__main__':
    tr_df = pd.read_csv('data/train.csv')
    tst_df = pd.read_csv('data/test.csv')
    mdl = train_model(tr_df, tst_df)
