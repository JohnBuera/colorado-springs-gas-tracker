# This function will be used to filter the stations based on the fuel type.
def get_available_stations(stations,fuel_type):
     available_stations = [ 
          station 
          for station in stations
          if fuel_type in station["prices"]
     ]

     return available_stations

# Finds the cheapest station for a given fuel type from the available stations.
def find_cheapest_station(available_stations, fuel_type):
    if len(available_stations) == 0:
        return None
    return min( 
        available_stations,
        key=lambda station: station["prices"][fuel_type]
    )

# Finds the most expensive stations for a given fuel type from the available stations.
def find_most_expensive_station(available_stations, fuel_type):
    if len(available_stations) == 0:
        return None
    return max(
        available_stations,
        key=lambda station: station["prices"][fuel_type]
    )


# Calculates the average price for a given fuel type across all stations.
def calculate_average_price(fuel_type, Stations): 
    prices = [ 
        station["prices"][fuel_type] 
        for station in Stations 
        if fuel_type in station["prices"] 
    ]
    if len(prices) == 0:
        print(f"No stations found for fuel type: {fuel_type}")
        return None

    return round(sum(prices) / len(prices), 2)
    


