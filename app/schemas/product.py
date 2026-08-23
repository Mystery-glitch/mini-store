from pydantic import BaseModel,ConfigDict,Field

class ProductCreate(BaseModel):
    name:str=Field(min_length=2,max_length=100)
    description:str|None=None
    price:float=Field(gt=0)
    category:str=Field(min_length=2,max_length=100)
    stock:int=Field(ge=0)

class ProductUpdate(BaseModel):
    name:str|None=Field(default=None,min_length=2,max_length=100)
    description:str|None=None
    price:float|None=Field(gt=0,default=None)
    category:str|None=Field(default=None,min_length=2,max_length=100)
    stock:int|None=Field(default=None,ge=0)

class ProductResponse(BaseModel):
    model_config=ConfigDict(from_attributes=True)

    id:int
    name:str
    description:str|None
    price:float
    category:str
    stock:int