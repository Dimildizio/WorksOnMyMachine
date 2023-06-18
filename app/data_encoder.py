import pickle
from sklearn.preprocessing import LabelEncoder


def create_encoder(data):
    encoder = LabelEncoder()
    encoded = data.apply(lambda x: encoder.fit_transform(x))
    with open('encoder.pk1', 'wb') as f:
        pickle.dump(encoder, f)
    return encoded


def encode_data(data):
    #THIS HAS A PROBLEM - classes_ are all encoded labels not colnames
    encoder = get_encoder()
    return data.apply(lambda x: encoder.transform(x) if x.name in encoder.classes_ else x)



def get_encoder():
    with open('encoder.pk1', 'rb') as f:
        encoder = pickle.load(f)
    return encoder
