from pydantic import BaseModel

from fastapi import FastAPI

app = FastAPI()

class Person(BaseModel):
    name: str
    last_name: str
    age: int
    hair_color: str | None = None
    is_married: bool | None = None

@app.get("/")
def root():
    return {"message": "Hello world!"}

# Request and response body
@app.post("/people")
def create_person(person: Person):
    return person
