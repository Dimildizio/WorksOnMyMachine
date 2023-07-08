import pickle
from sklearn.preprocessing import LabelEncoder


def create_encoder(data):
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
    encoders = get_encoder()
    for col, le in encoders.items():
        data[col] = le.transform(data[col])
    return data


def get_encoder():
    with open('encoder.pk1', 'rb') as f:
        encoders = pickle.load(f)
    return encoders
