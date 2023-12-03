from pydantic import BaseModel, Field, ConfigDict


class AuthBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: str = Field(..., example="test@test.com", min_length=5, max_length=50)
    password: str = Field(..., example="test123456", min_length=8, max_length=256)


class Signup(AuthBase):
    first_name: str = Field(..., example="Роберт", min_length=2, max_length=30)
    last_name: str = Field(..., example="Ласурия", min_length=2, max_length=30)


class Login(AuthBase):
    ...


class AccessToken(BaseModel):
    access_token: str
    token_type: str = "Bearer"
