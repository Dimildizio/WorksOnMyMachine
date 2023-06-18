from fastapi import FastAPI
from data_preprocessing import process
# from pydantic import BaseModel

app = FastAPI()


@app.get('/')
def read_root():
    return {"message": "I'm a TitanicAPI created to learn Docker+FastAPI. Titanic dataset task"
                       " is used as a simple ML task here"}


@app.get("/prediction")
def make_prediction(name: str, title: str, sex: str, pclass: int, age: int, deck: str, fare: float, siblings: int,
                    spouse: int, relatives: int, embarked: str):
    if process(title, sex, pclass, age, deck, fare, siblings, spouse, relatives, embarked):
        result = f'{name} has survived'
    else:
        result = f'{name} has died'
    return {"Prediction": result}
