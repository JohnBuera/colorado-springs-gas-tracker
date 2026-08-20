import random 
from pathfinding import find_shortest_path
from station_generator import generate_stations
# Represents the individual cells in the maze
class Cell: 
    def __init__(self, x, y): 
        self.x = x 
        self.y = y 
        self.walls = {'N': True, 'S': True, 'E': True, 'W': True}  # All walls are initially present
        self.visited = False  # To track if the cell has been visited during maze generation


# Representing the maze itself 
class Maze: 
    def __init__(self, width, height): 
        self.width = width 
        self.height = height 
        self.grid = [
            [Cell(x, y) for x in range(width)] 
            for y in range(height)]  # Create a grid of cells

    # Returning the cell at a particular xy position
    def get_cell(self, x, y): 
        if x < 0 or x >= self.width: 
            return None
        if y < 0 or y >= self.height:
            return None
        return self.grid[y][x]  # Return the cell at the specified position

    # Finding the neighboring cells that have not been visited yet 
    def get_unvisited_neighbors(self,cell): 
        neighbors = [] 

        #North 
        north = self.get_cell(cell.x, cell.y - 1)
        if north is not None and not north.visited: 
            neighbors.append(("N", north, "S"))

        # South
        south = self.get_cell(cell.x, cell.y + 1)
        if south is not None and not south.visited: 
            neighbors.append(("S", south, "N"))

        # East
        east = self.get_cell(cell.x + 1, cell.y)
        if east is not None and not east.visited: 
            neighbors.append(("E", east, "W"))
        # West
        west = self.get_cell(cell.x - 1, cell.y)
        if west is not None and not west.visited: 
            neighbors.append(("W", west, "E"))

        return neighbors  # Return the list of unvisited neighbors


    # Removing walls between the neighboring cells 
    def remove_walls(self, current_cell, next_cell, direction, opposite_direction): 
        # Basic explanation of how this works: 
        # If there is a wall to the east but then a new cell is generated there the wall betweent the two cells will be removed 
        current_cell.walls[direction] = False  # Remove the wall in the specified direction for the current cell 
        next_cell.walls[opposite_direction] = False  # Remove the wall in the opposite direction for the next cell

    # Generating our maze using randomized the depth-first search algorithm 
    def generate_maze(self): 
        start_x = random.randrange(self.width)  # Randomly select a starting x-coordinate
        start_y = random.randrange(self.height)  # Randomly select a starting y-coordinate

        current_cell = self.grid[start_y][start_x]  # Get the starting cell from the grid
        current_cell.visited = True  # Mark the starting cell as visited

        stack = []

        while True: 
            # Find the locations that have not been visited 
            neighbors = self.get_unvisited_neighbors(current_cell)

            if neighbors:
                # If there is somewhere new to go then it will remember where we are 
                stack.append(current_cell)

                # Randomly choose which neighboring location to visit
                direction, next_cell, opposite_direction = random.choice(neighbors)

                # Remove the walls 
                self.remove_walls(current_cell, next_cell, direction, opposite_direction)


                # Moving into a new cell
                current_cell = next_cell 

                # Recording we have been here so we don't regenerate the same cell
                current_cell.visited = True 

            # To where if we hit a random dead end we will go backwards til an unexplored neighbor is found 
            elif stack: 
                current_cell = stack.pop()

            # No unvisted cells remain
            else: 
                break 
    # Checks whether every cell in the maze can be reached.
    def is_fully_connected(self):

        start_cell = self.grid[0][0]

        visited = set()
        stack = [start_cell]

        while stack:

            current_cell = stack.pop()

            position = (
                current_cell.x,
                current_cell.y
            )

            if position in visited:
                continue

            visited.add(position)

            # Check every open direction.
            if not current_cell.walls["N"]:
                north = self.get_cell(
                    current_cell.x,
                    current_cell.y - 1
                )

                if north is not None:
                    stack.append(north)

            if not current_cell.walls["S"]:
                south = self.get_cell(
                    current_cell.x,
                    current_cell.y + 1
                )

                if south is not None:
                    stack.append(south)

            if not current_cell.walls["E"]:
                east = self.get_cell(
                    current_cell.x + 1,
                    current_cell.y
                )

                if east is not None:
                    stack.append(east)

            if not current_cell.walls["W"]:
                west = self.get_cell(
                    current_cell.x - 1,
                    current_cell.y
                )

                if west is not None:
                    stack.append(west)

        total_cells = self.width * self.height

        return len(visited) == total_cells


        # Prints a version of the maze inside of the terminal 
        # TESTING PURPOSES ONLY THE FRONT END WILL GENERATE THIS IN THE FUTURE 
    def print_maze(self):

        # Draw the top wall
        print("+" + "---+" * self.width)

        station_cells = generate_station_location( 
            maze, station_count= 10 
        )
        print("Gas Station Locations: ")
        for station_cell in station_cells: 
            print(
                station_cells.x 
                station_cells.y 
            )
        for row in self.grid:

            # Start the left side of this row
            middle_line = "|"
            bottom_line = "+"
            # Go through every cell in THIS row
            for cell in row:
                # Draw the inside of the cell
                middle_line += "   "

                # Draw the east wall if it exists
                if cell.walls["E"]:
                    middle_line += "|"
                else:
                    middle_line += " "

                # Draw the south wall if it exists
                if cell.walls["S"]:
                    bottom_line += "---+"
                else:
                    bottom_line += "   +"

            # Print this completed row
            print(middle_line)
            print(bottom_line)


# This code willonly runs when maze.py itself is executed 
if __name__ == "__main__": 
    # Starts samll while testing 
    maze = Maze( 
        width = 20, 
        height = 20
    )

    maze.generate_maze()
    start_cell = maze.get_cell(0,0)
    end_cell = maze.get_cell(19,19)

    stations = generate_stations(
    maze,
    station_count=10
    )

    for station in stations:
        print(station)



    path = find_shortest_path( 
        maze, 
        start_cell, 
        end_cell
    )
    if path is None: 
        print("ERROR: No path was found")
    else: 
        print(f"Path Length: {len(path) -1}")
        print(path)
    maze.print_maze()
    if maze.is_fully_connected(): 
        print("Maze is fully connected.")
    else: 
        print("ERROR: Maze contains unreachable cells ") 