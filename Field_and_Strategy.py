from dataclasses import dataclass
from enum import Enum
from collections import namedtuple
from random import seed, shuffle
from itertools import product
import sys
from sys import exit
sys.breakpointhook = exit

seed(1)

Piece = namedtuple('Piece', 'name size')

class Ship(Enum):
    Ship2 = Piece('destroyer', 2)
    Ship4 = Piece('battleship', 4)
    
    @property
    def size(self):
        return self.value.size
    
    @property
    def name(self):
        return self.value.name

@dataclass(frozen=True)
class Miss:
    pass

@dataclass(frozen=True)
class Hit:
    ship : Ship

@dataclass(frozen=True)
class Sinking(Hit):
    pass


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
        ships = {
            Ship.Ship4: {(0, 4), (1, 4), (2, 4), (3, 4)}, 
            Ship.Ship2: {(8, 7), (8, 8)}, 
        }
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
        

# def fire_at_the_same_spot(_):
#     return (0, 0)

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



if __name__ == '__main__':
    
    board_a = Board.from_random()
    board_b = Board.from_random()
    
    strategy_a = random_fire(board_b)
    strategy_b = random_fire(board_a)
    # strategy = fire_at_the_same_spot
    result_a, result_b = None, None
    while board_a.active_ships and board_b.active_ships:
        
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