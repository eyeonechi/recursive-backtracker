DIRECTIONS = (U, R, D, L) = (0, 1, 2, 3)
from collections import defaultdict

###############################################################################

def is_valid_maze(maze):
    """Returns True if the maze is valid, False otherwise."""
    # Asserts each constraint and returns False if any are not met.
    if not constraint_0(maze):
        return(False)
    if not constraint_1(maze):
        return(False)
    if not constraint_2(maze):
        return(False)
    if not constraint_3(maze):
        return(False)
    if not constraint_4(maze):
        return(False)
    if constraint_5(maze) is False:
        return(False)
    if constraint_6(maze) is False:
        return(False)
    if constraint_7(maze) is False:
        return(False)
    if constraint_8a(maze) is False:
        return(False)
    if constraint_8b(maze) is False:
        return(False)
    return(True)


def constraint_0(maze):
    """Checks if maze is empty."""
    return(False if len(maze) == 0 else True)


def constraint_1(maze):
    """Checks that all rows are of equal length and not empty."""
    # Appends False to a list each time a row is of unequal length.
    return(False if False in [False for row in maze if len(row) < 1 or
                              len(row) != len(maze[0])] else True)


def constraint_2(maze):
    """Checks for unique entry point in the first row."""
    # Appends True to a list each time an opening is detected.
    return(False if len([True for cell in maze[0]
                         if cell[U] is True]) != 1 else True)


def constraint_3(maze):
    """Checks for unique exit point in the last row."""
    # Appends True to a list each time an exit is detected.
    return(False if len([True for cell in maze[-1]
                         if cell[D] is True]) != 1 else True)


def constraint_4(maze):
    """Checks for openings out of the sides of the maze."""
    # Appends False to a list each time a side opening is found.
    return(False if False in [False for row in maze if row[0][L]
                              is True or row[-1][R] is True] else True)


def constraint_5(maze):
    """Checks that each cell is reachable from an adjacent cell."""
    # Asserts that each cell is not a tuple of four Falses.
    for row in maze:
        for cell in row:
            list_5 = [False for direction in cell if direction is False]
            if len(list_5) == 4:
                return(False)


def constraint_6(maze):
    """Checks for at least one downward path to the succeeding row."""
    # Appends True to a list each time a downward path is found.
    for row in maze:
        list_6 = [True for cell in row if cell[D] is True]
        if len(list_6) == 0:
            return(False)


def constraint_7(maze):
    """Checks for at least one upward path to the preceeding row."""
    # Appends True to a list each time an upward path is found.
    for row in maze:
        list_7 = [True for cell in row if cell[U] is True]
        if len(list_7) == 0:
            return(False)


def constraint_8a(maze):
    """Checks for symmetry in Boolean values to the right of cells."""
    # Appends False to a list if sides of each cell and its right
    # adjacent cell do not correspond to each other.
    return(False if len([False for row in maze for i in range(len(row) - 1)
                         if row[i][R] is True and row[i + 1][L]
                         is False]) > 0 else True)

def constraint_8b(maze):
    """Checks for symmetry in Boolean values to the left of cells."""
    # Appends False to a list if sides of each cell and its right
    # adjacent cell do not correspond to each other.
    return(False if len([False for row in maze for i in
                         range(0, len(row)) if row[i][L] is True
                         and row[i - 1][R] is False]) > 0 else True)

###############################################################################

def get_entry_point(maze):
    """Returns a 2-tuple of integers identifying the unique entry point"""
    # Indexes the first row of the maze and asserts 'UP' direction is True.
    return(0, (maze[0].index([cell for cell in maze[0] if cell[U]][0])))

###############################################################################

def get_exit_point(maze):
    """Returns a 2-tuple of integers identifying the unique exit point."""
    # Indexes the last row of the maze and asserts True 'DOWN' direction.
    return(len(maze) - 1, (maze[-1].index([cell for cell in maze[-1]
                                           if cell[D]][0])))

###############################################################################

def visualise_maze(maze):
    """Returns a string-based representation of the maze."""
    # Top edge of the maze as a single underscore character string.
    visual = '_'

    # Top edge of the first row of the maze made up of two spaces for
    # entry point(s), two underscore characters otherwise.
    for cell in maze[0]:
        visual += ('  ' if cell[U] else '__')
    visual += '\n'

    # Each row corresponds to each line in the output after the top edge,
    # terminated by newline character.
    for row in maze:
        # Pipe character for left wall of the row.
        visual += ('|' if not row[0][L] else '')

        # Marks paths down the maze with single spaces.
        # Marks cells with both path downwards and right with two spaces,
        # single underscore otherwise.
        # Marks cells with only right direction with single underscore
        # followed by single space.
        # Marks paths to the right of the cell with pipe character.
        for cell in row:
            visual += (' ' if cell[D] and not cell[R] else '')
            visual += ('  ' if cell[D] and cell[R] else '')
            visual += ('_' if not cell[D] and not cell[R] else '')
            visual += ('_ ' if not cell[D] and cell[R] else '')
            visual += ('|' if cell[R] is False else '')
        visual += '\n'

    return(visual)

###############################################################################

def solve_maze(maze):
    """Returns the path through the maze (if available) using an
    algorithm where each cell visited is traversed via possible
    paths based on cell configuration, backtracking steps to entry
    point when encountered with a dead end. Algorithm stops when exit
    point is found, or when back at entry point with all paths traversed.
    Algorithm is notably similar to Tremaux's Algorithm: http://en.wiki
    pedia.org/wiki/Maze_solving_algorithm#Tr.C3.A9maux.27s_algorithm"""
    # Dictionary to map each cell to its coordinates.
    maze_dict = defaultdict(tuple)
    # List containing coordinates to the solution of the maze.
    maze_list = []
    # Locates the unique entry and exit point of the maze.
    entry_point = get_entry_point(maze)
    exit_point = get_exit_point(maze)
    # 2-tuple of integers, starting at the entry point.
    coordinate = entry_point
    # Determines which way to traverse the maze.
    direction = ''
    # List containing directions possible to move from the entry point.
    direction_list = []

    # Matches each cell in the maze to its coordinates.
    for row_num, row in enumerate(maze):
        for cell_num, cell in enumerate(row):
            maze_dict[(row_num, cell_num)] = cell

    # Appends possible directions to direction_list and determines
    # the initial direction to traverse from the entry point.
    if entry_point:
        if maze_dict[entry_point][R] is True:
            direction = 'R'
            direction_list.append('R')
        if maze_dict[entry_point][D] is True:
            direction = 'D'
            direction_list.append('D')
        if maze_dict[entry_point][L] is True:
            direction = 'L'
            direction_list.append('L')

    # Continuously traverses the maze while under a while loop.
    while maze_dict.keys():

        # Case where current coordinate is the entry point.
        if coordinate == entry_point:
            # Inverts the direction corresponding to direction explored.
            if direction not in direction_list:
                if direction == 'U':
                    direction = 'D'
                elif direction == 'R':
                    direction = 'L'
                elif direction == 'D':
                    direction = 'U'
                elif direction == 'L':
                    direction = 'R'

            # Returns None when back at entry point and all directions
            # have been explored.
            if len(maze_list) > 0:
                direction_list.remove(direction)
                maze_list = []
                if len(direction_list) == 0:
                    return(None)
                direction = direction_list[0]

        # Case where algorithm has found the exit point.
        if coordinate == exit_point:
            # Appends exit point into and returns the solution.
            if len(maze_list) == 0:
                maze_list.append(exit_point)
            elif maze_list[-1] != exit_point:
                maze_list.append(exit_point)
            return(maze_list)

        # Algorithm tries to traverse to the'Right'.
        if direction is 'R':
            # Checks if it is possible to traverse right from the cell.
            if maze_dict[coordinate][R] is True:
                maze_list.append(coordinate)
                coordinate = (coordinate[0], coordinate[1] + 1)

                # Checks if right adjacent cell can be traversed.
                if coordinate in maze_dict.keys():
                    # Once within right cell, tries to traverse in a
                    # direction possible based on cell configuration.
                    if (maze_dict[coordinate][U] is False or
                       maze_dict[coordinate][D] is False):
                        direction = 'R'
                    if (maze_dict[coordinate][D] is False and
                       maze_dict[coordinate][R] is False):
                        direction = 'U'
                    if (maze_dict[coordinate][U] is False and
                       maze_dict[coordinate][R] is False):
                        direction = 'D'

                    # Case where dead end is found going right.
                    if (maze_dict[coordinate][U] is False and
                       maze_dict[coordinate][R] is False and
                       maze_dict[coordinate][D] is False):
                        direction = 'L'
                        coordinate = (coordinate[0], coordinate[1] - 1)
                        maze_list.remove(coordinate)
                else:
                    direction = 'U'
                    coordinate = (coordinate[0], coordinate[1] - 1)
            else:
                direction = 'D'

        # Algorithm tries to traverse to the 'Left'.
        if direction is 'L':
            # Checks if it is possible to traverse right from the cell.
            if maze_dict[coordinate][L] is True:
                maze_list.append(coordinate)
                coordinate = (coordinate[0], coordinate[1] - 1)
                direction = 'U'

                # Checks if left adjacent cell can be traversed.
                if coordinate in maze_dict.keys():
                    # Once within left cell, tries to traverse in a
                    # direction possible based on cell configuration.
                    if (maze_dict[coordinate][D] is False or
                       maze_dict[coordinate][U] is False):
                        direction = 'L'
                    if (maze_dict[coordinate][D] is False and
                       maze_dict[coordinate][L] is False):
                        direction = 'U'
                    if (maze_dict[coordinate][U] is False and
                       maze_dict[coordinate][L] is False):
                        direction = 'D'

                    # Case where dead end is found going left.
                    if (maze_dict[coordinate][D] is False and
                       maze_dict[coordinate][L] is False and
                       maze_dict[coordinate][U] is False):
                        direction = 'R'
                        coordinate = (coordinate[0], coordinate[1] + 1)
                        maze_list.remove(coordinate)
                else:
                    coordinate = (coordinate[0], coordinate[1] + 1)
                    direction = 'D'
            else:
                direction = 'U'

        # Algorithm tries to traverse 'Down'.
        if direction is 'D':
            # Checks if it is possible to traverse downwards.
            if maze_dict[coordinate][D] is True:
                maze_list.append(coordinate)
                coordinate = (coordinate[0] + 1, coordinate[1])

                # Checks if cell below can be traversed.
                if coordinate in maze_dict.keys():
                    # Once within cell below, tries to traverse in a
                    # direction possible based on cell configuration.
                    if (maze_dict[coordinate][R] is False or
                       maze_dict[coordinate][L] is False):
                        direction = 'D'
                    if (maze_dict[coordinate][R] is False and
                       maze_dict[coordinate][D] is False):
                        direction = 'L'
                    if (maze_dict[coordinate][L] is False and
                       maze_dict[coordinate][D] is False):
                        direction = 'R'

                    # Case where dead end is found going downwards.
                    if (maze_dict[coordinate][R] is False and
                       maze_dict[coordinate][D] is False and
                       maze_dict[coordinate][L] is False):
                        direction = 'U'
                        coordinate = (coordinate[0] - 1, coordinate[1])
                        maze_list.remove(coordinate)
                else:
                    direction = 'R'
                    coordinate = (coordinate[0] - 1, coordinate[1])
            else:
                direction = 'L'

        # Algorithm tries to traverse 'Up'.
        if direction is 'U':
            # Checks if it is possible to traverse upwards.
            if maze_dict[coordinate][U] is True:
                maze_list.append(coordinate)
                coordinate = (coordinate[0] - 1, coordinate[1])

                # Checks if cell above can be traversed.
                if coordinate in maze_dict.keys():
                    if (maze_dict[coordinate][L] is False or
                       maze_dict[coordinate][R] is False):
                        direction = 'U'
                    if (maze_dict[coordinate][L] is False and
                       maze_dict[coordinate][U] is False):
                        direction = 'R'
                    if (maze_dict[coordinate][R] is False and
                       maze_dict[coordinate][U] is False):
                        direction = 'L'

                    # Case where dead end is found going upwards.
                    if (maze_dict[coordinate][L] is False and
                       maze_dict[coordinate][U] is False and
                       maze_dict[coordinate][R] is False):
                        direction = 'D'
                        coordinate = (coordinate[0] + 1, coordinate[1])
                        maze_list.remove(coordinate)
                else:
                    direction = 'L'
                    coordinate = (coordinate[0] + 1, coordinate[1])
            else:
                direction = 'R'

