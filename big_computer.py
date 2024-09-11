import pygame
import math
import collections
from collections import deque
from SmartMoveFinder import findBestMove

RES = WIDTH, HEIGHT = 1200, 900
TILE = 100


pygame.init()
sc = pygame.display.set_mode(RES)
clock = pygame.time.Clock()


class Hexagon:
    def __init__(self, q_coord, r_coord, s_coord, value=0, undo_val=0):
        """initializes class"""
        self.q = q_coord
        self.r = r_coord
        self.s = s_coord
        self.grid = (q, r, s)
        self.empty = True
        self.value = value
        self.undo_val = undo_val
        self.neighbors = [(self.q, self.r + 1, self.s - 1),
                          (self.q, self.r - 1, self.s + 1),
                          (self.q + 1, self.r - 1, self.s),
                          (self.q + 1, self.r, self.s - 1),
                          (self.q - 1, self.r + 1, self.s),
                          (self.q - 1, self.r, self.s + 1)]

    def get_val(self):
        """returns value of tile"""
        return self.value

    def get_undo_val(self):
        """returns undo value"""
        return self.undo_val

    def set_val(self, num):
        """sets value of tile"""
        self.value = num

    def print_coord(self):
        """returns (q,r,s) coordinates of tile"""
        return self.q, self.r, self.s

    def viable_neighbors(self):
        """returns neighbors of tile that exist in the grid"""
        neighbors = []
        for neighbor in self.neighbors:
            if neighbor in hex_list_grid:
                place = hex_list_grid.index(neighbor)
                neighbors.append(hex_list[place])
        return neighbors


