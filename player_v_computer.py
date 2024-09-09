import pygame
import asyncio
import math
import collections
from random import choice
from collections import deque
from SmartMoveFinder import score_board, findBestMove

RES = WIDTH, HEIGHT = 1200, 900
TILE = 100


pygame.init()
sc = pygame.display.set_mode(RES)
clock = pygame.time.Clock()


class Hexagon:
    def __init__(self, q, r, s, value=0, undo_val=0):
        self.q = q
        self.r = r
        self.s = s
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
        return self.value
    def get_undo_val(self):
        return self.undo_val

    def set_val(self, num):
        self.value = num

    def print_coord(self):
        return (self.q, self.r, self.s)

    def viable_neighbors(self):
        neighbors = []
        for neighbor in self.neighbors:
            for thing in hex_list:
                if Hexagon(neighbor[0], neighbor[1], neighbor[2]).grid == thing.grid:
                    neighbors.append(thing)
        return neighbors

class Strand:
    def __init__(self, tiles):
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
        return self._new_game
    def add_white_piece(self, thing):
        self._white_group.append(thing)
    def sub_valid_move(self, tile):
        self._valid_moves.remove(tile)
    def add_valid_move(self, tile):
        self._valid_moves.append(tile)
    def get_valid_moves(self):
        return self._valid_moves


    def add_black_piece(self, thing):
        self._black_group.append(thing)

    def set_new_game(self, state):
        self._new_game = state

    def get_turn(self):
        return self._turn

    def set_moves(self, num):
        self._moves = num

    def set_type(self, val):
        self._type = val

    def get_type(self):
        return self._type

    def set_first_move(self, status):
        self.first_move = status

    def undo_white_move(self):
        num = self._white_group[-1].get_undo_val()
        step = -1
        for thing in range(0, num):
            self._white_group[step].set_val(num)
            self.add_valid_move(self._white_group[-1])
            self._white_group = self._white_group[:-1]
        return self._white_group, num
    def dec_moves(self):
        self._moves -= 1
        if self._moves == 0 and self._turn == "black":
            self._turn = "white"
            self.first_move = True
        elif self._moves == 0 and self._turn == "white":
            self._turn = "black"
            self.first_move = True


    def findLargestGroup(self):
        if self.get_new_game() == True:
            return {"black": 1, "white": 0}

        first_check = self.black_win_check()
        visited = first_check[0]
        black_list = first_check[1]
        length = len(visited)

        for thing in black_list:
            if thing not in visited:
                group =len(self.black_win_check(thing)[0])
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


        return {"black" : length, "white" : length2}




    def black_win_check(self, start_node=None, black_list=None):
        if black_list is None:
            black_list = self._black_group
        if start_node is None:
            if not black_list:
                return False
            start_node = black_list[0]
        #breadth first search
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
        if white_list is None:
            white_list = self._white_group
        if start_node is None:
            if not white_list:
                return False
            start_node = white_list[0]
        #breadth first search
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

hex_list = []
for q in range(-5, 6):
    for r in range(-5, 6):
        for s in range(-5, 6):
            if (q + r + s) == 0:
                undo_val = 2
                val = 2
                if abs(q) == 4 or abs(r) == 4 or abs(s) == 4:
                    undo_val = 3
                    val = 3
                if 5 in (abs(q), abs(r), abs(s)) and 0 in (abs(q), abs(r), abs(s)):
                    undo_val = 6
                    val = 6
                if 5 in (abs(q), abs(r), abs(s)) and 0 not in (abs(q), abs(r), abs(s)):
                    undo_val = 4
                    val = 4
                if (q, r, s) == (0, 0, 0) or (q, r, s) == (0, -2, +2) or (q, r, s) == (2, 0, -2) or (q, r, s) == (
                -2, 2, 0):
                    undo_val = 1
                    val = 1
                cell = Hexagon(q, r, s, val, undo_val)
                hex_list.append(cell)
Point = collections.namedtuple("Point", ["x", "y"])


def hex_to_pixel(h):
    x = (3 / 2 * h.q) * 38
    y = (math.sqrt(3.0) / 2.0 * h.q + math.sqrt(3.0) * h.r) * 38
    return Point(x + 135, y - 145)


def pixel_to_flat_hex(point):
    q = (2 / 3 * (point[0] - 135)) / 38
    r = (-1 / 3 * (point[0] - 135) + math.sqrt(3) / 3 * (point[1] + 145)) / 38
    return (round(q), round(r))


hi = HEIGHT / 2
wi = WIDTH / 2
def draw_hex(h, size):
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
    mouse_pos = pygame.mouse.get_pos()
    mouse_list = [mouse_pos[0], mouse_pos[1]]
    mouse_list[0] = mouse_pos[0] - hi
    mouse_list[1] = mouse_pos[1] - wi
    new_mouse_pos = pixel_to_flat_hex(mouse_list)
    return new_mouse_pos


game1 = Strand(hex_list)
turn_color = game1.get_turn()
old_val = 2

async def main():
    while True:
        sc.fill(pygame.Color('thistle1'))
        turn_color = game1.get_turn()
        if turn_color == "white":
            new_mouse_pos = pixel_to_flat_hex(hex_to_pixel(findBestMove(game1.get_valid_moves(), game1)))
            for thing in hex_list:
                if thing.print_coord()[0] == new_mouse_pos[0]:
                    if thing.print_coord()[1] == new_mouse_pos[1]:
                        if game1.first_move != True and thing.get_val() != old_val:
                            continue

                        if thing.get_val() == 7 or thing.get_val() == 8:
                            continue


                        elif turn_color == "white":
                            old_val = thing.get_val()
                            game1.set_type(old_val)
                            pygame.time.delay(300)
                            thing.set_val(8)
                            game1.add_white_piece(thing)
                            game1.sub_valid_move(thing)
                            print(len(game1._valid_moves))




                        if game1.first_move == True:
                            game1.set_moves(old_val)
                            game1.set_first_move(False)

                        game1.dec_moves()
                        #print(game1.findLargestGroup())



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                turn_color = game1.get_turn()
                if turn_color == "white":
                    continue
                else:
                    new_mouse_pos = get_mouse()
                for thing in hex_list:
                    if thing.print_coord()[0] == new_mouse_pos[0]:
                        if thing.print_coord()[1] == new_mouse_pos[1]:
                            if game1.first_move != True and thing.get_val() != old_val:
                                continue
                            if game1.get_new_game() == True and thing.get_val() != 2:
                                continue
                            if thing.get_val() == 7 or thing.get_val() == 8:
                                continue
                            if turn_color == "black":
                                old_val = thing.get_val()
                                thing.set_val(7)
                                game1.add_black_piece(thing)
                                game1.sub_valid_move(thing)


                                print(score_board(game1))

                                #print(game1.findLargestGroup())



                            if game1.first_move == True:
                                game1.set_moves(old_val)
                                game1.set_first_move(False)
                            if game1.get_new_game() == True:
                                game1.dec_moves()
                                game1.set_new_game(False)
                            game1.dec_moves()

        for thing in hex_list:
            draw_hex(thing, 35)

        pygame.display.flip()
        clock.tick(1000)
        await asyncio.sleep(0)
asyncio.run(main())