###############################################################################

def shortest_paths(maze, point):
    """Finds the shortest acyclic path(s) which passes through 'point'
    using an algorithm which uses a 'brute-force' method to determine
    every possible combination of moves from the starting point. The
    iterative part of the algorithm uses the cell configuration to
    determine which direction to traverse, and appends multiple
    'direction-coordinate lists' in the instance a cell has more than
    one direction possible to be traversed. The recursive part of the
    algorithm triggers when it repeatedly calls a separate function
    'remove_paths' when encountered with one instance of the exit point
    or a dead end. Said function will cause the algorithm to backtrack
    to the last junction traversed to move in another direction.
    Algorithm is possibly similar to the Recursive Algorithm: http://en.
    wikipedia.org/wiki/Maze_solving_algorithm#Recursive_algorithm
    NOTE: I am sincerely sorry for the length of this code..."""
    # Locates the unique entry and exit point of the maze.
    entry_point = get_entry_point(maze)
    exit_point = get_exit_point(maze)
    # Dictionary to map each cell to its coordinates.
    maze_dict = maze_dictionary(maze)
    # Dictionary of all possible cell configurations.
    path_dict = defaultdict(tuple)
    path_dict = path_dictionary(path_dict)
    # 2-tuple of integers, starting at the entry point.
    coordinate = entry_point
    # Determines which way to traverse the maze.
    direction = ''
    # List containing directions possible to move from the entry point.
    direction_list = []
    # List of coordinates being traversed.
    path_list = []
    # List containing coordinates of cells visited.
    visit_list = []
    # List containing coordinates of each the solution of the maze.
    route_list = []
    # List of all possible solutions of the maze.
    maze_list = []
    # List of acyclic paths which go through point.
    through_list = []
    # List of shortest acyclic paths which go through point.
    shortest_list = []

    # Appends possible directions to direction_list and determines
    # the initial direction to traverse from the entry point.
    if entry_point:
        if maze_dict[entry_point][R] is True:
            direction = 'R'
            direction_list.append('R')
        if maze_dict[entry_point][D] is True:
            direction = 'D'
            direction_list.append('D')
        if maze_dict[entry_point][L] is True:
            direction = 'L'
            direction_list.append('L')

    # Appends list of direction and coordinates possible to be
    # traversed from the entry point.
    for direction in direction_list:
        path_list.append([direction, entry_point])
        visit_list.append([direction, entry_point])

    # Continuously traverses the maze while under a while loop.
    while coordinate in maze_dict.keys():
        # Algorithm traverses 'Up'.
        if direction is 'U':
            # Case where current coordinate is the entry point.
            if coordinate == entry_point:
                # Asserts whether coordinate has been traversed.
                if coordinate in visit_list:
                    # Backtracks to the last junction encountered.
                    (path_list, visit_list
                     ) = remove_paths(path_list, visit_list)
                    if len(path_list) == 0:
                        break
                    while (len(path_list) > 0 and
                           type(path_list[-1]) is tuple):
                        (path_list, visit_list
                         ) = remove_paths(path_list, visit_list)
                    # Breaks if no directions left to traverse
                    if len(path_list) == 0:
                        break
                    coordinate = path_list[-1][1]
                    direction = path_list[-1][0]
                    path_list.append(coordinate)
                    visit_list.append(coordinate)
                    if direction is 'U':
                        coordinate = (coordinate[0] - 1, coordinate[1])
                    elif direction is 'R':
                        coordinate = (coordinate[0], coordinate[1] + 1)
                    elif direction is 'D':
                        coordinate = (coordinate[0] + 1, coordinate[1])
                    elif direction is 'L':
                        coordinate = (coordinate[0], coordinate[1] - 1)
                else:
                    path_list.append(coordinate)
                    visit_list.append(coordinate)
                    coordinate = (coordinate[0] - 1, coordinate[1])

            # Case where algorithm has found the exit point.
            elif coordinate == exit_point:
                path_list.append(coordinate)
                visit_list.append(coordinate)
                route_list = []

                # Captures coordinates as one instance of a solution.
                for coordinate in path_list:
                    if type(coordinate) is tuple:
                        route_list.append(coordinate)
                maze_list.append(route_list)
                # Backtracks to the last junction encountered.
                (path_list, visit_list
                 ) = remove_paths(path_list, visit_list)
                if len(path_list) == 0:
                    break
                while (len(path_list) > 0 and
                       type(path_list[-1]) is tuple):
                    (path_list, visit_list
                     ) = remove_paths(path_list, visit_list)
                # Breaks if no directions left to traverse
                if len(path_list) == 0:
                    break
                coordinate = path_list[-1][1]
                direction = path_list[-1][0]
                path_list.append(coordinate)
                visit_list.append(coordinate)
                if direction is 'U':
                    coordinate = (coordinate[0] - 1, coordinate[1])
                elif direction is 'R':
                    coordinate = (coordinate[0], coordinate[1] + 1)
                elif direction is 'D':
                    coordinate = (coordinate[0] + 1, coordinate[1])
                elif direction is 'L':
                    coordinate = (coordinate[0], coordinate[1] - 1)

            # Case where dead end is encountered going up.
            elif path_dict[maze_dict[coordinate]] == 0:
                path_list.append(coordinate)
                visit_list.append(coordinate)

                # Backtracks to the last junction encountered.
                (path_list, visit_list
                 ) = remove_paths(path_list, visit_list)
                if len(path_list) == 0:
                    break
                while (len(path_list) > 0 and
                       type(path_list[-1]) is tuple):
                    (path_list, visit_list
                     ) = remove_paths(path_list, visit_list)
                # Breaks if no directions left to traverse
                if len(path_list) == 0:
                    break
                coordinate = path_list[-1][1]
                direction = path_list[-1][0]
                path_list.append(coordinate)
                visit_list.append(coordinate)
                if direction is 'U':
                    coordinate = (coordinate[0] - 1, coordinate[1])
                elif direction is 'R':
                    coordinate = (coordinate[0], coordinate[1] + 1)
                elif direction is 'D':
                    coordinate = (coordinate[0] + 1, coordinate[1])
                elif direction is 'L':
                    coordinate = (coordinate[0], coordinate[1] - 1)

            # Case where cell has only one direction to be traversed.
            elif path_dict[maze_dict[coordinate]] == 1:
                # Asserts cell has not been visited.
                if coordinate not in visit_list:
                    if maze_dict[coordinate
                                 ] == (False, True, True, False):
                        path_list.append(coordinate)
                        visit_list.append(coordinate)
                        coordinate = (coordinate[0], coordinate[1] + 1)
                        direction = 'R'
                    elif maze_dict[coordinate
                                   ] == (False, False, True, True):
                        path_list.append(coordinate)
                        visit_list.append(coordinate)
                        coordinate = (coordinate[0], coordinate[1] - 1)
                        direction = 'L'
                    elif maze_dict[coordinate
                                   ] == (True, False, True, False):
                        path_list.append(coordinate)
                        visit_list.append(coordinate)
                        coordinate = (coordinate[0] - 1, coordinate[1])
                        direction = 'U'

                # Backtracks to the last junction encountered.
                else:
                    (path_list, visit_list
                     ) = remove_paths(path_list, visit_list)
                    if len(path_list) == 0:
                        break
                    while (len(path_list) > 0 and
                           type(path_list[-1]) is tuple):
                        (path_list, visit_list
                         ) = remove_paths(path_list, visit_list)
                    # Breaks if no directions left to traverse
                    if len(path_list) == 0:
                        break
                    coordinate = path_list[-1][1]
                    direction = path_list[-1][0]
                    path_list.append(coordinate)
                    visit_list.append(coordinate)
                    if direction is 'U':
                        coordinate = (coordinate[0] - 1, coordinate[1])
                    elif direction is 'R':
                        coordinate = (coordinate[0], coordinate[1] + 1)
                    elif direction is 'D':
                        coordinate = (coordinate[0] + 1, coordinate[1])
                    elif direction is 'L':
                        coordinate = (coordinate[0], coordinate[1] - 1)

            # Case where cell has two directions possible to traverse.
            elif path_dict[maze_dict[coordinate]] == 2:
                # Asserts cell has not been visited.
                if coordinate not in visit_list:
                    if maze_dict[coordinate
                                 ] == (True, False, True, True):
                        visit_list.append(coordinate)
                        if ['U', coordinate] not in visit_list:
                            path_list.append(['U', coordinate])
                            visit_list.append(['U', coordinate])
                        if ['L', coordinate] not in visit_list:
                            path_list.append(['L', coordinate])
                            visit_list.append(['L', coordinate])
                        path_list.append(coordinate)
                        visit_list.append(coordinate)
                        if path_list[-2] == ['U', coordinate]:
                            coordinate = (coordinate[0] - 1,
                                          coordinate[1])
                            direction = 'U'
                        elif path_list[-2] == ['L', coordinate]:
                            coordinate = (coordinate[0],
                                          coordinate[1] - 1)
                            direction = 'L'
                    elif maze_dict[coordinate
                                   ] == (True, True, True, False):
                        visit_list.append(coordinate)
                        if ['U', coordinate] not in visit_list:
                            path_list.append(['U', coordinate])
                            visit_list.append(['U', coordinate])
                        if ['R', coordinate] not in visit_list:
                            path_list.append(['R', coordinate])
                            visit_list.append(['R', coordinate])
                        path_list.append(coordinate)
                        visit_list.append(coordinate)
                        if path_list[-2] == ['U', coordinate]:
                            coordinate = (coordinate[0] - 1,
                                          coordinate[1])
                            direction = 'U'
                        if path_list[-2] == ['R', coordinate]:
                            coordinate = (coordinate[0],
                                          coordinate[1] + 1)
                            direction = 'R'
                    elif maze_dict[coordinate
                                   ] == (False, True, True, True):
                        visit_list.append(coordinate)
                        if ['R', coordinate] not in visit_list:
                            path_list.append(['R', coordinate])
                            visit_list.append(['R', coordinate])
                        if ['L', coordinate] not in visit_list:
                            path_list.append(['L', coordinate])
                            visit_list.append(['L', coordinate])
                        path_list.append(coordinate)
                        visit_list.append(coordinate)
                        if path_list[-2] == ['R', coordinate]:
                            coordinate = (coordinate[0],
                                          coordinate[1] + 1)
                            direction = 'R'
                        if path_list[-2] == ['L', coordinate]:
                            coordinate = (coordinate[0],
                                          coordinate[1] - 1)
                            direction = 'L'

                # Backtracks to the last junction encountered.
                else:
                    (path_list, visit_list
                     ) = remove_paths(path_list, visit_list)
                    if len(path_list) == 0:
                        break
                    while (len(path_list) > 0 and
                           type(path_list[-1]) is tuple):
                        (path_list, visit_list
                         ) = remove_paths(path_list, visit_list)
                    # Breaks if no directions left to traverse
                    if len(path_list) == 0:
                        break
                    coordinate = path_list[-1][1]
                    direction = path_list[-1][0]
                    path_list.append(coordinate)
                    visit_list.append(coordinate)
                    if direction is 'U':
                        coordinate = (coordinate[0] - 1, coordinate[1])
                    elif direction is 'R':
                        coordinate = (coordinate[0], coordinate[1] + 1)
                    elif direction is 'D':
                        coordinate = (coordinate[0] + 1, coordinate[1])
                    elif direction is 'L':
                        coordinate = (coordinate[0], coordinate[1] - 1)

            # Case where cell has three possible directions to traverse.
            elif path_dict[maze_dict[coordinate]] == 3:
                # Asserts cell has not been visited.
                if coordinate not in visit_list:
                    if maze_dict[coordinate
                                 ] == (True, True, True, True):
                        visit_list.append(coordinate)
                        if ['U', coordinate] not in visit_list:
                            path_list.append(['U', coordinate])
                            visit_list.append(['U', coordinate])
                        if ['R', coordinate] not in visit_list:
                            path_list.append(['R', coordinate])
                            visit_list.append(['R', coordinate])
                        if ['L', coordinate] not in visit_list:
                            path_list.append(['L', coordinate])
                            visit_list.append(['L', coordinate])
                        path_list.append(coordinate)
                        visit_list.append(coordinate)
                        if path_list[-2] == ['U', coordinate]:
                            coordinate = (coordinate[0] - 1,
                                          coordinate[1])
                            direction = 'U'
                        if path_list[-2] == ['R', coordinate]:
                            coordinate = (coordinate[0],
                                          coordinate[1] + 1)
                            direction = 'R'
                        if path_list[-2] == ['L', coordinate]:
                            coordinate = (coordinate[0],
                                          coordinate[1] - 1)
                            direction = 'L'

                # Backtracks to the last junction encountered.
                else:
                    (path_list, visit_list
                     ) = remove_paths(path_list, visit_list)
                    if len(path_list) == 0:
                        break
                    while (len(path_list) > 0 and
                           type(path_list[-1]) is tuple):
                        (path_list, visit_list
                         ) = remove_paths(path_list, visit_list)
                    # Breaks if no directions left to traverse
                    if len(path_list) == 0:
                        break
                    coordinate = path_list[-1][1]
                    direction = path_list[-1][0]
                    path_list.append(coordinate)
                    visit_list.append(coordinate)
                    if direction is 'U':
                        coordinate = (coordinate[0] - 1, coordinate[1])
                    elif direction is 'R':
                        coordinate = (coordinate[0], coordinate[1] + 1)
                    elif direction is 'D':
                        coordinate = (coordinate[0] + 1, coordinate[1])
                    elif direction is 'L':
                        coordinate = (coordinate[0], coordinate[1] - 1)

        # Algorithm traverses to the 'Right'.
        elif direction is 'R':
            # Case where current coordinate is the entry point.
            if coordinate == entry_point:
                # Asserts whether coordinate has been traversed.
                if coordinate in visit_list:
                    # Backtracks to the last junction encountered.
                    (path_list, visit_list
                     ) = remove_paths(path_list, visit_list)
                    if len(path_list) == 0:
                        break
                    while (len(path_list) > 0 and
                           type(path_list[-1]) is tuple):
                        (path_list, visit_list
                         ) = remove_paths(path_list, visit_list)
                    # Breaks if no directions left to traverse
                    if len(path_list) == 0:
                        break
                    coordinate = path_list[-1][1]
                    direction = path_list[-1][0]
                    path_list.append(coordinate)
                    visit_list.append(coordinate)
                    if direction is 'U':
                        coordinate = (coordinate[0] - 1, coordinate[1])
                    elif direction is 'R':
                        coordinate = (coordinate[0], coordinate[1] + 1)
                    elif direction is 'D':
                        coordinate = (coordinate[0] + 1, coordinate[1])
                    elif direction is 'L':
                        coordinate = (coordinate[0], coordinate[1] - 1)
                else:
                    path_list.append(coordinate)
                    visit_list.append(coordinate)
                    coordinate = (coordinate[0], coordinate[1] + 1)

            # Case where algorithm has found the exit point.
            elif coordinate == exit_point:
                path_list.append(coordinate)
                visit_list.append(coordinate)
                route_list = []

                # Captures coordinates as one instance of a solution.
                for coordinate in path_list:
                    if type(coordinate) is tuple:
                        route_list.append(coordinate)
                maze_list.append(route_list)

                # Backtracks to the last junction encountered.
                (path_list, visit_list
                 ) = remove_paths(path_list, visit_list)
                if len(path_list) == 0:
                    break
                while (len(path_list) > 0 and
                       type(path_list[-1]) is tuple):
                    (path_list, visit_list
                     ) = remove_paths(path_list, visit_list)
                # Breaks if no directions left to traverse
                if len(path_list) == 0:
                    break
                coordinate = path_list[-1][1]
                direction = path_list[-1][0]
                path_list.append(coordinate)
                visit_list.append(coordinate)
                if direction is 'U':
                    coordinate = (coordinate[0] - 1, coordinate[1])
                elif direction is 'R':
                    coordinate = (coordinate[0], coordinate[1] + 1)
                elif direction is 'D':
                    coordinate = (coordinate[0] + 1, coordinate[1])
                elif direction is 'L':
                    coordinate = (coordinate[0], coordinate[1] - 1)

            # Case where dead end is encountered going right.
            elif path_dict[maze_dict[coordinate]] == 0:
                path_list.append(coordinate)
                visit_list.append(coordinate)

                # Backtracks to the last junction encountered.
                (path_list, visit_list
                 ) = remove_paths(path_list, visit_list)
                if len(path_list) == 0:
                    break
                while (len(path_list) > 0 and
                       type(path_list[-1]) is tuple):
                    (path_list, visit_list
                     ) = remove_paths(path_list, visit_list)
                # Breaks if no directions left to traverse
                if len(path_list) == 0:
                    break
                coordinate = path_list[-1][1]
                direction = path_list[-1][0]
                path_list.append(coordinate)
                visit_list.append(coordinate)
                if direction is 'U':
                    coordinate = (coordinate[0] - 1, coordinate[1])
                elif direction is 'R':
                    coordinate = (coordinate[0], coordinate[1] + 1)
                elif direction is 'D':
                    coordinate = (coordinate[0] + 1, coordinate[1])
                elif direction is 'L':
                    coordinate = (coordinate[0], coordinate[1] - 1)

            # Case where cell has only one direction to be traversed.
            elif path_dict[maze_dict[coordinate]] == 1:
                # Asserts cell has not been visited.
                if coordinate not in visit_list:
                    if maze_dict[coordinate
                                 ] == (False, False, True, True):
                        path_list.append(coordinate)
                        visit_list.append(coordinate)
                        coordinate = (coordinate[0] + 1, coordinate[1])
                        direction = 'D'
                    elif maze_dict[coordinate
                                   ] == (True, False, False, True):
                        path_list.append(coordinate)
                        visit_list.append(coordinate)
                        coordinate = (coordinate[0] - 1, coordinate[1])
                        direction = 'U'
                    elif maze_dict[coordinate
                                   ] == (False, True, False, True):
                        path_list.append(coordinate)
                        visit_list.append(coordinate)
                        coordinate = (coordinate[0], coordinate[1] + 1)
                        direction = 'R'

                # Backtracks to the last junction encountered.
                else:
                    (path_list, visit_list
                     ) = remove_paths(path_list, visit_list)
                    if len(path_list) == 0:
                        break
                    while (len(path_list) > 0 and
                           type(path_list[-1]) is tuple):
                        (path_list, visit_list
                         ) = remove_paths(path_list, visit_list)
                    # Breaks if no directions left to traverse
                    if len(path_list) == 0:
                        break
                    coordinate = path_list[-1][1]
                    direction = path_list[-1][0]
                    path_list.append(coordinate)
                    visit_list.append(coordinate)
                    if direction is 'U':
                        coordinate = (coordinate[0] - 1, coordinate[1])
                    elif direction is 'R':
                        coordinate = (coordinate[0], coordinate[1] + 1)
                    elif direction is 'D':
                        coordinate = (coordinate[0] + 1, coordinate[1])
                    elif direction is 'L':
                        coordinate = (coordinate[0], coordinate[1] - 1)

            # Case where cell has two directions possible to traverse.
            elif path_dict[maze_dict[coordinate]] == 2:
                # Asserts cell has not been visited.
                if coordinate not in visit_list:
                    if maze_dict[coordinate
                                 ] == (False, True, True, True):
                        visit_list.append(coordinate)
                        if ['R', coordinate] not in visit_list:
                            path_list.append(['R', coordinate])
                            visit_list.append(['R', coordinate])
                        if ['D', coordinate] not in visit_list:
                            path_list.append(['D', coordinate])
                            visit_list.append(['D', coordinate])
                        path_list.append(coordinate)
                        visit_list.append(coordinate)
                        if path_list[-2] == ['R', coordinate]:
                            coordinate = (coordinate[0],
                                          coordinate[1] + 1)
                            direction = 'R'
                        elif path_list[-2] == ['D', coordinate]:
                            coordinate = (coordinate[0] + 1,
                                          coordinate[1])
                            direction = 'D'
                    elif maze_dict[coordinate
                                   ] == (True, True, False, True):
                        visit_list.append(coordinate)
                        if ['U', coordinate] not in visit_list:
                            path_list.append(['U', coordinate])
                            visit_list.append(['U', coordinate])
                        if ['R', coordinate] not in visit_list:
                            path_list.append(['R', coordinate])
                            visit_list.append(['R', coordinate])
                        path_list.append(coordinate)
                        visit_list.append(coordinate)
                        if path_list[-2] == ['U', coordinate]:
                            coordinate = (coordinate[0] - 1,
                                          coordinate[1])
                            direction = 'U'
                        if path_list[-2] == ['R', coordinate]:
                            coordinate = (coordinate[0],
                                          coordinate[1] + 1)
                            direction = 'R'
                    elif maze_dict[coordinate
                                   ] == (True, False, True, True):
                        visit_list.append(coordinate)
                        if ['U', coordinate] not in visit_list:
                            path_list.append(['U', coordinate])
                            visit_list.append(['U', coordinate])
                        if ['D', coordinate] not in visit_list:
                            path_list.append(['D', coordinate])
                            visit_list.append(['D', coordinate])
                        path_list.append(coordinate)
                        visit_list.append(coordinate)
                        if path_list[-2] == ['U', coordinate]:
                            coordinate = (coordinate[0] - 1,
                                          coordinate[1])
                            direction = 'U'
                        if path_list[-2] == ['D', coordinate]:
                            coordinate = (coordinate[0] + 1,
                                          coordinate[1])
                            direction = 'D'

                # Backtracks to the last junction encountered.
                else:
                    (path_list, visit_list
                     ) = remove_paths(path_list, visit_list)
                    if len(path_list) == 0:
                        break
                    while (len(path_list) > 0 and
                           type(path_list[-1]) is tuple):
                        (path_list, visit_list
                         ) = remove_paths(path_list, visit_list)
                    # Breaks if no directions left to traverse
                    if len(path_list) == 0:
                        break
                    coordinate = path_list[-1][1]
                    direction = path_list[-1][0]
                    path_list.append(coordinate)
                    visit_list.append(coordinate)
                    if direction is 'U':
                        coordinate = (coordinate[0] - 1, coordinate[1])
                    elif direction is 'R':
                        coordinate = (coordinate[0], coordinate[1] + 1)
                    elif direction is 'D':
                        coordinate = (coordinate[0] + 1, coordinate[1])
                    elif direction is 'L':
                        coordinate = (coordinate[0], coordinate[1] - 1)

            # Case where cell has three possible directions to traverse.
            elif path_dict[maze_dict[coordinate]] == 3:
                # Asserts cell has not been visited.
                if coordinate not in visit_list:
                    if maze_dict[coordinate
                                 ] == (True, True, True, True):
                        visit_list.append(coordinate)
                        if ['U', coordinate] not in visit_list:
                            path_list.append(['U', coordinate])
                            visit_list.append(['U', coordinate])
                        if ['R', coordinate] not in visit_list:
                            path_list.append(['R', coordinate])
                            visit_list.append(['R', coordinate])
                        if ['D', coordinate] not in visit_list:
                            path_list.append(['D', coordinate])
                            visit_list.append(['D', coordinate])
                        path_list.append(coordinate)
                        visit_list.append(coordinate)
                        if path_list[-2] == ['U', coordinate]:
                            coordinate = (coordinate[0] - 1,
                                          coordinate[1])
                            direction = 'U'
                        if path_list[-2] == ['R', coordinate]:
                            coordinate = (coordinate[0],
                                          coordinate[1] + 1)
                            direction = 'R'
                        if path_list[-2] == ['D', coordinate]:
                            coordinate = (coordinate[0] + 1,
                                          coordinate[1])
                            direction = 'D'

                # Backtracks to the last junction encountered.
                else:
                    (path_list, visit_list
                     ) = remove_paths(path_list, visit_list)
                    if len(path_list) == 0:
                        break
                    while (len(path_list) > 0 and
                           type(path_list[-1]) is tuple):
                        (path_list, visit_list
                         ) = remove_paths(path_list, visit_list)
                    # Breaks if no directions left to traverse
                    if len(path_list) == 0:
                        break
                    coordinate = path_list[-1][1]
                    direction = path_list[-1][0]
                    path_list.append(coordinate)
                    visit_list.append(coordinate)
                    if direction is 'U':
                        coordinate = (coordinate[0] - 1, coordinate[1])
                    elif direction is 'R':
                        coordinate = (coordinate[0], coordinate[1] + 1)
                    elif direction is 'D':
                        coordinate = (coordinate[0] + 1, coordinate[1])
                    elif direction is 'L':
                        coordinate = (coordinate[0], coordinate[1] - 1)

        # Algorithm tries traversing 'Down'.
        elif direction is 'D':
            # Case where current coordinate is the entry point.
            if coordinate == entry_point:
                # Asserts whether coordinate has been traversed.
                if coordinate in visit_list:
                    # Backtracks to the last junction encountered.
                    (path_list, visit_list
                     ) = remove_paths(path_list, visit_list)
                    if len(path_list) == 0:
                        break
                    while (len(path_list) > 0 and
                           type(path_list[-1]) is tuple):
                        (path_list, visit_list
                         ) = remove_paths(path_list, visit_list)
                    # Breaks if no directions left to traverse
                    if len(path_list) == 0:
                        break
                    coordinate = path_list[-1][1]
                    direction = path_list[-1][0]
                    path_list.append(coordinate)
                    visit_list.append(coordinate)
                    if direction is 'U':
                        coordinate = (coordinate[0] - 1, coordinate[1])
                    elif direction is 'R':
                        coordinate = (coordinate[0], coordinate[1] + 1)
                    elif direction is 'D':
                        coordinate = (coordinate[0] + 1, coordinate[1])
                    elif direction is 'L':
                        coordinate = (coordinate[0], coordinate[1] - 1)
                else:
                    path_list.append(coordinate)
                    visit_list.append(coordinate)
                    coordinate = (coordinate[0] + 1, coordinate[1])

            # Case where algorithm has found the exit point.
            elif coordinate == exit_point:
                path_list.append(coordinate)
                visit_list.append(coordinate)
                route_list = []

                # Captures coordinates as one instance of a solution.
                for coordinate in path_list:
                    if type(coordinate) is tuple:
                        route_list.append(coordinate)
                maze_list.append(route_list)

                # Backtracks to the last junction encountered.
                (path_list, visit_list
                 ) = remove_paths(path_list, visit_list)
                if len(path_list) == 0:
                    break
                while (len(path_list) > 0 and
                       type(path_list[-1]) is tuple):
                    (path_list, visit_list
                     ) = remove_paths(path_list, visit_list)
                # Breaks if no directions left to traverse
                if len(path_list) == 0:
                    break
                coordinate = path_list[-1][1]
                direction = path_list[-1][0]
                path_list.append(coordinate)
                visit_list.append(coordinate)
                if direction is 'U':
                    coordinate = (coordinate[0] - 1, coordinate[1])
                elif direction is 'R':
                    coordinate = (coordinate[0], coordinate[1] + 1)
                elif direction is 'D':
                    coordinate = (coordinate[0] + 1, coordinate[1])
                elif direction is 'L':
                    coordinate = (coordinate[0], coordinate[1] - 1)

            # Case where dead end is encountered going down.
            elif path_dict[maze_dict[coordinate]] == 0:
                path_list.append(coordinate)
                visit_list.append(coordinate)

                # Backtracks to the last junction encountered.
                (path_list, visit_list
                 ) = remove_paths(path_list, visit_list)
                if len(path_list) == 0:
                    break
                while (len(path_list) > 0 and
                       type(path_list[-1]) is tuple):
                    (path_list, visit_list
                     ) = remove_paths(path_list, visit_list)
                # Breaks if no directions left to traverse
                if len(path_list) == 0:
                    break
                coordinate = path_list[-1][1]
                direction = path_list[-1][0]
                path_list.append(coordinate)
                visit_list.append(coordinate)
                if direction is 'U':
                    coordinate = (coordinate[0] - 1, coordinate[1])
                elif direction is 'R':
                    coordinate = (coordinate[0], coordinate[1] + 1)
                elif direction is 'D':
                    coordinate = (coordinate[0] + 1, coordinate[1])
                elif direction is 'L':
                    coordinate = (coordinate[0], coordinate[1] - 1)

            # Case where cell has only one direction to be traversed.
            elif path_dict[maze_dict[coordinate]] == 1:
                # Asserts cell has not been visited.
                if coordinate not in visit_list:
                    if maze_dict[coordinate
                                 ] == (True, True, False, False):
                        path_list.append(coordinate)
                        visit_list.append(coordinate)
                        coordinate = (coordinate[0], coordinate[1] + 1)
                        direction = 'R'
                    elif maze_dict[coordinate
                                   ] == (True, False, False, True):
                        path_list.append(coordinate)
                        visit_list.append(coordinate)
                        coordinate = (coordinate[0], coordinate[1] - 1)
                        direction = 'L'
                    elif maze_dict[coordinate
                                   ] == (True, False, True, False):
                        path_list.append(coordinate)
                        visit_list.append(coordinate)
                        coordinate = (coordinate[0] + 1, coordinate[1])
                        direction = 'D'

                # Backtracks to the last junction encountered.
                else:
                    (path_list, visit_list
                     ) = remove_paths(path_list, visit_list)
                    if len(path_list) == 0:
                        break
                    while (len(path_list) > 0 and
                           type(path_list[-1]) is tuple):
                        (path_list, visit_list
                         ) = remove_paths(path_list, visit_list)
                    # Breaks if no directions left to traverse
                    if len(path_list) == 0:
                        break
                    coordinate = path_list[-1][1]
                    direction = path_list[-1][0]
                    path_list.append(coordinate)
                    visit_list.append(coordinate)
                    if direction is 'U':
                        coordinate = (coordinate[0] - 1, coordinate[1])
                    elif direction is 'R':
                        coordinate = (coordinate[0], coordinate[1] + 1)
                    elif direction is 'D':
                        coordinate = (coordinate[0] + 1, coordinate[1])
                    elif direction is 'L':
                        coordinate = (coordinate[0], coordinate[1] - 1)

            # Case where cell has two directions possible to traverse.
            elif path_dict[maze_dict[coordinate]] == 2:
                # Asserts cell has not been visited.
                if coordinate not in visit_list:
                    if maze_dict[coordinate
                                 ] == (True, False, True, True):
                        visit_list.append(coordinate)
                        if ['D', coordinate] not in visit_list:
                            path_list.append(['D', coordinate])
                            visit_list.append(['D', coordinate])
                        if ['L', coordinate] not in visit_list:
                            path_list.append(['L', coordinate])
                            visit_list.append(['L', coordinate])
                        path_list.append(coordinate)
                        visit_list.append(coordinate)
                        if path_list[-2] == ['D', coordinate]:
                            coordinate = (coordinate[0] + 1,
                                          coordinate[1])
                            direction = 'D'
                        elif path_list[-2] == ['L', coordinate]:
                            coordinate = (coordinate[0],
                                          coordinate[1] - 1)
                            direction = 'L'
                    elif maze_dict[coordinate
                                   ] == (True, True, True, False):
                        visit_list.append(coordinate)
                        if ['R', coordinate] not in visit_list:
                            path_list.append(['R', coordinate])
                            visit_list.append(['R', coordinate])
                        if ['D', coordinate] not in visit_list:
                            path_list.append(['D', coordinate])
                            visit_list.append(['D', coordinate])
                        path_list.append(coordinate)
                        visit_list.append(coordinate)
                        if path_list[-2] == ['R', coordinate]:
                            coordinate = (coordinate[0],
                                          coordinate[1] + 1)
                            direction = 'R'
                        if path_list[-2] == ['D', coordinate]:
                            coordinate = (coordinate[0] + 1,
                                          coordinate[1])
                            direction = 'D'
                    elif maze_dict[coordinate
                                   ] == (True, True, False, True):
                        visit_list.append(coordinate)
                        if ['D', coordinate] not in visit_list:
                            path_list.append(['R', coordinate])
                            visit_list.append(['R', coordinate])
                        if ['L', coordinate] not in visit_list:
                            path_list.append(['L', coordinate])
                            visit_list.append(['L', coordinate])
                        path_list.append(coordinate)
                        visit_list.append(coordinate)
                        if path_list[-2] == ['R', coordinate]:
                            coordinate = (coordinate[0],
                                          coordinate[1] + 1)
                            direction = 'R'
                        if path_list[-2] == ['L', coordinate]:
                            coordinate = (coordinate[0],
                                          coordinate[1] - 1)
                            direction = 'L'

                # Backtracks to the last junction encountered.
                else:
                    (path_list, visit_list
                     ) = remove_paths(path_list, visit_list)
                    if len(path_list) == 0:
                        break
                    while (len(path_list) > 0 and
                           type(path_list[-1]) is tuple):
                        (path_list, visit_list
                         ) = remove_paths(path_list, visit_list)
                    # Breaks if no directions left to traverse
                    if len(path_list) == 0:
                        break
                    coordinate = path_list[-1][1]
                    direction = path_list[-1][0]
                    path_list.append(coordinate)
                    visit_list.append(coordinate)
                    if direction is 'U':
                        coordinate = (coordinate[0] - 1, coordinate[1])
                    elif direction is 'R':
                        coordinate = (coordinate[0], coordinate[1] + 1)
                    elif direction is 'D':
                        coordinate = (coordinate[0] + 1, coordinate[1])
                    elif direction is 'L':
                        coordinate = (coordinate[0], coordinate[1] - 1)

            # Case where cell has three possible directions to traverse.
            elif path_dict[maze_dict[coordinate]] == 3:
                # Asserts cell has not been visited.
                if coordinate not in visit_list:
                    if maze_dict[coordinate
                                 ] == (True, True, True, True):
                        visit_list.append(coordinate)
                        if ['R', coordinate] not in visit_list:
                            path_list.append(['R', coordinate])
                            visit_list.append(['R', coordinate])
                        if ['D', coordinate] not in visit_list:
                            path_list.append(['D', coordinate])
                            visit_list.append(['D', coordinate])
                        if ['L', coordinate] not in visit_list:
                            path_list.append(['L', coordinate])
                            visit_list.append(['L', coordinate])
                        path_list.append(coordinate)
                        visit_list.append(coordinate)
                        if path_list[-2] == ['R', coordinate]:
                            coordinate = (coordinate[0],
                                          coordinate[1] + 1)
                            direction = 'R'
                        if path_list[-2] == ['D', coordinate]:
                            coordinate = (coordinate[0] + 1,
                                          coordinate[1])
                            direction = 'D'
                        if path_list[-2] == ['L', coordinate]:
                            coordinate = (coordinate[0],
                                          coordinate[1] - 1)
                            direction = 'L'

                # Backtracks to the last junction encountered.
                else:
                    (path_list, visit_list
                     ) = remove_paths(path_list, visit_list)
                    if len(path_list) == 0:
                        break
                    while (len(path_list) > 0 and
                           type(path_list[-1]) is tuple):
                        (path_list, visit_list
                         ) = remove_paths(path_list, visit_list)
                    # Breaks if no directions left to traverse
                    if len(path_list) == 0:
                        break
                    coordinate = path_list[-1][1]
                    direction = path_list[-1][0]
                    path_list.append(coordinate)
                    visit_list.append(coordinate)
                    if direction is 'U':
                        coordinate = (coordinate[0] - 1, coordinate[1])
                    elif direction is 'R':
                        coordinate = (coordinate[0], coordinate[1] + 1)
                    elif direction is 'D':
                        coordinate = (coordinate[0] + 1, coordinate[1])
                    elif direction is 'L':
                        coordinate = (coordinate[0], coordinate[1] - 1)

        # Algorithm tries traversing to the 'Left'.
        elif direction is 'L':
            # Case where current coordinate is the entry point.
            if coordinate == entry_point:
                # Asserts whether coordinate has been traversed.
                if coordinate in visit_list:
                    # Backtracks to the last junction encountered.
                    (path_list, visit_list
                     ) = remove_paths(path_list, visit_list)
                    if len(path_list) == 0:
                        break
                    while (len(path_list) > 0 and
                           type(path_list[-1]) is tuple):
                        (path_list, visit_list
                         ) = remove_paths(path_list, visit_list)
                    # Breaks if no directions left to traverse
                    if len(path_list) == 0:
                        break
                    coordinate = path_list[-1][1]
                    direction = path_list[-1][0]
                    path_list.append(coordinate)
                    visit_list.append(coordinate)
                    if direction is 'U':
                        coordinate = (coordinate[0] - 1, coordinate[1])
                    elif direction is 'R':
                        coordinate = (coordinate[0], coordinate[1] + 1)
                    elif direction is 'D':
                        coordinate = (coordinate[0] + 1, coordinate[1])
                    elif direction is 'L':
                        coordinate = (coordinate[0], coordinate[1] - 1)
                else:
                    path_list.append(coordinate)
                    visit_list.append(coordinate)
                    coordinate = (coordinate[0], coordinate[1] - 1)

            # Case where algorithm has found the exit point.
            elif coordinate == exit_point:
                path_list.append(coordinate)
                visit_list.append(coordinate)
                route_list = []

                # Captures coordinates as one instance of a solution.
                for coordinate in path_list:
                    if type(coordinate) is tuple:
                        route_list.append(coordinate)
                maze_list.append(route_list)

                # Backtracks to the last junction encountered.
                (path_list, visit_list
                 ) = remove_paths(path_list, visit_list)
                if len(path_list) == 0:
                    break
                while (len(path_list) > 0 and
                       type(path_list[-1]) is tuple):
                    (path_list, visit_list
                     ) = remove_paths(path_list, visit_list)
                # Breaks if no directions left to traverse
                if len(path_list) == 0:
                    break
                coordinate = path_list[-1][1]
                direction = path_list[-1][0]
                path_list.append(coordinate)
                visit_list.append(coordinate)
                if direction is 'U':
                    coordinate = (coordinate[0] - 1, coordinate[1])
                elif direction is 'R':
                    coordinate = (coordinate[0], coordinate[1] + 1)
                elif direction is 'D':
                    coordinate = (coordinate[0] + 1, coordinate[1])
                elif direction is 'L':
                    coordinate = (coordinate[0], coordinate[1] - 1)

            # Case where dead end is encountered going up.
            elif path_dict[maze_dict[coordinate]] == 0:
                path_list.append(coordinate)
                visit_list.append(coordinate)

                # Backtracks to the last junction encountered.
                (path_list, visit_list
                 ) = remove_paths(path_list, visit_list)
                if len(path_list) == 0:
                    break
                while (len(path_list) > 0 and
                       type(path_list[-1]) is tuple):
                    (path_list, visit_list
                     ) = remove_paths(path_list, visit_list)
                # Breaks if no directions left to traverse
                if len(path_list) == 0:
                    break
                coordinate = path_list[-1][1]
                direction = path_list[-1][0]
                path_list.append(coordinate)
                visit_list.append(coordinate)
                if direction is 'U':
                    coordinate = (coordinate[0] - 1, coordinate[1])
                elif direction is 'R':
                    coordinate = (coordinate[0], coordinate[1] + 1)
                elif direction is 'D':
                    coordinate = (coordinate[0] + 1, coordinate[1])
                elif direction is 'L':
                    coordinate = (coordinate[0], coordinate[1] - 1)

            # Case where cell has only one direction to be traversed.
            elif path_dict[maze_dict[coordinate]] == 1:
                # Asserts cell has not been visited.
                if coordinate not in visit_list:
                    if maze_dict[coordinate
                                 ] == (False, True, True, False):
                        path_list.append(coordinate)
                        visit_list.append(coordinate)
                        coordinate = (coordinate[0] + 1, coordinate[1])
                        direction = 'D'
                    elif maze_dict[coordinate
                                   ] == (True, True, False, False):
                        path_list.append(coordinate)
                        visit_list.append(coordinate)
                        coordinate = (coordinate[0] - 1, coordinate[1])
                        direction = 'U'
                    elif maze_dict[coordinate
                                   ] == (False, True, False, True):
                        path_list.append(coordinate)
                        visit_list.append(coordinate)
                        coordinate = (coordinate[0], coordinate[1] - 1)
                        direction = 'L'

                # Backtracks to the last junction encountered.
                else:
                    (path_list, visit_list
                     ) = remove_paths(path_list, visit_list)
                    if len(path_list) == 0:
                        break
                    while (len(path_list) > 0 and
                           type(path_list[-1]) is tuple):
                        (path_list, visit_list
                         ) = remove_paths(path_list, visit_list)
                    # Breaks if no directions left to traverse
                    if len(path_list) == 0:
                        break
                    coordinate = path_list[-1][1]
                    direction = path_list[-1][0]
                    path_list.append(coordinate)
                    visit_list.append(coordinate)
                    if direction is 'U':
                        coordinate = (coordinate[0] - 1, coordinate[1])
                    elif direction is 'R':
                        coordinate = (coordinate[0], coordinate[1] + 1)
                    elif direction is 'D':
                        coordinate = (coordinate[0] + 1, coordinate[1])
                    elif direction is 'L':
                        coordinate = (coordinate[0], coordinate[1] - 1)

            # Case where cell has two directions possible to traverse.
            elif path_dict[maze_dict[coordinate]] == 2:
                # Asserts cell has not been visited.
                if coordinate not in visit_list:
                    if maze_dict[coordinate
                                 ] == (False, True, True, True):
                        visit_list.append(coordinate)
                        if ['D', coordinate] not in visit_list:
                            path_list.append(['D', coordinate])
                            visit_list.append(['D', coordinate])
                        if ['L', coordinate] not in visit_list:
                            path_list.append(['L', coordinate])
                            visit_list.append(['L', coordinate])
                        path_list.append(coordinate)
                        visit_list.append(coordinate)
                        if path_list[-2] == ['D', coordinate]:
                            coordinate = (coordinate[0] + 1,
                                          coordinate[1])
                            direction = 'D'
                        elif path_list[-2] == ['L', coordinate]:
                            coordinate = (coordinate[0],
                                          coordinate[1] - 1)
                            direction = 'L'
                    elif maze_dict[coordinate
                                   ] == (True, True, False, True):
                        visit_list.append(coordinate)
                        if ['U', coordinate] not in visit_list:
                            path_list.append(['U', coordinate])
                            visit_list.append(['R', coordinate])
                        if ['L', coordinate] not in visit_list:
                            path_list.append(['L', coordinate])
                            visit_list.append(['L', coordinate])
                        path_list.append(coordinate)
                        visit_list.append(coordinate)
                        if path_list[-2] == ['U', coordinate]:
                            coordinate = (coordinate[0] - 1,
                                          coordinate[1])
                            direction = 'U'
                        if path_list[-2] == ['L', coordinate]:
                            coordinate = (coordinate[0],
                                          coordinate[1] - 1)
                            direction = 'L'
                    elif maze_dict[coordinate
                                   ] == (True, True, True, False):
                        visit_list.append(coordinate)
                        if ['U', coordinate] not in visit_list:
                            path_list.append(['U', coordinate])
                            visit_list.append(['U', coordinate])
                        if ['D', coordinate] not in visit_list:
                            path_list.append(['D', coordinate])
                            visit_list.append(['D', coordinate])
                        path_list.append(coordinate)
                        visit_list.append(coordinate)
                        if path_list[-2] == ['U', coordinate]:
                            coordinate = (coordinate[0] - 1,
                                          coordinate[1])
                            direction = 'U'
                        if path_list[-2] == ['D', coordinate]:
                            coordinate = (coordinate[0] + 1,
                                          coordinate[1])
                            direction = 'D'

                # Backtracks to the last junction encountered.
                else:
                    (path_list, visit_list
                     ) = remove_paths(path_list, visit_list)
                    if len(path_list) == 0:
                        break
                    while (len(path_list) > 0 and
                           type(path_list[-1]) is tuple):
                        (path_list, visit_list
                         ) = remove_paths(path_list, visit_list)
                    # Breaks if no directions left to traverse
                    if len(path_list) == 0:
                        break
                    coordinate = path_list[-1][1]
                    direction = path_list[-1][0]
                    path_list.append(coordinate)
                    visit_list.append(coordinate)
                    if direction is 'U':
                        coordinate = (coordinate[0] - 1, coordinate[1])
                    elif direction is 'R':
                        coordinate = (coordinate[0], coordinate[1] + 1)
                    elif direction is 'D':
                        coordinate = (coordinate[0] + 1, coordinate[1])
                    elif direction is 'L':
                        coordinate = (coordinate[0], coordinate[1] - 1)

            # Case where cell has three possible directions to traverse.
            elif path_dict[maze_dict[coordinate]] == 3:
                # Asserts cell has not been visited.
                if coordinate not in visit_list:
                    if maze_dict[coordinate
                                 ] == (True, True, True, True):
                        visit_list.append(coordinate)
                        if ['U', coordinate] not in visit_list:
                            path_list.append(['U', coordinate])
                            visit_list.append(['U', coordinate])
                        if ['D', coordinate] not in visit_list:
                            path_list.append(['D', coordinate])
                            visit_list.append(['D', coordinate])
                        if ['L', coordinate] not in visit_list:
                            path_list.append(['L', coordinate])
                            visit_list.append(['L', coordinate])
                        path_list.append(coordinate)
                        visit_list.append(coordinate)
                        if path_list[-2] == ['U', coordinate]:
                            coordinate = (coordinate[0] - 1,
                                          coordinate[1])
                            direction = 'R'
                        if path_list[-2] == ['D', coordinate]:
                            coordinate = (coordinate[0] + 1,
                                          coordinate[1])
                            direction = 'D'
                        if path_list[-2] == ['L', coordinate]:
                            coordinate = (coordinate[0],
                                          coordinate[1] - 1)
                            direction = 'L'

                # Backtracks to the last junction encountered.
                else:
                    (path_list, visit_list
                     ) = remove_paths(path_list, visit_list)
                    if len(path_list) == 0:
                        break
                    while (len(path_list) > 0 and
                           type(path_list[-1]) is tuple):
                        (path_list, visit_list
                         ) = remove_paths(path_list, visit_list)
                    # Breaks if no directions left to traverse
                    if len(path_list) == 0:
                        break
                    coordinate = path_list[-1][1]
                    direction = path_list[-1][0]
                    path_list.append(coordinate)
                    visit_list.append(coordinate)
                    if direction is 'U':
                        coordinate = (coordinate[0] - 1, coordinate[1])
                    elif direction is 'R':
                        coordinate = (coordinate[0], coordinate[1] + 1)
                    elif direction is 'D':
                        coordinate = (coordinate[0] + 1, coordinate[1])
                    elif direction is 'L':
                        coordinate = (coordinate[0], coordinate[1] - 1)

    # Filters solutions contain 'point', returns None if none detected.
    [through_list.append(path) for path in maze_list if point in path]

    # Returns None if no solutions pass 'point'.
    if len(through_list) == 0:
        return(None)

    # Determines the shortest paths in the list of all solutions.
    shortest_length = len(through_list[0])
    for path in through_list:
        if len(path) < shortest_length:
            shortest_length = len(path)

    # Returns all paths with length equivalent to 'shortest_length'.
    [shortest_list.append(path) for path in through_list
     if len(path) == shortest_length]
    return(sorted(shortest_list))

