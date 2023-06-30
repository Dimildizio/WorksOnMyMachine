import pandas as pd
from sklearn.ensemble import RandomForestRegressor


def age_pred(model, data: pd.DataFrame):
    missing = data['Age'].isnull()
    y_pred = model.predict(data.loc[missing].drop(['Age'], axis=1))
    data.loc[missing, 'Age'] = y_pred
    return data


def age_predictor(train: pd.DataFrame, test: pd.DataFrame, target: pd.Series) -> tuple:
    together = pd.concat([train, test], axis=0).dropna(subset=['Age'])
    y = together['Age']
    X = together.drop('Age', axis=1)

    model = RandomForestRegressor()
    model.fit(X, y)

    test = age_pred(model, test)
    train = age_pred(model, train)
    train['Survived'] = target
    return train, test
