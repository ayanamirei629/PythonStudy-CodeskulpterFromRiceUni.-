"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        self._zombie_list = []
        self._human_list = []
        poc_grid.Grid.clear(self)
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row,col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)     
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        # replace with an actual generator
        for zombie in self._zombie_list:
            yield zombie
            

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row,col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        # replace with an actual generator
        for human in self._human_list:
            yield human
        
    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        visited = poc_grid.Grid(self._grid_height, self._grid_width)

        distance_field = [[self._grid_width * self._grid_height \
                                for dummy_col in range(self._grid_width)]  \
                                    for dummy_row in range(self._grid_height)]   
        boundary = poc_queue.Queue()
        #DEFINE THE INITIAL POINT TO COMPUTE THE DISTANCE        
        if entity_type == HUMAN:
            for human in self._human_list:
                boundary.enqueue(human)
                visited.set_full(human[0],human[1])
                distance_field[human[0]][human[1]] = 0
        elif entity_type == ZOMBIE:
            for zombie in self._zombie_list:
                boundary.enqueue(zombie)
                visited.set_full(zombie[0],zombie[1])
                distance_field[zombie[0]][zombie[1]] = 0
       
        #BFS method
        while len(boundary) > 0:
            cell = boundary.dequeue()
            neighbors = visited.four_neighbors(cell[0],cell[1])
            for neighbor in neighbors:
                if visited.is_empty(neighbor[0],neighbor[1]) and \
                   self.is_empty(neighbor[0],neighbor[1]):
                        visited.set_full(neighbor[0],neighbor[1])
                        boundary.enqueue(neighbor)
                        distance_field[neighbor[0]][neighbor[1]] = \
                        distance_field[cell[0]][cell[1]] +1
        
        return distance_field
                
    
    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        board = zombie_distance_field
        new_human_list = []
        
        
        #check each human with its eight neighbor, the maximun number on the board which calculated by BFS method should
        #be the right choice
        for human in self._human_list:
            human_neighbors = self.eight_neighbors(human[0],human[1])
            distance = board[human[0]][human[1]]
            temp_pos = (human[0], human[1])
            for human_neighbor in human_neighbors:
                if self.is_empty(human_neighbor[0],human_neighbor[1]) and \
                    board[human_neighbor[0]][human_neighbor[1]] > distance:               
                    distance = board[human_neighbor[0]][human_neighbor[1]]
                    temp_pos = (human_neighbor[0], human_neighbor[1])
            new_human_list.append(temp_pos)
        self._human_list = new_human_list
        return
    
    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        #store and record list during moving zombies
        board = human_distance_field       
        new_zombie_list = []
        
        
        #check each zombie with its four neighbor, the minimun number on the board which calculated by BFS method should
        #be the right choice
        for zombie in self._zombie_list:
            zombie_neighbors = self.four_neighbors(zombie[0],zombie[1])
            distance = board[zombie[0]][zombie[1]]
            temp_pos = (zombie[0],zombie[1])
            for zombie_neighbor in zombie_neighbors:
                if self.is_empty(zombie_neighbor[0], zombie_neighbor[1]) and \
                    board[zombie_neighbor[0]][zombie_neighbor[1]] < distance:
                    distance = board[zombie_neighbor[0]][zombie_neighbor[1]]
                    temp_pos = (zombie_neighbor[0], zombie_neighbor[1])
            new_zombie_list.append(temp_pos)
        self._zombie_list = new_zombie_list
        return

# Start up gui for simulation - You will need to write some code above
# before this will work without errors

# poc_zombie_gui.run_gui(Apocalypse(30, 40))
