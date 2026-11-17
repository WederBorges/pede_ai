from pydantic import BaseModel, ConfigDict



class s_create_auth(BaseModel):

    email: str
    senha: str



class s_create_auth_out(BaseModel):

    access_token: str