class Strand:
    def __init__(self, tiles):
        """initializes class"""
        self._tiles = tiles
        self._type = 2
        self._moves = 1
        self._turn = "black"
        self.first_move = True
        self._new_game = True
        self._black_group = []
        self._white_group = []
        self._valid_moves = tiles.copy()

    def get_new_game(self):
        """returns if game is new"""
        return self._new_game

    def get_white_group(self):
        return self._white_group

    def add_white_piece(self, pos):
        """adds a piece to white moves"""
        self._white_group.append(pos)

    def sub_valid_move(self, tile):
        """deletes a value from valid moves list"""
        self._valid_moves.remove(tile)

    def add_valid_move(self, tile):
        """adds a value to valid move list"""
        self._valid_moves.append(tile)

    def get_valid_moves(self):
        """gets valid moves"""
        return self._valid_moves

    def add_black_piece(self, pos):
        """adds black piece to list"""
        self._black_group.append(pos)

    def set_new_game(self, state):
        """sets new game"""
        self._new_game = state

    def get_turn(self):
        """gets player turn"""
        return self._turn

    def set_moves(self, num):
        """sets number of moves"""
        self._moves = num

    def set_type(self, pos):
        """sets type"""
        self._type = pos

    def get_type(self):
        """gets type"""
        return self._type

    def set_first_move(self, status):
        """sets first move"""
        self.first_move = status

    def make_move(self, space, color):
        """takes a tile and color and sets that tile to that color, and deletes that from valid moves and
        adds it to the correct black or white list"""
        self.set_type(space.get_val())
        space.set_val(color)
        self.sub_valid_move(space)
        if color == 8:
            self._white_group.append(space)
        elif color == 7:
            self._black_group.append(space)
        if game1.first_move is True:
            game1.set_moves(space.get_undo_val())
            game1.set_first_move(False)
        if game1.get_new_game() is True:
            game1.dec_moves()
            game1.set_new_game(False)
        game1.dec_moves()

    def undo_white_move(self):
        """undoes white moves in sequence, until all the stones they have played during their last turn are removed,
        and adds them back into valid moves, and deletes them from white list data member"""
        num = self._white_group[-1].get_undo_val()
        step = -1
        for pos in range(0, num):
            self._white_group[step].set_val(num)
            self.add_valid_move(self._white_group[-1])
            self._white_group = self._white_group[:-1]
        return self._white_group, num

    def undo_black_move(self):
        """undoes black moves in sequence, until all the stones they have played during their last turn are removed,
        and adds them back into valid moves, and deletes them from black list data member"""
        num = self._black_group[-1].get_undo_val()
        step = -1
        for pos in range(0, num):
            self._black_group[step].set_val(num)
            self.add_valid_move(self._black_group[-1])
            self._black_group = self._black_group[:-1]
        return self._black_group, num

    def dec_moves(self):
        """decreases the amount of moves a player gets by one each stone they place, when it reaches zero, switches
        the turn to the opposite players color and sets first move to True"""
        self._moves -= 1
        if self._moves == 0 and self._turn == "black":
            self._turn = "white"
            self.first_move = True
        elif self._moves == 0 and self._turn == "white":
            self._turn = "black"
            self.first_move = True

    def find_largest_group(self):
        """passes the first value from black list and white list into their respective breadth first searches, if there
        are any remaining unvisited stones, reruns using those stones as starting place,
        returns the largest group of each color"""
        if self.get_new_game() is True:
            return {"black": 1, "white": 0}
        first_check = self.black_win_check()
        visited = first_check[0]
        black_list = first_check[1]
        length = len(visited)
        for pos in black_list:
            if pos not in visited:
                group = len(self.black_win_check(pos)[0])
                if group > length:
                    length = group
        second_check = self.white_win_check()
        visited2 = second_check[0]
        white_list = second_check[1]
        length2 = len(visited2)
        for value in white_list:
            if value not in visited2:
                group2 = len(self.white_win_check(value)[0])
                if group2 > length2:
                    length2 = group2
        return {"black": length, "white": length2}

    def black_win_check(self, start_node=None, black_list=None):
        """Uses a breadth first search to find the largest grouping of black stones"""
        if black_list is None:
            black_list = self._black_group
        if start_node is None:
            if not black_list:
                return False
            start_node = black_list[0]
        visited = set()
        queue = deque([start_node])
        visited.add(start_node)
        while queue:
            node = queue.popleft()
            for neighbor in node.viable_neighbors():
                if neighbor in black_list and neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return [visited, black_list]

    def white_win_check(self, start_node=None, white_list=None):
        """uses a breadth first search to find the largest group of white stones"""
        if white_list is None:
            white_list = self._white_group
        if start_node is None:
            if not white_list:
                return False
            start_node = white_list[0]
        visited = set()
        queue = deque([start_node])
        visited.add(start_node)
        while queue:
            node = queue.popleft()
            for neighbor in node.viable_neighbors():
                if neighbor in white_list and neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return [visited, white_list]


# create grid of hexagons to be passed into new strand game
hex_list = []
for q in range(-6, 7):
    for r in range(-6, 7):
        for s in range(-6, 7):
            if (q + r + s) == 0:
                val = 2
                if 4 in (abs(q), abs(r), abs(s)) and -2 and 2 not in (abs(q), abs(r), abs(s)):
                    val = 3
                if 6 in (abs(q), abs(r), abs(s)):
                    if 0 in (abs(q), abs(r), abs(s)):
                        val = 6
                    elif q in (-1,0,1):
                        val = 6
                    elif r in (-1,0,1):
                        val = 6
                    elif s in (-1,0,1):
                        val = 6
                    else:
                        val = 4
                if 5 in (abs(q), abs(r), abs(s)) and 6 not in (abs(q), abs(r), abs(s)):
                    if 0 in (abs(q), abs(r), abs(s)):
                        val = 4
                    elif q in (-1,0,1):
                        val = 4
                    elif r in (-1,0,1):
                        val = 4
                    elif s in (-1,0,1):
                        val = 4
                    else:
                        val = 3

                if (q, r, s) == (0, 0, 0) or (q, r, s) == (0, -2, +2) or (q, r, s) == (2, 0, -2) or (q, r, s) == (
                        -2, 2, 0):
                    val = 1
                cell = Hexagon(q, r, s, val, val)
                hex_list.append(cell)
