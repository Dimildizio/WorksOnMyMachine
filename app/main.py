from fastapi import FastAPI
from data_preprocessing import process

# from pydantic import BaseModel

app = FastAPI()


@app.get('/')
def read_root():
    return {"message": "I'm a TitanicAPI created to learn Docker+FastAPI. Titanic dataset task"
                       " is used as a simple ML task here"}


@app.get("/prediction")
# line should work like this: http://localhost:8000/prediction?title=Mr&surname=Johnes&name=John&sex=male&pclass=2&age=30&cabin=E3213&fare=76.4&siblings=1&spouse=0&relatives=1&embarked=S&ticket=121441
def make_prediction(title: str, name: str, surname: str, sex: str, pclass: int, age: int, cabin: str, fare: float,
                    siblings: int, spouse: int, relatives: int, embarked: str, ticket: str):

    if process(title, name, surname, sex, pclass, age, cabin, fare, siblings, spouse, relatives, embarked, ticket):
        result = f'{name} has survived'
    else:
        result = f'{name} has died'
    return {"Prediction": result}
