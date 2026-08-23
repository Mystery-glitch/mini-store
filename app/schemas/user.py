# ConfigDict -> Used for configuration how Pydantic model behaves.
from pydantic import BaseModel,ConfigDict,EmailStr

class UserResponse(BaseModel):
    model_config=ConfigDict(from_attributes=True)

    id:int
    email:EmailStr
    role:str
    is_active:bool
    