Point = collections.namedtuple("Point", ["x", "y"])
hex_list_grid = [square.grid for square in hex_list]


# Helper functions for printing hexagon grid
def hex_to_pixel(h):
    """converts hex grid to pixel screen location"""
    x = (3 / 2 * h.q) * 38
    y = (math.sqrt(3.0) / 2.0 * h.q + math.sqrt(3.0) * h.r) * 38
    return Point(x + 135, y - 145)


def pixel_to_flat_hex(point):
    """converts pixel screen location to hex grid"""
    q_coord = (2 / 3 * (point[0] - 135)) / 38
    r_coord = (-1 / 3 * (point[0] - 135) + math.sqrt(3) / 3 * (point[1] + 145)) / 38
    return round(q_coord), round(r_coord)


hi = HEIGHT / 2
wi = WIDTH / 2


def draw_hex(h, size):
    """calculates coordinates and draws the polygons with appropriate color"""
    color_map = {
        3: "sandybrown",
        6: "lightgreen",
        4: "mediumorchid1",
        1: "palevioletred",
        7: "black",
        8: "white"
    }

    color = color_map.get(h.value, "lightblue")
    coord = hex_to_pixel(h)
    # Calculate points for hexagon vertices
    points = [(coord.x + size * math.sin(3.14 / 2) + hi, coord.y + size * math.cos(3.14 / 2) + wi),
              (coord.x + size * math.sin(3.14 / 6) + hi, coord.y + size * math.cos(3.14 / 6) + wi),
              (coord.x + size * math.sin(11 * 3.14 / 6) + hi, coord.y + size * math.cos(11 * 3.14 / 6) + wi),
              (coord.x + size * math.sin(3 * 3.14 / 2) + hi, coord.y + size * math.cos(3 * 3.14 / 2) + wi),
              (coord.x + size * math.sin(7 * 3.14 / 6) + hi, coord.y + size * math.cos(7 * 3.14 / 6) + wi),
              (coord.x + size * math.sin(5 * 3.14 / 6) + hi, coord.y + size * math.cos(5 * 3.14 / 6) + wi)]
    pygame.draw.polygon(sc, pygame.Color(color), points)


def get_mouse():
    """takes a mouse click location and converts to hex grid location"""
    mouse_pos = pygame.mouse.get_pos()
    mouse_list = [mouse_pos[0] - hi, mouse_pos[1] - wi]
    mouse = pixel_to_flat_hex(mouse_list)
    return mouse


# Creates a game and sets first turn as black
game1 = Strand(hex_list)

while True:
    sc.fill(pygame.Color('thistle1'))
    if game1.get_turn() == "white":
        new_mouse_pos = pixel_to_flat_hex(hex_to_pixel(findBestMove(game1.get_valid_moves(), game1)))
        for thing in hex_list:
            if (thing.print_coord()[0], thing.print_coord()[1]) == (new_mouse_pos[0], new_mouse_pos[1]):
                if not game1.first_move and thing.get_val() != game1.get_type():
                    continue
                if thing.get_val() == 7 or thing.get_val() == 8:
                    continue
                pygame.time.delay(300)
                game1.make_move(thing, 8)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game1.get_turn() == "white":
                continue
            else:
                new_mouse_pos = get_mouse()
            for thing in hex_list:
                if (thing.print_coord()[0], thing.print_coord()[1]) == (new_mouse_pos[0], new_mouse_pos[1]):
                    if not game1.first_move and thing.get_val() != game1.get_type():
                        continue
                    if game1.get_new_game() and thing.get_val() != 2:
                        continue
                    if thing.get_val() == 7 or thing.get_val() == 8:
                        continue
                    print(game1.find_largest_group())
                    game1.make_move(thing, 7)


    for thing in hex_list:
        draw_hex(thing, 35)

    pygame.display.flip()
    clock.tick(1000)
