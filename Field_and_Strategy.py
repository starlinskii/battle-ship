from dataclasses import dataclass
from enum import Enum
from collections import namedtuple
from random import seed, shuffle
from itertools import product
import random

seed(random)

Piece = namedtuple('Piece', ['name', 'size', 'order'])

class Ship(Enum):
    Boat1 = Piece('boat', 1, 1)
    Boat2 = Piece('boat', 1, 2)
    Boat3 = Piece('boat', 1, 3)
    Boat4 = Piece('boat', 1, 4)
    destroyer1 = Piece('destroyer', 2, 1)
    destroyer2 = Piece('destroyer', 2, 2)
    destroyer3 = Piece('destroyer', 2, 3)
    battleship = Piece('battleship', 4, 1)
    carrier = Piece('carrier', 5, 1)

    @property
    def size(self):
        return self.value.size
    
    @property
    def name(self):
        return self.value.name
    
ships_list = [Ship.destroyer1, Ship.destroyer2, Ship.destroyer3, Ship.Boat1, Ship.Boat2, Ship.Boat3, Ship.Boat4, Ship.battleship, Ship.carrier]

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
    kx = random.randint(0, 1)
    ky = 1 - kx
    if (x + ship.size >= len(field) and y + ship.size >= len(field)): return 0
    
    if (x + ship.size >= len(field)):
        kx, ky = 0, 1
    if (y + ship.size >= len(field)):
        kx, ky = 1, 0

    for i in range(ship.size):
        for dx, dy in product((-1, 0, 1), repeat=2):
            if not (0 <= x + dx + i*kx < len(field) and 0 <= y + dy + i*ky < len(field[0])): continue
            if (field[x + dx + i*kx][y + dy + i*ky] != 0): return 0
    for i in range(ship.size):
        field[x + i*kx][y + i*ky] = 1
    ships[ship] = {(x + i*kx, y + i*ky) for i in range(ship.size)}
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
        tgt = ships_list.copy()
        ships = {}
        for ship in tgt:
            for cord in targets:
                if check_and_place(cord, ship, field, ships) != 0:
                    break
        #print(ships, end='\n\n\n')
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
                    

def calculate_probabilities(board, targets):
    calculate_board = [[0 for _ in range(board.size[1])] for __ in range(board.size[0])]
    for ship in board.active_ships:
        cnt_of_vars = 0
        for basex, basey in targets:

            # if len(board.state[ship]) >= 2:
            #     ...
            # elif len(board.state[ship]) == 1:
            #     ...
            # else:
                for xadj, yadj in [(1, ship.size), (ship.size, 1)]:
                    if not (0 <= basex + xadj < board.size[0]):break
                    if not (0 <= basey + yadj < board.size[1]):break
                    flag = False
                    for i in range(xadj + 1):
                        for j in range(yadj + 1):
                            flag |= checkcells(board, basex + i, basey + j)
                            if ((basex + i, basey + j) not in targets):
                                flag = True
                    if (flag): continue
                    for i in range(xadj):
                        for j in range(yadj):
                            calculate_board[basex + i][basey + j] += 1
                            if (ship.size == 1):
                                calculate_board[basex + i][basey + j] -= 0.5
    ans = -1, -1
    probability = -1
    for i in range(board.size[0]):
        for j in range(board.size[1]):
            if (calculate_board[i][j] > probability and (i, j) in targets):
                probability = calculate_board[i][j]
                ans = i, j
    if (ans != (-1, -1)):
        print(ans)
        print(targets)
        targets.remove(ans)
        print(targets)
    return ans
                    
def checkcells(board, x, y):
    ans = False
    for dx, dy in product([-1, 0, 1], repeat=2):
        if not (0 <= x + dx < board.size[0]): continue
        if not (0 <= y + dy < board.size[1]): continue
        if ((x + dx, y + dy) in board.layout and (x + dx, y + dy) in board.state[board.layout[(x + dx, y + dy)]]):
            ans = True
    return ans


@lambda coro: lambda *a, **kw: [ci := coro(*a, **kw), next(ci), ci.send][-1]
def smart_fire(board):
    targets = set()
    for x, y in [*product(range(board.size[0]), range(board.size[1]))]:
        targets.add((x, y))
    result = yield
    while len(targets) > 0:
        tgt = calculate_probabilities(board, targets)
        print(tgt)

        result = yield tgt



if __name__ == '__main__':
    board_a = Board.from_random()
    board_b = Board.from_random()
    
    strategy_a = smart_fire(board_b)
    strategy_b = random_fire(board_a)
    print(strategy_a)
    print()
    print(strategy_b)
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