def maze_dictionary(maze):
    """Creates a dictionary mapping each cell to its coordinates."""
    # Matches each cell in the maze to its corresponding coordinates.
    maze_dict = defaultdict(tuple)
    for row_num, row in enumerate(maze):
        for cell_num, cell in enumerate(row):
            maze_dict[(row_num, cell_num)] = cell
    return(maze_dict)

def path_dictionary(path_dict):
    """Creates a dictionary listing all possible types of cells"""
    # Cells which are dead ends.
    path_dict[(False, False, True, False)] = 0
    path_dict[(False, False, False, True)] = 0
    path_dict[(True, False, False, False)] = 0
    path_dict[(False, True, False, False)] = 0
    # Cells which have one direction to traverse.
    path_dict[(False, True, True, False)] = 1
    path_dict[(False, False, True, True)] = 1
    path_dict[(True, False, False, True)] = 1
    path_dict[(True, True, False, False)] = 1
    path_dict[(True, False, True, False)] = 1
    path_dict[(False, True, False, True)] = 1
    # Cells which have two directions to traverse.
    path_dict[(True, False, True, True)] = 2
    path_dict[(True, True, True, False)] = 2
    path_dict[(False, True, True, True)] = 2
    path_dict[(True, True, False, True)] = 2
    # Cells which have three directions to traverse.
    path_dict[(True, True, True, True)] = 3
    return(path_dict)

