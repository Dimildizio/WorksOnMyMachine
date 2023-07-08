from fastapi import FastAPI, Query
from data_preprocessing import process


app = FastAPI()


@app.get('/')
def read_root():
    return {"message": "I'm a TitanicAPI created to learn Docker+FastAPI. Titanic dataset task"
                       " is used as a simple ML task here"}


@app.get("/prediction")
# line should work like this: http://localhost:8000/prediction?title=Mr&surname=Johnes&name=John&sex=male&pclass=2&age=30&cabin=E3213&fare=76.4&siblings=1&spouse=0&relatives=1&embarked=S&ticket=121441
async def make_prediction(title: str = Query(default='Mr', description="Passenger's title"),
                          name: str = Query(default='Jack', description="Passenger's name"),
                          surname: str = Query(default='Dawson', description="Passenger's surname"),
                          sex: str = Query(default='male', description="Passenger's gender"),
                          pclass: int = Query(default=1, description="Passenger's class"),
                          age: int = Query(default=20, description="Passenger's age"),
                          cabin: str = Query(default='G60', description="Code-number of Passenger's cabin"),
                          fare: float = Query(default=7, description="Price for the group ticket"),
                          siblings: int = Query(default=0, description="How many Passenger's siblings are with them"),
                          spouse: int = Query(default=0, description="Passenger's partner"),
                          relatives: int = Query(default=0, description="How many Passenger's children are onboard"),
                          embarked: str = Query(default='S', description="Port where the Passenger got on the ship"),
                          ticket: str = Query(default='6666', description="Passenger's ticket number")):

    output, text = process(title, name, surname, sex, pclass, age, cabin, fare,
                           siblings, spouse, relatives, embarked, ticket)

    response = {'Message': text}
    result = 'Congratulations! You have survived the Titanic catastrophy' if output else "Congratulations! " \
             "You are now in a better world! You have died in a Titanic catastrophy"
    print('the output type is: ', int(output))
    print(result)
    response['Prediction'] = bool(output)
    return response
