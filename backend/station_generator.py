# What is this file going to do: 
# 1. Pick random maze cells 
# 2. Create Ranodm station names 
# 3. Create addresses 
# 4. Create fuel Types 
# 5. Create prices based off the average gas price inside of colorado springs 



import random 

# Randomly selects maze cells to act as gas stations ^-^ 
def generate_station_location(maze, station_count): 
    
    all_cells = [ 
        cell
        for row in maze.grid 
        for cell in row
    ]

    # This will prevent asking for more stations than cells 
    if station_count > len(all_cells): 
        station_count = len(all_cells)

    # Pick unique cells so two stations can't be at the same spot 
    station_cells = random.sample( 
        all_cells, 
        station_count
    )

    return station_cells