def remove_paths(path_list, visit_list):
    """Removes coordinates from the end of 'path_list' until a
    'direction-coordinate list' is encountered."""
    # Removes tuple coordinates and halts when encountered with a list.
    for coordinate in reversed(path_list):
        if type(coordinate) is tuple:
            path_list.remove(coordinate)
        else:
            # Takes note of the 'direction-coordinate list'
            recent_direction = coordinate
            path_list.remove(coordinate)
            break

    # Does not remove the 'direction-coordinate list' to prevent
    # algorithm from traversing back through the same path.
    for coordinate in reversed(visit_list):
        if coordinate != recent_direction:
            visit_list = visit_list[:-1]
        else:
            break
    return(path_list, visit_list)

###############################################################################

if __name__ == '__main__':
    print('Maze Validation')
    # True
    print(is_valid_maze([[(True, True, False, False), (False, False, True, True)], [(False, True, True, False), (True, False, False, True)]]))
    # False
    print(is_valid_maze([[(True, True, False, False)], [(False, True, True, False), (True, False, False, True)]]))
    # False
    print(is_valid_maze([[(True, True, False, False), (False, False, True, False)], [(False, True, True, False), (True, False, False, True)]]))
    # False
    print(is_valid_maze([[(True, True, False, False), (False, False, False, True)], [(False, True, True, False), (False, False, False, True)]]))

    # False
    print(is_valid_maze([]))
    # False
    print(is_valid_maze([[]]))
    # False
    print(is_valid_maze([[], []]))
    # True
    print(is_valid_maze([[(True, False, True, False)]]))
    # False
    print(is_valid_maze([[(True, True, True, False)]]))
    # True
    print(is_valid_maze([[(True, False, True, False)], [(True, False, True, False)]]))
    # False
    print(is_valid_maze([[(True, True, True, False)], [(True, False, True, False)]]))
    # True
    print(is_valid_maze([[(False, True, True, False), (True, True, False, True), (False, False, True, True)], [(True, False, True, False), (False, True, False, False), (True, False, False, True)]]))
    # True
    print(is_valid_maze([[(True, True, True, False), (False, True, False, True), (False, True, False, True), (False, False, True, True)], [(True, False, True, False), (False, True, True, False), (False, False, True, True), (True, False, True, False)], [(True, False, True, False), (True, True, False, False), (True, False, False, True), (True, False, True, False)], [(True, True, False, False), (False, True, False, True), (False, True, False, True), (True, False, True, True)]]))
    # True
    print(is_valid_maze([[(False, False, True, False), (False, True, False, False), (True, True, False, True), (False, False, True, True)], [(True, True, True, False), (False, True, False, True), (False, True, False, True), (True, False, True, True)], [(True, True, True, False), (False, True, False, True), (False, False, True, True), (True, False, True, False)], [(True, True, False, False), (False, True, True, True), (True, False, False, True), (True, False, False, False)]]))
    # True
    print(is_valid_maze([[(True, True, True, False), (False, True, True, True), (False, False, True, True)], [(True, True, True, False), (True, True, True, True), (True, False, True, True)], [(True, True, False, False), (True, True, False, True), (True, False, True, True)]]))

    # False
    print(is_valid_maze([[(True, True, True, False)]]))
    # True
    print(is_valid_maze([[(True, True, True, False), (False, False, False, True), (False, False, True, False)], [(True, False, True, False), (False, False, True, False), (True, False, True, False)], [(True, True, False, False), (True, False, False, True), (True, False, True, False)]]))
    # False
    print(is_valid_maze([[(True,False,True,False),(False,False,False,False)],[(True,False,True,False),(False,False,False,False)]]))
    # True
    print(is_valid_maze([[(True, False, True, False), (False, True, False, False), (False, False, False, True)], [(True, True, False, False), (False, True, False, True), (False, False, True, True)]]))
    # True
    print(is_valid_maze([[(True, False, True, False), (False, True, False, False), (False, True, False, True), (False, False, True, True)], [(True, False, True, False), (False, True, False, False), (False, False, False, True), (True, False, True, False)], [(True, True, False, False), (False, True, False, True), (False, True, False, True), (True, False, True, True)], [(False, True, False, False), (False, True, False, True), (False, True, False, True), (True, False, True, True)]]))
    # True
    print(is_valid_maze([[(True, False, True, False), (False, True, True, False), (False, True, False, True), (False, True, False, True), (False, True, False, True), (False, True, False, True), (False, False, True, True)],[(True, False, True, False), (True, False, True, False), (False, True, False, False), (False, True, False, True), (False, True, False, True), (False, True, False, True), (True, False, True, True)],[(True, True, False, False), (True, False, False, True), (False, True, True, False), (False, True, False, True), (False, True, False, True), (False, True, False, True), (True, False, True, True)],[(False, True, True, False), (False, True, False, True), (True, False, False, True), (False, False, True, False), (False, True, True, False), (False, False, True, True), (True, False, True, False)],[(True, True, True, False), (False, True, False, True), (False, True, False, True), (True, False, False, True), (True, False, True, False), (True, False, True, False), (True, False, True, False)],[(True, True, False, False), (False, True, False, True), (False, True, False, True), (False, True, False, True), (True, False, False, True), (True, False, True, False), (True, False, False, False)]]))
    # True
    print(is_valid_maze([[(True, False, True, False), (False, True, True, False), (False, True, False, True), (False, True, False, True), (False, False, True, True)], [(True, False, True, False), (True, True, False, False), (False, True, False, True), (False, False, True, True), (True, False, False, False)], [(True, True, True, False), (False, True, False, True), (False, True, False, True), (True, True, False, True), (False, False, True, True)], [(True, False, True, False), (False, False, True, False), (False, True, True, False), (False, True, False, True), (True, False, True, True)], [(True, False, True, False), (True, False, True, False), (True, False, True, False), (False, False, True, False), (True, False, True, False)], [(True, True, False, False), (True, False, False, True), (True, True, False, False), (True, False, False, True), (True, False, True, False)], [(False, False, True, False), (False, True, True, False), (False, True, False, True), (False, True, False, True), (True, False, True, True)], [(True, True, False, False), (True, False, False, True), (False, False, True, False), (False, True, True, False), (True, False, True, True)], [(False, True, True, False), (False, True, False, True), (True, True, False, True), (True, False, False, True), (True, False, False, False)]]))
    # True
    print(is_valid_maze([[(True, False, True, False), (False, True, True, False), (False, False, True, True), (False, True, True, False), (False, False, True, True), (False, True, True, False), (False, True, False, True), (False, True, False, True), (False, True, False, True), (False, True, False, True), (False, True, False, True), (False, False, True, True)],[(True, True, False, False), (True, False, False, True), (True, True, False, False), (True, False, False, True), (True, True, True, False), (True, False, False, True), (False, True, True, False), (False, True, True, True), (False, True, False, True), (False, True, False, True), (False, False, True, True), (True, False, True, False)],[(False, True, True, False), (False, True, False, True), (False, True, False, True), (False, True, False, True), (True, False, False, True), (False, True, True, False), (True, False, False, True), (True, True, False, False), (False, True, False, True), (False, False, True, True), (True, False, True, False), (True, False, True, False)],[(True, True, False, False), (False, True, True, True), (False, True, False, True), (False, True, False, True), (False, True, False, True), (True, False, False, True), (False, True, True, False), (False, True, False, True), (False, True, False, True), (True, False, False, True), (True, False, True, False), (True, False, True, False)],[(False, True, True, False), (True, False, True, True), (False, True, False, False), (False, True, False, True), (False, True, False, True), (False, True, False, True), (True, False, False, True), (False, True, True, False), (False, True, False, True), (False, True, False, True), (True, False, False, True), (True, False, True, False)],[(True, False, True, False), (True, True, False, False), (False, True, False, True), (False, True, False, True), (False, True, False, True), (False, True, False, True), (False, True, False, True), (True, False, True, True), (False, True, True, False), (False, True, False, True), (False, True, False, True), (True, False, False, True)],[(True, True, False, False), (False, True, False, True), (False, True, True, True), (False, True, False, True), (False, True, False, True), (False, True, False, True), (False, False, True, True), (True, False, True, False), (True, False, True, False), (False, True, True, False), (False, False, True, True), (False, False, True, False)],[(False, True, True, False), (False, True, False, True), (True, False, True, True), (False, True, False, False), (False, True, True, True), (False, True, False, True), (True, False, False, True), (True, False, True, False), (True, True, True, False), (True, False, False, True), (True, True, False, False), (True, False, True, True)],[(True, True, False, False), (False, False, True, True), (True, True, False, False), (False, False, True, True), (True, True, False, False), (False, True, False, True), (False, True, False, True), (True, False, False, True), (True, True, True, False), (False, True, True, True), (False, False, False, True), (True, False, True, False)],[(False, True, True, False), (True, False, False, True), (False, True, False, False), (True, True, False, True), (False, True, False, True), (False, True, False, True), (False, True, False, True), (False, True, False, True), (True, False, False, True), (True, False, True, False), (False, True, True, False), (True, False, False, True)],[(True, False, True, False), (False, True, True, False), (False, False, True, True), (False, True, True, False), (False, False, True, True), (False, True, True, False), (False, False, True, True), (False, True, True, False), (False, False, True, True), (True, False, True, False), (True, True, True, False), (False, False, True, True)],[(True, True, False, False), (True, False, False, True), (True, True, False, False), (True, False, False, True), (True, True, False, False), (True, False, False, True), (True, True, False, False), (True, False, False, True), (True, True, False, False), (True, False, False, True), (True, False, False, False), (True, False, True, False)]]))

    print('Maze Entry Point')
    # (0, 0)
    print(get_entry_point([[(True, True, False, False), (False, False, True, True)], [(False, True, True, False), (True, False, False, True)]]))
    # (0, 1)
    print(get_entry_point([[(False, True, True, False), (True, True, False, True), (False, False, True, True)], [(True, False, True, False), (False, True, False, False), (True, False, False, True)]]))

    # (0, 2)
    print(get_entry_point([[(False, False, True, False), (False, True, False, False), (True, True, False, True), (False, False, True, True)], [(True, True, True, False), (False, True, False, True), (False, True, False, True), (True, False, True, True)], [(True, True, True, False), (False, True, False, True), (False, False, True, True), (True, False, True, False)], [(True, True, False, False), (False, True, True, True), (True, False, False, True), (True, False, False, False)]]))

    print('Maze Exit Point')
    # (1, 0)
    get_exit_point([[(True, True, False, False), (False, False, True, True)], [(False, True, True, False), (True, False, False, True)]])
    # (2, 2)
    get_exit_point([[(True, True, True, False), (False, False, False, True), (False, False, True, False)], [(True, False, True, False), (False, False, True, False), (True, False, True, False)], [(True, True, False, False), (True, False, False, True), (True, False, True, False)]])
    # (3, 1)
    get_exit_point([[(False, False, True, False), (False, True, False, False), (True, True, False, True), (False, False, True, True)], [(True, True, True, False), (False, True, False, True), (False, True, False, True), (True, False, True, True)], [(True, True, True, False), (False, True, False, True), (False, False, True, True), (True, False, True, False)], [(True, True, False, False), (False, True, True, True), (True, False, False, True), (True, False, False, False)]])

    print('Maze Visualisation')
    # _  __
    # |_  |
    # |  _|
    print(visualise_maze([[(True, True, False, False), (False, False, True, True)], [(False, True, True, False), (True, False, False, True)]]))
    # _  ____
    # |  _  |
    # | | | |
    # |_ _| |
    print(visualise_maze([[(True, True, True, False), (False, True, False, True), (False, False, True, True)], [(True, False, True, False), (False, False, True, False), (True, False, True, False)], [(True, True, False, False), (True, False, False, True), (True, False, True, False)]]))

    # _
    # | |
    print(visualise_maze([[(True, False, True, False)]]))
    # _
    # | |
    # | |
    print(visualise_maze([[(True, False, True, False)], [(True, False, True, False)]]))
    # ___  __
    # |  _  |
    # | |_ _|
    print(visualise_maze([[(False, True, True, False), (True, True, False, True), (False, False, True, True)], [(True, False, True, False), (False, True, False, False), (True, False, False, True)]]))
    # _  ____
    # |  _| |
    # | | | |
    # |_ _| |
    print(visualise_maze([[(True, True, True, False), (False, False, False, True), (False, False, True, False)], [(True, False, True, False), (False, False, True, False), (True, False, True, False)], [(True, True, False, False), (True, False, False, True), (True, False, True, False)]]))
    # _  ____
    # |     |
    # | | | |
    # |_ _| |
    print(visualise_maze([[(True, True, True, False), (False, True, True, True), (False, False, True, True)], [(True, False, True, False), (True, False, True, False), (True, False, True, False)], [(True, True, False, False), (True, False, False, True), (True, False, True, False)]]))
    # ___  __
    # |  _  |
    # |  _  |
    # |_   _|
    print(visualise_maze([[(False, True, True, False), (True, True, False, True), (False, False, True, True)], [(True, True, True, False), (False, True, False, True), (True, False, True, True)], [(True, True, False, False), (False, True, True, True), (True, False, False, True)]]))
    # _____  __
    # | |_ _  |
    # |  _ _  |
    # |  _  | |
    # |_   _|_|
    print(visualise_maze([[(False, False, True, False), (False, True, False, False), (True, True, False, True), (False, False, True, True)], [(True, True, True, False), (False, True, False, True), (False, True, False, True), (True, False, True, True)], [(True, True, True, False), (False, True, False, True), (False, False, True, True), (True, False, True, False)], [(True, True, False, False), (False, True, True, True), (True, False, False, True), (True, False, False, False)]]))

    print('Maze Solution')
    # [(0, 0), (0, 1), (1, 1), (1, 0)]
    print(solve_maze([[(True, True, False, False), (False, False, True, True)], [(False, True, True, False), (True, False, False, True)]]))
    # [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)]
    print(solve_maze([[(True, True, True, False), (False, True, False, True), (False, False, True, True)], [(True, False, True, False), (False, False, True, False), (True, False, True, False)], [(True, True, False, False), (True, False, False, True), (True, False, True, False)]]))
    # None
    print(solve_maze([[(True, True, True, False), (False, False, False, True), (False, False, True, False)], [(True, False, True, False), (False, False, True, False), (True, False, True, False)], [(True, True, False, False), (True, False, False, True), (True, False, True, False)]]))

    # [(0, 1), (0, 0), (1, 0)]
    print(solve_maze([[(False, True, True, False), (True, True, False, True), (False, False, True, True)], [(True, False, True, False), (False, True, False, False), (True, False, False, True)]]))

    print('Shortest Paths')
    # [[(0, 0), (1, 0), (2, 0), (2, 1), (1, 1), (0, 1), (0, 2), (1, 2), (2, 2)]]
    print(shortest_paths([[(True, True, True, False), (False, True, True, True), (False, False, True, True)], [(True, False, True, False), (True, False, True, False), (True, False, True, False)], [(True, True, False, False), (True, False, False, True), (True, False, True, False)]], (1, 1)))
    # None
    print(shortest_paths([[(True, True, True, False), (False, True, False, True), (False, False, True, True)], [(True, False, True, False), (False, False, True, False), (True, False, True, False)], [(True, True, False, False), (True, False, False, True), (True, False, True, False)]], (1, 1)))
    # [[(0, 1), (0, 0), (1, 0), (1, 1), (1, 2), (2, 2), (2, 1)], [(0, 1), (0, 2), (1, 2), (1, 1), (1, 0), (2, 0), (2, 1)]]
    print(shortest_paths([[(False, True, True, False), (True, True, False, True), (False, False, True, True)], [(True, True, True, False), (False, True, False, True), (True, False, True, True)], [(True, True, False, False), (False, True, True, True), (True, False, False, True)]], (1, 1)))

    print(shortest_paths([[(True, True, True, False), (False, True, True, True), (False, False, True, True)], [(True, True, True, False), (True, True, True, True), (True, False, True, True)], [(True, True, False, False), (True, True, False, True), (True, False, True, True)]], (0, 0)))
    print(shortest_paths([[(False, False, True, False), (False, True, False, False), (True, True, False, True), (False, False, True, True)], [(True, True, True, False), (False, True, False, True), (False, True, False, True), (True, False, True, True)], [(True, True, True, False), (False, True, False, True), (False, False, True, True), (True, False, True, False)], [(True, True, False, False), (False, True, True, True), (True, False, False, True), (True, False, False, False)]], (0, 0)))
    print(shortest_paths([[(True, True, True, False), (False, True, False, True), (False, True, False, True), (False, False, True, True)], [(True, False, True, False), (False, True, True, False), (False, False, True, True), (True, False, True, False)], [(True, False, True, False), (True, True, False, False), (True, False, False, True), (True, False, True, False)], [(True, True, False, False), (False, True, False, True), (False, True, False, True), (True, False, True, True)]], (0, 0)))
    print(shortest_paths([[(True, True, True, False), (False, True, True, True), (False, False, True, True)], [(True, True, True, False), (True, True, True, True), (True, False, True, True)], [(True, True, False, False), (True, True, False, True), (True, False, True, True)]], (0, 0)))
    print(shortest_paths([[(True, False, True, False), (False, False, True, False)], [(True, False, False, False), (True, False, True, False)]], (0, 0)))
    print(shortest_paths([[(False, False, True, False), (True, False, True, False), (False, False, True, False)], [(True, True, True, False), (True,  True,  True, True), (True, False, True, True)], [(True, True, False, False), (True,  True,  True, True), (True, False, False, True)]], (0, 0)))
