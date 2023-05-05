from typing import Annotated
from pydantic import BaseModel, Field

from enum import Enum

from fastapi import FastAPI, Query, Path, Body

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

    
    class Config:
        schema_extra = {
            "example": {
                "name": "Foo",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.3,
            }
        }

class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    red = "red"
    blonde = "blonde"

class Person(BaseModel):
    id: int
    name: str = Field(default="Jhon", min_length=1, max_length=50)
    last_name: str | None = Field(default="Doe", min_length=1, max_length=50)
    age: int = Field(default=0, ge=0, le=200)
    hair_color: HairColor = Field(default="black")
    is_married: bool = Field(default=False)

    class Config:
        schema_extra = {
            "example": {
                "name": "Jane",
                "lastname": "Doe",
                "age": 0,
                "hair_color": "black"
            }
        }

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

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results

@app.post("/items")
def create_item(item: Annotated[Item, Body(...)]):
    return item
