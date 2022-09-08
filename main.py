#python
from typing import Optional #esto para hacer tipado estatico
from enum import Enum

#pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr

#fastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import HTTPException
from fastapi import Body,Query,Path,Form,Header,Cookie,File,UploadFile




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
    status_code=status.HTTP_200_OK,
    tags=["Home"])
def home():
    return {"hello":"worl"}

#request and response body
@app.post(
    "/person/new",
    response_model=PersonOut,
    status_code = status.HTTP_201_CREATED,
    tags=["Persons"],
    summary="Create person in the app")
def create_person(person:Person=Body(...)):
    """
    Create Person

    This path operation create a person in the app and save information in database.
    
    Parameters:
    -Request body parameter:
        -**person: Person** ->  A person model with first name, last name, email,hair color, marital status and password 
    
    Returns a person model with first name, last name, age, email hair color and marital status
    
    """
    return person

#validaciones: query parameters

@app.get("/person/detail/",
status_code=status.HTTP_200_OK,
tags=["Persons"],
deprecated=True
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

persons =[1,2,3,4,5]
@app.get(
    "/person/detail/{person_id}",
    tags=["Persons"])
def show_person(
    person_id:int =Path(
        ..., 
        gt=0,
        title="Person Id",
        description="This is the person Id, it's requierd and it shot be grather than 0"
        )
):
    if person_id not in persons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="this person doesn't exist"
        )
    return {person_id: "It exists!"}

#validacion request body
@app.put(
    path="/person/person/{person_id}",
    tags=["Persons"])
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
    status_code=status.HTTP_200_OK,
    tags=["autentication"]
)
def login(username:str = Form(...),password:str= Form(...)):
    return LoginOut(username=username)

#Cookies and Headers Parameters
@app.post(
    path="/contact",
    status_code=status.HTTP_200_OK,
    tags=["Form"]
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
@app.post(
    path="/post-image",
    tags=["imagens"]
)
def post_image(
    image:UploadFile = File(...)
):
   return{ 
    "filename":image.filename,
    "format":image.content_type,
    "Size(kb)":round(len(image.file.read())/1024,ndigits=2) #para obter los kilobites tienes que dividir los bites entre 1024 
    }

#http exception
