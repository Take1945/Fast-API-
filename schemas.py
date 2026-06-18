from database import Base
from sqlalchemy import Column,Integer,String,Enum,DateTime
from datetime import datetime
from models import ItemStatus

class Item(Base):
    
 __tablename__= "items"

 id = Column(Integer,primary_key=True,index=True)
 name=Column(String,nullable=False)
 price=Column(Integer,nullable=False)
 description=Column(String,nullable=True)
 status =Column(Enum(ItemStatus),nullable=False,default=ItemStatus.ON_SALE)
 created_at =Column(DateTime, default=datetime.now())
 update_at = Column(DateTime,default=datetime.now, onupdate=datetime.now())