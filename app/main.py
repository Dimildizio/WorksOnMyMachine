from fastapi import FastAPI
# from pydantic import BaseModel

app = FastAPI()


@app.get('/')
def read_root():
    return {"message": "I'm a TitanicAPI created to learn Docker+FastAPI. Titanic dataset task"
                       " is used as a simple ML task here"}
