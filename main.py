#python
from dataclasses import field
from doctest import Example
from typing import Optional #esto para hacer tipado estatico
from enum import Enum

#pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr

#fastAPI
from fastapi import FastAPI
from fastapi import Body
from fastapi import Query
from fastapi import Path,Form,Header,Cookie
from fastapi import status



app = FastAPI()

#Models
class HairColor(Enum):
    white="white"
    brown="brown"
    blonde="blonde"
    red="red"

class Country(Enum):
    Colombia="Colombia"
    Brazil="Brazil"
    Ecuador="Ecuador"
    Peru="Peru"
    Uruguay="Uruguay"
    Argentina="Argentina"
    Bolivia="Bolivia"
    Venezuela="Venezuela"

class Location(BaseModel):
    city:str = Field(
        ...,
        max_length=50,
        min_length=1)
    state:str = Field(
        ...,
        max_length=50,
        min_length=1)
    country:Country

class PersonModel(BaseModel):
    first_name: str =Field(
        ...,
        min_length=1,
        max_length=50,
        example="Ivan "
        
    )
    last_name:str  =Field(
        ...,
        min_length=1,
        max_length=50,
        example="Palencia Benavide"
    )
    age: int = Field(
        ...,
        gt=0,
        le=115,
        example=25)
    email:EmailStr 
    hair_color:Optional[HairColor] = Field(default=None)
    is_married:Optional[bool] = Field(default=None)

class Person(PersonModel):
    password: str = Field(
        ...,
        min_lenght=8,
        example="EstaEsLaContrasenaDeEjemplo")

class LoginOut(BaseModel):
    username:str = Field(
    ...,
    max_length=20,
    example="ivanfastapi")

class PersonOut(PersonModel):
    pass

   # class Config:
    #    schema_extra ={
     #       "example":{
      #          "first_name":"Ivan",
       #         "last_name":"Palencia Benavide",
        #        "age":21,
         #       "email":"ivan@ejemplo.com",
          #      "hair_color":"Black",
           #     "is_married":"false"
            #}
        #}

 #path operation       
@app.get(
    "/",
    status_code=status.HTTP_200_OK)
def home():
    return {"hello":"worl"}

#request and response body
@app.post(
    "/person/new",
    response_model=PersonOut,
    status_code = status.HTTP_201_CREATED)
def create_person(person:Person=Body(...)):
    return person

#validaciones: query parameters

@app.get("/person/detail/",
status_code=status.HTTP_200_OK
)
def show_person(
name: Optional[str]=Query(
    None,
    min_lenght=1,
    max_lenght=50,
    title="Person Name",
    description="this is the person name it's between 1 and 50 character"
    ),
age: str=Query(
    ...,
    title="person age",
    description="this is person age. It's requierd"
    )
):
    return {name:age}

#validacion: path parameter
@app.get("/person/detail/{person_id}")
def show_person(
    person_id:int =Path(
        ..., 
        gt=0,
        title="Person Id",
        description="This is the person Id, it's requierd and it shot be grather than 0"
        )
):
    return {person_id: "It exists!"}

#validacion request body
@app.put("/person/person/{person_id}")
def update_person(
    person_id:int=Path(
        ...,
        titles="Person Id",
        description="This is the person Id,it should be greather than 0 ",
        gt=0),
        
    person:Person=Body(...),
    #location : Location=Body(...)
):
#los modelos deben ser devueltos como diccionarios, pero primero devemos combinarlos en un solo diccionario
    #results:dict #aqui declaramos la variable result con el tipo de dato que alojara
    #results = person.dict()
    #results.update(location.dict())
    #return results
    return person

#forms
@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK
)
def login(username:str = Form(...),password:str= Form(...)):
    return LoginOut(username=username)

#Cookies and Headers Parameters
@app.post(
    path="/contact",
    status_code=status.HTTP_200_OK
)
def contact(
    first_name: str = Form(
       ...,
       max_length=20,
       min_length=1
    ),
    last_name:str=Form(
       ...,
       max_length=20,
       min_length=1
    ),
    email:EmailStr = Form(...),
    message:str=Form(
        ...,
        min_length=20
    ),
    #apartir de aqui los parametros que viene del header
    user_agent: Optional[str]=Header(default=None),
    ads : Optional[str] = Cookie(default=None)
):
    return user_agent

#archivos o files