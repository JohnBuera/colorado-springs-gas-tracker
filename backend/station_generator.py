# What this file is responsible for:
# 1. Pick random maze cells
# 2. Create random station names
# 3. Create random addresses
# 4. Create fuel types
# 5. Generate prices within a realistic range
# 6. Return a list of complete gas station objects


import random


# Randomly selects maze cells to act as gas stations.
def generate_station_locations(maze, station_count):

    # Flatten the 2D maze grid into one list of Cell objects.
    all_cells = [
        cell
        for row in maze.grid
        for cell in row
    ]

    # Prevent asking for more gas stations than there are maze cells.
    if station_count > len(all_cells):
        raise ValueError(
            "Station count cannot be greater than the number of maze cells."
        )

    # random.sample() selects unique cells.
    # This guarantees two gas stations will not occupy the same maze cell.
    station_cells = random.sample(
        all_cells,
        station_count
    )

    return station_cells


# Generates a random station name.
def generate_station_name(station_number):

    station_prefixes = [
        "Fuel Stop",
        "Quick Fuel",
        "Road Runner Gas",
        "Mountain Fuel",
        "Front Range Gas",
        "Highway Fuel",
        "Peak Petroleum"
    ]

    prefix = random.choice(station_prefixes)

    return f"{prefix} {station_number}"


# Generates a random fake street address.
def generate_address():

    address_number = random.randint(
        100,
        9999
    )

    street_names = [
        "Main St",
        "Pine St",
        "Oak Ave",
        "Maple St",
        "Cedar Rd",
        "Cascade Ave",
        "Nevada Ave",
        "Academy Blvd",
        "Union Blvd",
        "Austin Bluffs Pkwy"
    ]

    street_name = random.choice(
        street_names
    )

    return f"{address_number} {street_name}"


# Generates a regular gas price.
#
# Most prices stay within a similar range.
# Later we can base this on a configurable city-wide average.
def generate_regular_price():

    regular_price = random.uniform(
        2.90,
        3.60
    )

    return round(
        regular_price,
        2
    )


# Generates all fuel prices for one gas station.
def generate_fuel_prices():

    # Generate Regular first because the other prices
    # will be based on it.
    regular_price = generate_regular_price()

    # MidGrade is usually somewhat more expensive than Regular.
    midgrade_price = (
        regular_price
        + random.uniform(
            0.20,
            0.45
        )
    )

    # Premium is generally the most expensive gasoline grade.
    premium_price = (
        regular_price
        + random.uniform(
            0.45,
            0.80
        )
    )

    # Diesel can vary more independently.
    diesel_price = (
        regular_price
        + random.uniform(
            0.10,
            0.60
        )
    )

    return {
        "Regular": round(
            regular_price,
            2
        ),

        "MidGrade": round(
            midgrade_price,
            2
        ),

        "Premium": round(
            premium_price,
            2
        ),

        "Diesel": round(
            diesel_price,
            2
        )
    }


# Creates one complete gas station object.
def create_station(
    station_cell,
    station_number
):

    station = {

        # Randomly generated station name.
        "name": generate_station_name(
            station_number
        ),

        # Stores where this station exists inside the maze.
        #
        # The frontend can later use this to draw the station.
        "cell": (
            station_cell.x,
            station_cell.y
        ),

        # Randomly generated fake address.
        "address": generate_address(),

        # Generate all fuel prices.
        "prices": generate_fuel_prices()
    }

    return station


# Generates an entire list of gas stations.
def generate_stations(
    maze,
    station_count
):

    # First select unique cells for the stations.
    station_cells = generate_station_locations(
        maze,
        station_count
    )

    stations = []

    # Turn every selected maze cell into a full gas station.
    for index, station_cell in enumerate(
        station_cells,
        start=1
    ):

        station = create_station(
            station_cell,
            index
        )

        stations.append(
            station
        )

    return stations