#modelos o esquemas para los post y get

#modelos json
from pydantic import BaseModel, Field, EmailStr
#modelos DB
from sqlalchemy import Table, Column, func
from sqlalchemy.sql.sqltypes import Integer, String, DateTime
from database.db import engine, meta_data

#establecer el modelo para los post
class PostSchema(BaseModel):
    id: int = Field(default=None)
    title: str = Field(...)
    content: str = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Securing FastAPI applications with JWT.",
                "content": "In this tutorial, you'll learn how to secure your application by enabling authentication using JWT. We'll be using PyJWT to sign, encode and decode JWT tokens...."
            }
        }

#modelo para el registro post
class UserSchema(BaseModel):
    fullname: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "fullname": "Abdulazeez Abdulazeez Adeshina",
                "email": "abdulazeez@x.com",
                "password": "weakpassword"
            }
        }

#modelo para el logeo post
class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "email": "abdulazeez@x.com",
                "password": "weakpassword"
            }
        }

# Modelo de la base de datos 
usersDB = Table("usuario", meta_data,
            Column("NAME_USER", String(200)), 
            Column("EMAIL_USER", String(100)),
            Column("CONTRASEÑA", String(200)),
            Column("TOKEN_USUARIO", String(200))
            )


meta_data.create_all(engine)