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
def build_distance_map(
        maze,
        user_cell, 
        max_search_units
): 
    distances = { 
        user_cell: 0
    }

    queue = deque(
        [user_cell]

    )

    while queue: 
        current_cell = queue.popleft()

        current_distance = ( distances[current_cell])

        # Don't search beyond the users max range 
        if current_distance >= max_search_units: 
            continue

        neighbors = get_reachable_neighbors(
            maze,
            current_cell
        )

        for neighbor in neighbors: 
            #BFS guarentees the first visit will be the shortest paath available
            if neighbor in distances: 
                continue
            distances[neighbor] = ( 
                current_distance+1 
            )
            queue.append(neighbor)

    return distances

###################################################
# STATION TRAVEL CALCULATIONS 
###################################################

def calculate_station_travel( 
        distance_units, 
        mpg, 
        miles_per_unit,
        minutes_per_unit
): 
    distance_miles = ( 
        distance_units * miles_per_unit
    )

    drive_minutes = ( 
        distance_units * minutes_per_unit
    )

    fuel_used_gallons = ( 
        distance_miles / mpg
    )

    return{ 
        "distance_units":  distance_units, 
        "distance_miles": distance_miles, 
        "drive_minutes": drive_minutes, 
        "fuel_used_gallons": fuel_used_gallons
    }


#################################################
# CALCULATE REAL STATION COSTS ^3^
#################################################

def calculate_station_cost(
        station_price, 
        fuel_remaining_gallons, 
        tank_capacity_gallons, 
        fuel_used_gallons
): 
    fuel_at_station = (fuel_remaining_gallons - fuel_used_gallons) 
    fuel_at_station = max(fuel_at_station,0)    # Safety against tiny floating point error 

    gallons_to_fill = ( 
        tank_capacity_gallons - fuel_at_station
    )

    purchase_cost = (gallons_to_fill * station_price)

    return{
        "fuel_at_station": fuel_at_station, 
        "gallons_to_fill": gallons_to_fill, 
        "purchase_cost": purchase_cost
    }

#################################################
# BUILDING AVAILABLE STATION LIST
#################################################

def get_available_stations ( 
        stations, 
        distance_map, 
        requested_fuel_type, 
        fuel_remaining_gallons, 
        tank_capacity_gallons, 
        mpg,
        miles_per_unit,
        minutes_per_unit
): 
    available_stations = []
    for station in stations: 
        station_cell = station.get("cell")

        # stations does not have a usable map location 
        if station_cell is None: 
            continue

        # Station is outside the reachable BFS area
        if station_cell not in distance_map: 
            continue
        

        fuel_key = get_station_fuel_key(station, requested_fuel_type)

        # Station doesnt carry the requested fuel
        if fuel_key is None: 
            continue

        station_price = ( 
            station["prices"][fuel_key]
        )


        distance_units = (distance_map[station_cell])

        travel_data = calculate_station_travel( 
            distance_units, 
            mpg, 
            miles_per_unit, 
            minutes_per_unit
        )

        # Vehicle needs to have enought fuel to get there 
        if (travel_data["fuel_used_gallons"] > fuel_remaining_gallons): 
            continue

        cost_data = calculate_station_cost(
            station_price, 
            fuel_remaining_gallons, 
            tank_capacity_gallons, 
            travel_data["fuel_used_gallons"]
        )


        available_stations.append( 
            {
                "station": station, 
                "fuel_type": fuel_key, 
                "price_per_gallon": station_price, 
                "distance_units": travel_data["distance_units"],
                "distance_miles":travel_data["distance_miles"],
                "drive_minutes": travel_data["drive_minutes"],
                "fuel_used_gallons": travel_data["fuel_used_gallons"],
                "fuel_at_station":cost_data["fuel_at_station"]
                "gallons_to_fill_"
            }
        )