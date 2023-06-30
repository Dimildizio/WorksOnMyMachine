import pandas as pd
from sklearn.ensemble import RandomForestRegressor


def age_pred(model, data: pd.DataFrame):
    missing = data['Age'].isnull()
    y_pred = model.predict(data.loc[missing].drop(['Age'], axis=1))
    data.loc[missing, 'Age'] = y_pred
    return data


def age_predictor(train: pd.DataFrame, test: pd.DataFrame, target:pd.Series) -> tuple:
    together = pd.concat([train, test], axis=0).dropna(subset=['Age'])
    y = together['Age']
    X = together.drop('Age', axis=1)

    model = RandomForestRegressor()
    model.fit(X, y)

    test = age_pred(model, test)
    train = age_pred(model, train)
    train['Survived'] = target
    return train, test

'''
if __name__ == '__main__':
    train_df = pd.read_csv('data/train.csv')
    test_df = pd.read_csv('data/test.csv')
    train_df = load_encoder(train_df)
    test_df = load_encoder(test_df)
    train_df, test_df = age_predictor(train_df.drop('Survived', axis=1), test_df, train_df['Survived'])
'''