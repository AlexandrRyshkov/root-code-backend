from models.base import get_base

Base = get_base()
from sqlalchemy import Column, Integer, String, Float


class Station(Base):
    __tablename__ = 'stations'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    esr_code = Column(Integer)
    railroad_code = Column(Integer)
    okato_name = Column(String)
    x = Column(Float)
    y = Column(Float)
