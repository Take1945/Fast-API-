from typing import Annotated
from fastapi import APIRouter,Path,Query,HTTPException,Depends
from sqlalchemy.orm import Session
from cruds import item as item_cruds
from models import ItemCreate,ItemUpdate,ItemResponse
from typing import Optional
from database import get_db
DbDependency = Annotated[Session,Depends(get_db)]
router = APIRouter(prefix="/items",tags=["items"])

@router.get("",response_model=list[ItemResponse],status_code=201)
async def find_all(db:DbDependency):
    return item_cruds.find_all(db)

# @router.get("",response_model=list[ItemResponse])
# async def find_all():
#     return item_cruds.find_all()

@router.get("/{id}",response_model=ItemResponse)
async def find_by_id(db:DbDependency ,id: int=Path(gt=1)):
     found_item = item_cruds.find_by_id(db,id)
     if not found_item:
         raise HTTPException(status_code=404,detail="Item not found")
     return item_cruds.find_by_id(id)

@router.get("/")
async def find_by_name(db:DbDependency ,name:str=Query(min_length=3,max_length=10)):
     return item_cruds.find_by_name(db,name)

# @router.post("/")
# async def create(item_create:ItemCreate):
#     return item_cruds.create(item_create)

@router.put("/{id}", response_model=Optional[ItemResponse])
async def update(db:DbDependency,item_update:ItemUpdate,id:int =Path(gt=0)):
     return item_cruds.update(db,id,item_update)

@router.delete("/{id}",response_model=Optional[ItemResponse])
async def delete(db:DbDependency,id :int=Path(gt=0)):
     deleted_item =item_cruds.delete(db,id)
     if not deleted_item:
         raise HTTPException(status_code=404,detail="Item not deleted")
     return deleted_item

@router.post("/",response_model=ItemResponse,status_code=201)
async def create(db:DbDependency,item_create:ItemCreate):
    return item_cruds.create(db,item_create)