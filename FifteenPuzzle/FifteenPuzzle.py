"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods
    def position_tile(self, target_row, target_col, end_loc = None, end_zero_pos = None):
        """
        Returns a sequence of moves to position target tile in targeted space
        """
        def is_zero_below(zero_pos, location):
            """
            Checks whether zero in position below target tile. Returns a boolean.
            """
            if zero_pos[1] == location[1]:
                return True
            else:
                return False
        
        def update(self, move):
            """
            Updates puzzle with given move.
            """
            self.update_puzzle(move)
            return move
        
        if end_loc == None:
            end_loc = (target_row, target_col)
        if end_zero_pos == None:
            end_zero_pos = [target_row, target_col - 1]
            
        move = ""
        total_moves = ""
        location = self.current_position(target_row, target_col)
        zero_pos = self.current_position(0, 0)
        
        while location != end_loc:
            location = self.current_position(target_row, target_col)
            zero_pos = self.current_position(0, 0)
            
            # x in correct col
            if location[1] == end_loc[1] and location[0] != end_loc[0]:
                v_dist = abs(zero_pos[0] - location[0])
                for dummy_move in range(v_dist):
                    move += "u"
                total_moves += update(self, move)
                move = ""
                location = self.current_position(target_row, target_col)
                zero_pos = self.current_position(0, 0)
                
                if is_zero_below(zero_pos, location):
                    move += "ld"
                total_moves += update(self, move)
                move = ""
                location = self.current_position(target_row, target_col)
                zero_pos = self.current_position(0, 0)
                    
                # reposition 0 under x
                if location[0] != end_loc[0]:
                    if location[0] > end_loc[0]:
                        if zero_pos[0] == location[0]:
                            if zero_pos[1] == location[1] - 1:
                                move += "urd"
                            elif zero_pos[1] == location[1] + 1:
                                move += "uld"
                    elif location[0] < end_loc[0]:
                        if zero_pos[1] > location[1]:
                            if zero_pos[0] != 0:
                                move += "ullddr"
                            else:
                                move += "dl"
                        else:
                            move += "dr"
                    total_moves += update(self, move)
                    move = ""
                    location = self.current_position(target_row, target_col)
                    zero_pos = self.current_position(0, 0)
                        
            # if x not in correct col    
            elif location[1] != end_loc[1]:
                if location[0] < zero_pos[0]:
                    v_dist = abs(zero_pos[0] - location[0])
                    for dummy_move in range(v_dist):
                        move += "u"
                    total_moves += update(self, move)
                    move = ""
                    location = self.current_position(target_row, target_col)
                    zero_pos = self.current_position(0, 0)
                
                if location[1] > zero_pos[1] and location[1] > end_loc[1]:
                    for dummy_move in range(abs(location[1] - zero_pos[1])):
                        move += "r"
                elif location[1] < zero_pos[1] and location[1] < end_loc[1]:
                    for dummy_move in range(abs(location[1] - zero_pos[1])):
                        move += "l"
                total_moves += update(self, move)
                move = ""
                location = self.current_position(target_row, target_col)
                zero_pos = self.current_position(0, 0)
                
                # if col is wrong
                if location[1] < zero_pos[1] and location[1] != end_loc[1]:
                    move += "ul"
                    if location[1] != end_loc[1]:
                        move += "ld"
                elif location[1] > zero_pos[1] and location[1] != end_loc[1]:
                    move += "ur"
                    if location[1] != end_loc[1]:
                        move += "rd"
                
                # if top row
                if location[0] == 0:
                    move = move.replace("d", "u")
                    move = move.replace("u", "d", 1)
                total_moves += update(self, move)
                move = ""
                location = self.current_position(target_row, target_col)
                zero_pos = self.current_position(0, 0)
                    
                if location[0] > zero_pos[0]:
                    move += "ld"
                    if location[1] == 0:
                        move = move.replace("l", "r")

            total_moves += update(self, move)
            move = ""
            location = self.current_position(target_row, target_col)
            zero_pos = self.current_position(0, 0)
        
        # getting 0 into final position to satisfy invariants   
        if location == (end_loc) and zero_pos != end_zero_pos:
            total_moves += self.final_0_pos(zero_pos, end_zero_pos) 
        
        return total_moves
        
    def final_0_pos(self, zero_pos, end_zero_pos):
        """
        Returns move to place 0 in final position to satisfy invariants
        """
        print end_zero_pos
        
        v_dist = abs(zero_pos[0] - end_zero_pos[0])
        h_dist = abs(zero_pos[1] - end_zero_pos[1])
        move = ""
        total_moves = ""
        done = False
        while not done:
            if zero_pos[0] > end_zero_pos[0]:
                for dummy_move in range(v_dist):
                    move += "u"
                total_moves += move
                self.update_puzzle(move)
                move = ""
                zero_pos = self.current_position(0, 0)
            elif zero_pos[0] < end_zero_pos[0]:
                for dummy_move in range(end_zero_pos[0] - zero_pos[0]):
                    move += "d"
                total_moves += move
                self.update_puzzle(move)
                move = ""
                zero_pos = self.current_position(0, 0)
            elif zero_pos[1] != end_zero_pos[1]:
                if zero_pos[1] > end_zero_pos[1]:
                    for dummy_move in range(h_dist):
                        move += "l"
                    total_moves += move
                    self.update_puzzle(move)
                    move = ""
                    zero_pos = self.current_position(0, 0)
                elif zero_pos[1] < end_zero_pos[1]:
                    for dummy_move in range(h_dist):
                        move += "r"
                    total_moves += move
                    self.update_puzzle(move)
                    move = ""
                    zero_pos = self.current_position(0, 0)
            
            if zero_pos[0] == end_zero_pos[0]:
                if zero_pos[1] == end_zero_pos[1]:
                    done = True
            
        return total_moves
                            
    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        # replace with your code

        for index_row in range( self._height - target_row ):
            for col in range( self._width ):
                #check the same row, the right part of the target point
                if index_row == 0:
                    if col == target_col:
                        #check the target point
                        if self._grid[ target_row ][ target_col ] != 0:
                            return False
                    #check the rest column in this row
                    elif col > target_col:
                        if self._grid[ target_row ][ col ] != self._width * target_row + col:
                            return False
                else:
                    if self._grid[ target_row + index_row ][ col ] != self._width * ( target_row + index_row ) + col:
                        return False
        return True
        
    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        # replace with your code
        #check condition
        move_string = ''
        assert target_row > 1
        assert target_col > 0
        assert self.lower_row_invariant(target_row, target_col)
        #find the position of that number
        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == self._width * target_row + target_col:
                    temp = (row , col)
        #move 0 to the position if number is on the target row
        #0 goes left first
        if target_col > temp[1]:
            move_string += (target_col - temp[1]) * 'l'
            #if the number is on the up-left side
            if target_row > temp[0]:
                move_string += (target_row - temp[0]) * 'u'
                #check right loop down or left loop down,left first
                if temp[1] > 0:
                    move_string += (target_row - temp[0] - 1) * 'lddru'
                    move_string += 'rdl'
                elif temp[1] == 0:
                    move_string += (target_row - temp[0] - 1) * 'rddlu'
                    move_string += 'rdl'
            move_string += (target_col - temp[1] - 1) * 'urrdl'        
        #0 goes upside first
        elif target_col <= temp[1]:
            move_string += (target_row - temp[0]) * 'u'
            #if the number is on the up-right side
            if target_col < temp[1]: 
                move_string += (temp[1] - target_col) * 'r'
                #check up loop or down loop to left, up first
                if temp[0] > 0:
                    move_string += (temp[1] - target_col - 1) * 'ulldr'
                    move_string += 'dlu'
                elif temp[0] == 0:
                    move_string += (temp[1] - target_col - 1) * 'dllur'
                    move_string += 'dlu'
            move_string += (target_row - temp[0] - 1) * 'lddru'
            move_string += 'ld'
        #print move_string
        self.update_puzzle(move_string)
        assert self.lower_row_invariant(target_row, target_col - 1)
        return move_string
            
    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        #move target number to position (target_row - 1, 1)
        assert target_row > 1
        move_string = ''
        self.update_puzzle('ur')
        #check whether the number is in the position
        if self._grid[target_row][0] == self._width * target_row:
            move_string += (self._width - 2) * 'r'
            self.update_puzzle(move_string)
            assert self.lower_row_invariant(target_row - 1, self._width - 1)
            return 'ur' + move_string
        #find the position of that number
        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == self._width * target_row:
                    temp = (row , col)
        #reset 0 pos        
        temp_row = target_row - 1
        temp_col = 1
        #use the interior method for moving
        if temp_col > temp[1]:
            move_string += (temp_col - temp[1]) * 'l'
            #if the number is on the up-left side
            if temp_row > temp[0]:
                move_string += (temp_row - temp[0]) * 'u'
                #check right loop down or left loop down,left first
                if temp[1] > 0:
                    move_string += (temp_row - temp[0] - 1) * 'lddru'
                    move_string += 'rdl'
                elif temp[1] == 0:
                    move_string += (temp_row - temp[0] - 1) * 'rddlu'
                    move_string += 'rdl'
            move_string += (temp_col - temp[1] - 1) * 'urrdl'        
        #0 goes upside first
        elif temp_col <= temp[1]:
            move_string += (temp_row - temp[0]) * 'u'
            #if the number is on the up-right side
            if temp_col < temp[1]: 
                move_string += (temp[1] - temp_col) * 'r'
                #check up loop or down loop to left, up first
                if temp[0] > 0:
                    move_string += (temp[1] - temp_col - 1) * 'ulldr'
                    move_string += 'dlu'
                elif temp[0] == 0:
                    move_string += (temp[1] - temp_col - 1) * 'dllur'
                    move_string += 'dlu'
            move_string += (temp_row - temp[0] - 1) * 'lddru'
            move_string += 'ld'
        #target number at position(targe_row - 1, 1), 0 at (target_row - 1, 0)
        #after move string below, target number at right pos, 0 at (targe_row - 1, 1)
        move_string += 'ruldrdluruldrulddruulddru'
        move_string += (self._width - 2) * 'r'
        self.update_puzzle(move_string)
        assert self.lower_row_invariant(target_row - 1, self._width - 1)
        return 'ur' + move_string  
    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if self._grid[0][target_col] != 0:
            return False
        
        portion = 1
        for idx in range(2):
            right = self._grid[idx]
            col = len(right[target_col + portion:])
            for val in right[target_col + portion:]:
                tile = self._width + (idx * self._width) - col
                if val != tile:
                    return False
                col -= 1
            portion -= 1
        
        for idx in range(2, self._height):
            row = self._grid[idx]
            col = self._width
            for val in row:
                tile = self._width + (idx * self._width) - col
                if val != tile:
                    return False
                col -= 1
                
        return True
    
    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if self._grid[1][target_col] != 0:
            return False
        
        for idx in range(2):
            right = self._grid[idx]     
            col = len(right[target_col + 1:])
            for val in right[target_col + 1:]:
                tile = self._width + (idx * self._width) - col
                if val != tile:
                    return False
                col -= 1
                
        for idx in range(2, self._height):
            row = self._grid[idx]
            col = self._width
            for val in row:
                tile = self._width + (idx * self._width) - col
                if val != tile:
                    return False
                col -= 1
                
        return True

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row0_invariant(target_col)
        
        location = self.current_position(0, target_col)
        zero_pos = self.current_position(0, 0)
        total_moves = ""
        move = ""
        
        while location != (0, target_col):
            if location[0] == 0 and location[1] == target_col - 1 and self.row0_invariant(target_col):
                move += "ld"
                self.update_puzzle(move)
                total_moves += move
                move = ""
                location = self.current_position(0, target_col)
                zero_pos = self.current_position(0, 0)
                break
          
            if location[0] > zero_pos[0] and location[1] < zero_pos[1]:
                for dummy_move in range(zero_pos[1] - location[1]):
                    move += "l"
                for dummy_move in range(abs(zero_pos[0] - location[0])):
                    move += "d"
                total_moves += move
                self.update_puzzle(move)
                move = ""
                location = self.current_position(0, target_col)
                zero_pos = self.current_position(0, 0)
            
                if location[1] != target_col - 1:
                    move += "ruldr"
                    total_moves += move
                    self.update_puzzle(move)
                    move = ""
                    location = self.current_position(0, target_col)
                    zero_pos = self.current_position(0, 0)
              
            if location[0] == 0 and location[1] == target_col - 1:
                move += "uldrurdluldruldrruld"
                self.update_puzzle(move)
                total_moves += move
                move = ""
                location = self.current_position(0, target_col)
                zero_pos = self.current_position(0, 0)
            
            else:
                move_sequence = self.position_tile(0, target_col, (0, target_col - 1), (1, target_col - 1))
                total_moves += move_sequence
                move = ""
                location = self.current_position(0, target_col)
                zero_pos = self.current_position(0, 0)
               
        assert self.row1_invariant(target_col - 1)
        return total_moves

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row1_invariant(target_col)
        move_string = ''
        #find the position of that number
        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == self._width + target_col:
                    temp = (row , col)
        #0 goes left first
        if target_col > temp[1]:
            move_string += (target_col - temp[1]) * 'l'
            #if the number is on the up-left side
            if temp[0] == 0:
                move_string += 'urdl'
            move_string += (target_col - temp[1] - 1) * 'urrdl'
            move_string += 'ur'
        elif target_col == temp[1]:
            move_string += 'u'
        self.update_puzzle(move_string)
        assert self.row0_invariant(target_col)
        return move_string
    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        # replace with your code
        assert self.row1_invariant(1)
        
        total_moves = ""
        sequence = ["l", "u", "r", "d"]
        
        row0 = [val for val in range(self._width)]
        row1 = [val + self._width for val in range(self._width)]
        
        while self._grid[0] != row0 and self._grid[1] != row1:
            for move in sequence:
                total_moves += move
                self.update_puzzle(move)
                if self._grid[0] == row0 and self._grid[1] == row1:
                    break
                    
        return total_moves
    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        # replace with your code
        return ""

# Start interactive simulation
poc_fifteen_gui.FifteenGUI(Puzzle(4, 4))

