from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base
from geoalchemy2 import Geography

class Properties(Base):
    __tablename__ = "properties"
    id = Column(Integer, primary_key=True)
    link = Column(String)
    rooms = Column('rooms', Integer)
    garage = Column('garage', String)
    balcony_number = Column('balconyNumber', Integer)
    area = Column('area', Float)
    location = Column('location', String)
    door = Column('door', String)
    window = Column('window', String)
    floor = Column('floor', String)
    window_number = Column('windowNumber', Integer)
    building_floor = Column('buildingFloor', Integer)
    which_floor = Column('whichFloor', Integer)
    commission_year = Column('commissionYear', Integer)
    leasing = Column('leasing', String)
    progress = Column('progress', String)
    price = Column('price', Float)
    province = Column('province', String)
    district = Column('district', String)
    khoroo = Column('khoroo', String)
    property_type = Column('propertyType', String)
    sell_type = Column('sellType', String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    lat = Column(Float)
    long = Column(Float)
    location = Column(Geography(geometry_type='POINT', srid=4326))

    images = relationship("PropertyImage", back_populates="property")

class PropertyImage(Base):
    __tablename__ = 'property_images'

    id = Column(Integer, primary_key=True)
    property_id = Column(Integer, ForeignKey('properties.id'))
    img_url = Column(Text)

    property = relationship("Properties", back_populates="images")
