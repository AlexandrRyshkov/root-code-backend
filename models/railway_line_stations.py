from models.base import get_base

Base = get_base()
from sqlalchemy import Column, Integer, ForeignKey


class RailwayLineStation(Base):
    __tablename__ = "railway_line_stations"
    railway_line_id = Column(ForeignKey("railway_lines.id"), primary_key=True)
    start_station_id = Column(ForeignKey("stations.id"), primary_key=True)
    end_station_id = Column(ForeignKey("stations.id"), primary_key=True)
    stop_number = Column(Integer)
