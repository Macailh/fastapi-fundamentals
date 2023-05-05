from typing import Annotated
from pydantic import BaseModel

from fastapi import FastAPI, Query, Path, Body

app = FastAPI()

class Person(BaseModel):
    id: int
    name: str | None = None
    last_name: str | None = None
    age: int | None = None
    hair_color: str | None = None
    is_married: bool | None = None

people_list = [Person(id=1, name="Salvador", last_name="German", age=23, hair_color="black", is_married=False),
               Person(id=2, name="Adrian", last_name="German", age=21, hair_color="black", is_married=False),
               Person(id=3, name="Gabriel", last_name="Hernandez", age=32, hair_color="blonde", is_married=False)]

@app.get("/")
def root():
    return {"message": "Hello world!"}

@app.get("/people")
def get_all_people():
    return people_list

@app.get("/people/{person_id}")
def show_person(person_id: Annotated[int, Path(title="The ID of the person to get", gt=0, le=1000)]):
    for person in people_list:
        if person.id == person_id:
            return person
    return None

@app.get("/people/")
def show_person_detail(name: Annotated[str | None, Query(min_length=3, max_length=50)] = None):
    return name

@app.post("/people")
def create_person(person: Annotated[Person, Body(...)]):
    return person
