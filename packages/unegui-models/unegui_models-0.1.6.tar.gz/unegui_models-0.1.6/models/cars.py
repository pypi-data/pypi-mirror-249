from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base
from geoalchemy2 import Geography


class CarListing(Base):
    __tablename__ = 'car_listings'

    id = Column(Integer, primary_key=True)
    link = Column(Text)
    prepayment_amount = Column(Float)
    engine_capacity = Column(Float)
    transmission = Column(String)
    drive_type = Column(String)
    car_type = Column(String)
    color = Column(String)
    manufacture_year = Column(Integer)
    import_year = Column(Integer)
    engine_type = Column(String)
    interior_color = Column(String)
    leasing = Column(String)
    wheel_drive = Column(String)
    mileage = Column(Integer)
    condition = Column(String)
    doors = Column(Integer)
    description = Column(Text)
    monthly_payment = Column(Float)
    loan_term = Column(Integer)
    price = Column(Float)
    brand = Column(String)
    model = Column(String)
    province = Column(String)
    district = Column(String)
    khoroo = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    lat = Column(Float)
    long = Column(Float)
    location = Column(Geography(geometry_type='POINT', srid=4326))

    images = relationship("CarImage", back_populates="car_listing")

class CarImage(Base):
    __tablename__ = 'car_images'

    id = Column(Integer, primary_key=True)
    car_listing_id = Column(Integer, ForeignKey('car_listings.id'))
    img_url = Column(Text)

    car_listing = relationship("CarListing", back_populates="images")