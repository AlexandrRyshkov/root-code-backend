from sqlalchemy.orm import relationship

from models.base import get_base
from models.railway_line_stations import RailwayLineStation

from sqlalchemy import Column, Integer
Base = get_base()


class RailwayLine(Base):
    __tablename__ = 'railway_lines'
    id = Column(Integer, primary_key=True)
    stations = relationship("RailwayLineStation")
