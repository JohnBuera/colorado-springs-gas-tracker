# Importing the different coluumn types being used when creating database tables 
from sqlalchemy import ( 
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    DateTime,
)

# This allows us to connect two python database models together 
from sqlalchemy.orm import relationship 

# Stores teh time when a gas price was recorded 
from datetime import datetime, UTC

# Importing the base class that we created inside of database.py
# Every database model will inherit from this base class
from database import Base

class Station(Base):
    # Setting the actual table name 
    __tablename__ = "stations"

    # UniqueID 
    id = Column(Integer, primary_key=True, index=True)

    # Station name
    name = Column(String, index=True, nullable = False) 

    # Address of the station 
    address = Column(String, unique=True, index=True, nullable = False)


    # Creating a relationship between this stations and all gas price records that will belong to it 
    prices = relationship("GasPrice", back_populates="station")

# This class will represent the gas_prices table 
class GasPrice(Base): 
    __tablename__ = "gas_prices"

    id = Column(Integer, primary_key=True, index=True)
    station_id = Column(Integer, ForeignKey("stations.id"), nullable=False )
    fuel_type = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    # Stores when this gas price was recorded
    observed_at = Column(DateTime(timezone=True), default=lambda:datetime.now(UTC))
    station = relationship("Station", back_populates="prices")
        