from dataclasses import dataclass
from enum import Enum
from collections import namedtuple
from random import seed, shuffle
from itertools import product
import random

seed(1)

Piece = namedtuple('Piece', ['name', 'size'])

class Ship(Enum):
    Ship2 = Piece('destroyer', 2)
    Ship4 = Piece('battleship', 4)
    
    @property
    def size(self):
        return self.value.size
    
    @property
    def name(self):
        return self.value.name
    
allow_ships = {Ship.Ship2, Ship.Ship4}

@dataclass(frozen=True)
class Miss:
    pass

@dataclass(frozen=True)
class Hit:
    ship : Ship

@dataclass(frozen=True)
class Sinking(Hit):
    pass


def check_and_place(cord, ship, field, ships):
    x, y = cord
    if (x + ship.size >= len(field)): return 0
    for i in range(ship.size):
        for dx, dy in product((-1, 0, 1), repeat=2):
            if not (0 <= x + dx + i < len(field) and 0 <= y + dy < len(field[0])): continue
            if (field[x + dx + i][y + dy] != 0): return 0
    for i in range(ship.size):
        field[x + i][y] = 1
    ships[ship] = {(x + i, y) for i in range(ship.size)}
    return 1



@dataclass
class Board:
    size : tuple
    ships : dict

    def __post_init__(self):
        self.layout = {
                       pos: ship 
                       for ship, positions in self.ships.items()
                       for pos in positions
                       }
        self.state = {ship: set() for ship in self.ships}

    @classmethod
    def from_random(cls, *, size=(9, 9), pieces=frozenset({*Ship})):
        targets = [*product(range(size[0]), range(size[1]))]
        field = [[0 for i in range(size[0])] for j in range(size[1])]
        shuffle(targets)
        tgt = allow_ships.copy()
        ships = {}
        for ship in tgt:
            for cord in targets:
                if check_and_place(cord, ship, field, ships) != 0:
                    break
        print(ships)
        return cls(ships=ships, size=size)
    

                
    @property
    def active_ships(self):
        return {ship for ship, hits in self.state.items() if len(hits) < ship.size}
    
    def strike(self, hit):
        if hit in self.layout:
            ship = self.layout[hit]
            self.state[ship].add(hit)
            return (Sinking if len(self.state[ship]) == ship.size else Hit)(ship)        
        return Miss()
        

@lambda coro: lambda *a, **kw: [ci := coro(*a, **kw), next(ci), ci.send][-1]
def random_fire(board):
    targets = [*product(range(board.size[0]), range(board.size[1]))]
    history = set()
    shuffle(targets)
    result = yield
    while targets:
        tgt = targets.pop()
        history.add(tgt)
        result = yield tgt
        if isinstance(result, Hit) and not isinstance(result, Sinking):
            basex, basey = base = tgt
            for xadj, yadj in product([-1, 0, +1], repeat=2):
                if (xadj != 0 and yadj != 0): continue
                if not (0 <= basex + xadj < board.size[0]):continue
                if not (0 <= basey + yadj < board.size[1]):continue
                tgt = basex + xadj, basey + yadj
                if tgt not in history:
                    history.add(tgt)
                    result = yield tgt
                    if isinstance(result, Hit) and not isinstance(result, Sinking):
                        ...

def calculate_probabilities(board):
    targets = [*product(range(board.size[0]), range(board.size[1]))]
    calculate_board = [[0 for _ in range(board.size[0])] for __ in range(board.size[1])]
    for ship in board.active_ships:
        cnt_of_vars = 0
        for basex, basey in targets:

            if len(board.state[ship]) >= 2:
                ...
            elif len(board.state[ship]) == 1:
                ...
            else:
                for xadj, yadj in [(0, ship.size), (ship.size, 0)]:
                    if not (0 <= basex + xadj < board.size[0]):break
                    if not (0 <= basey + yadj < board.size[1]):break
                    for i in range(xadj):
                        for j in range(yadj):
                            if ((basex + i, basey + j) not in targets):
                                flag = True
                                flag |= checkcells()
                                ...
                    calculate_board[basex][basey] = max(1 / cnt_of_vars, calculate_board, calculate_board[basex][basey])

                    
                    

                    

                    
def checkcells(board, x, y, place):
    ...

@lambda coro: lambda *a, **kw: [ci := coro(*a, **kw), next(ci), ci.send][-1]
def smart_fire(board):
    calculate_probabilities(board)



if __name__ == '__main__':
    
    board_a = Board.from_random()
    board_b = Board.from_random()
    
    strategy_a = random_fire(board_b)
    strategy_b = random_fire(board_a)
    # strategy = fire_at_the_same_spot
    result_a, result_b = None, None
    while board_a.active_ships and board_b.active_ships:
        #print(board_a.state)
        #print(board_a.layout)
        shot = strategy_a(result_a)
        result = result_a = board_b.strike(shot)

        if isinstance(result, Miss):
            print("A: miss")
        elif isinstance(result, Hit):
            print(f'A: hit {result.ship}')
            if isinstance(result, Sinking):
                print(f'A: sunk {result.ship}')
                
        shot = strategy_b(result_b)
        result = result_b = board_a.strike(shot)

        if isinstance(result, Miss):
            print("B: miss")
        elif isinstance(result, Hit):
            print(f'B: hit {result.ship}')
            if isinstance(result, Sinking):
                print(f'B: sunk {result.ship}')
        
    if board_a.active_ships:
        print('A won!')
    elif board_b.active_ships:
        print('B won!')