import pygame
import asyncio
import math
import collections
from random import choice

RES = WIDTH, HEIGHT = 1200, 900
TILE = 100


pygame.init()
sc = pygame.display.set_mode(RES)
clock = pygame.time.Clock()


class Hexagon:
    def __init__(self, q, r, s, value=0):
        self.q = q
        self.r = r
        self.s = s
        self.grid = (q, r, s)
        self.empty = True
        self.value = value
        self.neighbors = [(self.q, self.r + 1, self.s - 1),
                          (self.q, self.r - 1, self.s + 1),
                          (self.q + 1, self.r - 1, self.s),
                          (self.q + 1, self.r, self.s - 1),
                          (self.q - 1, self.r + 1, self.s),
                          (self.q - 1, self.r, self.s + 1)]

    def get_val(self):
        return self.value

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
        self._moves = 1
        self._turn = "black"
        self.first_move = True
        self._new_game = True
        self._black_group = []
        self._white_group = []

    def get_new_game(self):
        return self._new_game

    def set_new_game(self, state):
        self._new_game = state

    def get_turn(self):
        return self._turn

    def set_moves(self, num):
        self._moves = num

    def set_first_move(self, status):
        self.first_move = status
    def dec_moves(self):
        self._moves -= 1
        if self._moves == 0 and self._turn == "black":
            self._turn = "white"
            self.first_move = True
        elif self._moves == 0 and self._turn == "white":
            self._turn = "black"
            self.first_move = True
hex_list = []
for q in range(-5, 6):
    for r in range(-5, 6):
        for s in range(-5, 6):
            if (q + r + s) == 0:
                val = 2
                if abs(q) == 4 or abs(r) == 4 or abs(s) == 4:
                    val = 3
                if 5 in (abs(q), abs(r), abs(s)) and 0 in (abs(q), abs(r), abs(s)):
                    val = 6
                if 5 in (abs(q), abs(r), abs(s)) and 0 not in (abs(q), abs(r), abs(s)):
                    val = 4
                if (q, r, s) == (0, 0, 0) or (q, r, s) == (0, -2, +2) or (q, r, s) == (2, 0, -2) or (q, r, s) == (
                -2, 2, 0):
                    val = 1
                cell = Hexagon(q, r, s, val)
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
            new_mouse_pos = pixel_to_flat_hex(hex_to_pixel(choice(hex_list)))
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

                        elif turn_color == "white":
                            old_val = thing.get_val()
                            pygame.time.delay(900)
                            thing.set_val(8)

                        if game1.first_move == True:
                            game1.set_moves(old_val)
                            game1.set_first_move(False)
                        if game1.get_new_game() == True:
                            game1.dec_moves()
                            game1.set_new_game(False)
                        game1.dec_moves()


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

                            elif turn_color == "white":
                                old_val = thing.get_val()
                                thing.set_val(8)

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
