import onnxruntime
import pickle
from dataframe_manipulations import apply_all


def apply_encoder(data):
    transformed_data = apply_all(data)
    with open('encoder.pk1', 'rb') as f:
        encoders = pickle.load(f)
    for col, le in encoders.items():
        transformed_data[col] = le.transform(transformed_data[col])
    return transformed_data


def onnx_inference(df):
    values = prepare_onnx_vals(df)
    model = get_onnx_model()

    onnx_pred_info(model, values)
    result = run_onnx(model, values)
    return result[0]  # First value since we need only one


def get_onnx_model():
    return onnxruntime.InferenceSession('models/titanicboost.onnx')


def prepare_onnx_vals(df):
    return df.values.astype('float32')


def run_onnx(model, values):
    label = model.run(['label'], {'features': values})
    return label


def onnx_pred_info(model, vals):
    predictions = model.run(['probabilities'], {'features': vals})
    print('all predictions', predictions)
