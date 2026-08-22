# RESPONSIBILITES OF THIS FILE: 
# 1. Takes the users locations and vehicle info 

# 2. Figures out all the available stations according to the users requirements 

# 3. Filters through our gas station by: 
#       - Fuel Type 
#       - Drive time
#       - Remaining fuel 
#       - Gas mileage calculations 

# 4. We will use the vehicles gas mileage (MPG) to calculate how much fuel 
#       be used to get to the gas station 
#           - Note: For cars with very low gas mileage this could be an important factor 

# 5. Calculates the real cost of choosing each station 

 # 6. Compares the cheapes overall choice to the nearest station 

# 7. Determines whether driving farther for cheaper gas will realistically save money 

# 8. Return the best station and the shortest route there

from collections import deque
import math 

from pathfinding import get_reachable_neighbors

#------------------------------------------------------
# FUEL TYPE NORMALIZATION 
#------------------------------------------------------
def normalize_fuel_type(fuel_type): 
    return"".join(
        character
        for character in fuel_type.lower()
        if character.isalnum()
    )

# Finds teh actual key inside a station's prices dictionary 
def get_station_fuel_key(
        station, 
        requested_fuel_type
): 
    requested_fuel = normalize_fuel_type(requested_fuel_type)
    prices = station.get("prices", {})

    for fuel_name in prices: 
        if normalize_fuel_type(fuel_name) == requested_fuel_type: 
            return fuel_name

    # Just incase the station doesnt carry the requested fuel 
    return None


#-----------------------------------------
# USER INPUT VALIDATION
#-----------------------------------------

# Ensures that the values supplied by the user make sense before the optimizer begins calculating

def validate_user_inputs( 
        user_cell, 
        fuel_remaining_gallons, 
        tank_capacity_gallons, 
        mpg, 
        max_drive_minute, 
        miles_per_unit, 
        minutes_per_unit
): 
    if user_cell is None: 
        raise ValueError( 
            "The user location must be a valid maze cell"
        )

    if tank_capacity_gallons <= 0: 
        raise ValueError( 
            "Tank capacity must be greater than 0"
        )

    if fuel_remaining_gallons < 0: 
        raise ValueError(
            "Fuel remaining can not be negative"
        )

    if fuel_remaining_gallons > tank_capacity_gallons: 
        raise ValueError("Fuel Remaining can not exceed the tank's capacity")

    if mpg <= 0: 
        raise ValueError("MPG must be greater than 0")

    if max_drive_minute < 0: 
        raise ValueError("Maximum drive time cannot be negative")

    if miles_per_unit <= 0:
        raise ValueError(
            "Miles per maze unit must be greater than zero."
        )

    if minutes_per_unit <= 0:
        raise ValueError(
            "Minutes per maze unit must be greater than zero."
        )

#----------------------------------
# MAX SEARCH RANGE 
#----------------------------------

# Limits: 
# 1. How far is this user willing to drive 
# 2. How far can the vehicle physically travel with the current fuel remaining 

# Whichever limit is smaller becomes the limiting range 

def calcultate_max_search_units(
        fuel_remaining_gallons, 
        mpg, 
        max_drive_minutes, 
        miles_per_unit, 
        minutes_per_unit
): 
    # This will convert the maximum drive time into the movement units 
    max_units_by_time = (
        max_drive_minutes / minutes_per_unit
    )

    fuel_range_miles = ( 
        fuel_remaining_gallons * mpg
    )

    max_units_by_fuel = ( 
        fuel_range_miles / miles_per_unit
    )

    max_search_units = min(max_units_by_time, max_units_by_fuel)


    return math.floor(max_search_units)


#----------------------------------------
# BUILD DISTANCE MAP
#----------------------------------------

# Runs a single Breadth-First Search from the users location 
# Distacnes store the shortest route to every discovered cell