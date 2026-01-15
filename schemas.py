from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime



class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8)

class UserResponse(BaseModel):
    id: int
    username: str
    created_at: datetime

    class Config:
        orm_mode = True

class EncyclopediaCreate(BaseModel):
    name: str
    created_by: int
    description : str

class EncyclopediaResponse(BaseModel):
    id: int
    name: str
    description : str
    created_by: int
    created_at: datetime

    class Config:
        orm_mode = True

class CollectionCreate(BaseModel):
    name: str
    encyclopedia_id: int
    description : str
    configuration: Optional[Dict[str, Any]] = None


class CollectionResponse(BaseModel):
    id: int
    name: str
    description : str
    encyclopedia_id: int
    created_at: datetime
    meta: Optional[Dict[str, Any]] = None

    class Config:
        orm_mode = True


class ElementCreate(BaseModel):
    name: str
    description: str
    data: Optional[Dict[str, Any]] = None
    collection_id: int


class ElementResponse(BaseModel):
    id: int
    name: str
    description : str
    meta: Optional[Dict[str, Any]] = Field(None, alias="data")
    created_at: datetime
    collection_id: int

    class Config:
        orm_mode = True

class ElementsResponse(BaseModel):
    id: int
    name: str
    created_at: datetime

    class Config:
        orm_mode = True


class ElementUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    collection_id: Optional[int] = None



class TagCreate(BaseModel):
    name: str
    description : str

class TagResponse(BaseModel):
    id: int
    name: str
    description : str
    created_at: datetime    

    class Config:
        orm_mode = True