from pydantic import BaseModel,Field,ConfigDict
from typing import Optional
from enum import Enum
from datetime import datetime

class ItemStatus(Enum):
    ON_SALE = "ON_SALE"
    SOLD_OUT = "SOLD_OUT"

class ItemCreate(BaseModel):
    name:str = Field(min_length=2,max_length=20,examples=["PC"])
    price:int = Field(gt=0,examples=[10000])
    description:Optional[str] = Field(None,examples=["美品です"])

class ItemUpdate(BaseModel):
    name:Optional[str]= Field(None,min_length=2,max_length=20,)
    price:Optional[str]= Field(None,examples=[100000])
    description:Optional[str] = Field(None, examples=["美品です"])
    status:Optional[ItemStatus]= Field(None,examples=[ItemStatus.SOLD_OUT])



class ItemResponse(BaseModel):
    id: int =Field(gt=0,example=[1])
    name:str =Field(min_length=2,max_length=20,examples=["PC"])
    price:int =Field(gt=0,example=[10000])
    description:Optional[str] =Field(None, examples=["美品です"])
    status :ItemStatus = Field(example=[ItemStatus.ON_SALE])
    created_at:datetime
    update_at:datetime

    model_config=ConfigDict(from_attributes=True)
