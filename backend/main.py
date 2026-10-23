# Author: John Buera 
# Start Date: 2026-08-17 

# This will be the backend for the Colorado Springs Gas Tracker. 
# It will be a FastAPI application that will serve as an API for the frontend to consume.
# First we store the station locations and stats in a list of dictionaries inside of another file called data.py. 
# Each dictionary will contain the station name, prices for each fuel type, and the address of the station.
# There will be functions that are able to: 
#  return the latest price for each fuel type, as well as the average price, cheapest station, and most expensive station for each fuel type.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.database import engine
from backend import models, services
from backend.data import Stations

app = FastAPI()

# This lets our frontend get prices from the backend on a different port.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Looks at the models "Station" and "GasPrice"
models.Base.metadata.create_all(bind=engine)


@app.get("/")

def read_root(): 
    return { 
        "message": "Colorado Springs Gas Tracker is running"
    } 

# Adding an endpoint to check the status of the latest price 
@app.get("/prices/latest")
def get_latest_price():
    return Stations 

@app.get("/prices/stats/{fuel_type}")
def get_price_stats(fuel_type: str):

    # This section is going to help more with looking up the fuel and normalizing the text 
    fuel_lookup = {
        "regular": "Regular",
        "midgrade": "MidGrade",
        "premium": "Premium",
        "diesel": "Diesel"
    }

    normalized_fuel_type = fuel_lookup.get(fuel_type.lower())


    if normalized_fuel_type is None:
        return {"error": f"Invalid fuel type: {fuel_type}. Valid options are: Regular, MidGrade, Premium, Diesel."}

    # Now we will filter the stations to only include those that have the specified fuel type available.
    available_stations = services.get_available_stations(Stations, normalized_fuel_type)

    if len (available_stations) == 0:
        return {"error": f"No stations found for fuel type: {normalized_fuel_type}"}
    
    average_price = services.calculate_average_price(available_stations, normalized_fuel_type) 
    cheapest_station = services.find_cheapest_station(available_stations, normalized_fuel_type)
    most_expensive_station = services.find_most_expensive_station(available_stations, normalized_fuel_type)

    return {
        "fuel_type": normalized_fuel_type,
        "average_price": average_price,
        "cheapest_station": {
            "station": cheapest_station["station"],
            "price": cheapest_station["prices"][normalized_fuel_type],
            "address": cheapest_station["address"]
        },
        "most_expensive_station": {
            "station": most_expensive_station["station"],
            "price": most_expensive_station["prices"][normalized_fuel_type],
            "address": most_expensive_station["address"]
        }
    }