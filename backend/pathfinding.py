# deque os a double-ended qeue 
# BFS will use a a qeue so that we can explore the maze 
from collections import deque 


# Returns every neighboring ells that can be reached from the current cell 
def get_reachable_neighbors(maze,cell): 
    neighbors = [] 

    # If the north wall is open we can move north 
    if not cell.walls["N"]: 
        north = maze.get_cell(cell.x, cell.y-1) 

        if north is not None: 
            neighbors.append(north)

    # South 
    if not cell.walls["S"]: 
        south = maze.get_cell(cell.x,cell.y + 1 )

        if south is not None: 
            neighbors.append(south)

    # East
    if not cell.walls["E"]: 
        east = maze.get_cell(cell.x + 1, cell.y)

        if east is not None: 
            neighbors.append(east)

    # West 
    if not cell.walls["W"]: 
        west = maze.get_cell(cell.x-1, cell.y)

        if west is not None:
            neighbors.append(west)

    return neighbors 


# Using Breadth-First Search to find the shortest route between the two cells within the maze 
def find_shortest_path(maze, start_cell, end_cell): 


    # Storing the start position once so we can reuse it later on ^-^ 
    start_position = (
        start_cell.x, 
        start_cell.y
    )
    # This is where the unexplored cells will be stored
    queue = deque([start_cell])

    # Stores every cell already discovered 
    visited = { 
        start_position
    }


    # Previous remembers the path taken to each cell 
    previous = {}

    while queue: 
        current_cell = queue.popleft()

        # Once the destination is reached, stop searching :3 
        if current_cell is end_cell: 
            break 
        for neighbor in get_reachable_neighbors( 
            maze, 
            current_cell
        ): 
            neighbor_position = ( 
                neighbor.x, 
                neighbor.y 
            )

            # Ignore the cells already discovered 
            if neighbor_position in visited: 
                continue 
            visited.add(neighbor_position)

            # Logs the path made to reach the neighbor 
            previous[neighbor_position] = ( 
                current_cell.x, 
                current_cell.y
            )
            queue.append(neighbor)

    end_position = ( 
        end_cell.x, 
        end_cell.y
    )


    # IF BFS never reached the destination that means no valid path exists 
    if end_position not in visited: 
        return None

    # Rebuilds the route backwards 
    path = []

    current_position = end_position

    while current_position != start_position: 
        path.append(current_position)
        current_position = previous[ 
            current_position
        ]
    path.append(start_position)


    # Reversing the path constructed before returning it 
    path.reverse()

    return path