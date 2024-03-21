from dataclasses import dataclass
from enum import Enum
from collections import namedtuple
from random import seed, shuffle
from itertools import product
import random
import copy

seed(random)

inf = 1e9

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

def watch(orientation, x, y, ship, ships):
    global static_field
    cpy = copy.deepcopy(static_field)
    ans = False
    kx, ky = orientation, 1 - orientation

    if (y + ship.size - 1 >= len(static_field) or x + ship.size - 1 >= len(static_field)):
        ans = True

    for i in range(ship.size):
        for dx, dy in product([-1, 0, 1], repeat=2):
            if not (0 <= x + i*kx + dx < len(static_field)): continue
            if not (0 <= y + i*ky + dy < len(static_field)): continue
            if (cpy[x + i*kx + dx][y + i*ky + dy] == 'o'):
                ans = True
                print('gg')

    for i in range(min(ship.size, len(static_field) - x, len(static_field) - y)):
        cpy[x + i*kx][y + i*ky] = 'o'
    print('Do you want to place it like this?')
    for i in cpy:
        print(*i)
    print('Print 1 if yes')
    print('Print 0 if no')
    sure = int(input())
    if sure == 0:
        print('okay, lets try again')
        return True
    if not ans:
        static_field = copy.deepcopy(cpy)
        ships[ship] = {(x + i*kx, y + i*ky) for i in range(ship.size)}
        print('Success')
    else:
        print('Sorry, thats incorrect')
    return ans

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
            if (field[x + dx + i*kx][y + dy + i*ky] != 0): return False
    for i in range(ship.size):
        field[x + i*kx][y + i*ky] = 1
    ships[ship] = {(x + i*kx, y + i*ky) for i in range(ship.size)}
    return True

static_field = [
         ['#', '#', '#', '#', '#', '#', '#', '#', '#'], 
         ['#', '#', '#', '#', '#', '#', '#', '#', '#'], 
         ['#', '#', '#', '#', '#', '#', '#', '#', '#'], 
         ['#', '#', '#', '#', '#', '#', '#', '#', '#'], 
         ['#', '#', '#', '#', '#', '#', '#', '#', '#'], 
         ['#', '#', '#', '#', '#', '#', '#', '#', '#'], 
         ['#', '#', '#', '#', '#', '#', '#', '#', '#'], 
         ['#', '#', '#', '#', '#', '#', '#', '#', '#'], 
         ['#', '#', '#', '#', '#', '#', '#', '#', '#'],]


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
    def set_ship(cls, *, size=(9, 9), pieces=frozenset({*Ship})):
        ships = {}
        for ship in ships_list:
            flag = True
            orientation = 0
            x, y = -1, -1
            while flag:
                print(f'Please, choose, where do you want to set your {ship.name}')
                print('Firstly, choose an orientation: ')
                print('print 0 if horizontal')
                print('print 1 if vertical')
                orientation = int(input())
                if (orientation != 0 and orientation != 1):
                    print('sorry that is incorrect, please try again')
                    continue
                print('Great! Now, Lets choose the place: ')
                print('Print number of line: (0, 1, 2, 3, 4, 5, 6, 7, 8)')
                x = int(input())
                if not (0 <= x < 9):
                    print('sorry that is incorrect, please try again')
                    continue
                print('Print number of column: (0, 1, 2, 3, 4, 5, 6, 7, 8)')
                y = int(input())
                if not (0 <= y < 9):
                    print('sorry that is incorrect, please try again')
                    continue
                flag = watch(orientation, x, y, ship, ships)
        return cls(ships=ships, size=size)



    @classmethod
    def from_random(cls, *, size=(9, 9), pieces=frozenset({*Ship})):
        targets = [*product(range(size[0]), range(size[1]))]
        field = [[0 for i in range(size[0])] for j in range(size[1])]
        shuffle(targets)
        tgt = ships_list.copy()
        ships = {}
        for ship in tgt:
            for cord in targets:
                if check_and_place(cord, ship, field, ships):
                    break
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
                    
def define_oriental(tgt):
    #False-horizontal
    #True-vertical
    targ = copy.deepcopy(tgt)
    dx, dy = targ.pop()
    dy, y = targ.pop()
    dx -= dy
    return dx != 0
def getrange(tgt):
    global inf
    minx = inf
    miny = inf
    maxx = 0
    maxy = 0
    for cord in tgt:
        x, y = cord
        minx = min(x, minx)
        miny = min(y, miny)
        maxx = max(x, maxx)
        maxy = max(y, maxy)
    return ((minx, miny), (maxx, maxy))


def calculate_probabilities(board, targets):
    calculate_board = [[0 for _ in range(board.size[1])] for __ in range(board.size[0])]
    for ship in board.active_ships:
        #############################################################################
        if len(board.state[ship]) >= 2:
            tgt = []
            oriental = define_oriental(board.state[ship])
            result = getrange(board.state[ship])
            
            if (not oriental):
                for startx in range(result[1][0] - ship.size + 1, result[0][0] + 1):
                    if ((startx, result[0][1]) not in targets): break
                    if not (0 <= startx < board.size[0]): break
                    if not (0 <= startx + ship.size <= board.size[0]): break
                    flag = False
                    for i in range(ship.size):
                        flag |= checkcells(board, startx + i, result[0][1])
                        if (startx + i, result[0][1] not in targets):
                            flag = True
                    if (flag): continue
                    for i in range(ship.size):
                        tgt.append((startx + i, result[0][1]))
            else:
                for starty in range(result[1][1] - ship.size + 1, result[0][1] + 1):
                    if ((starty, result[0][0]) not in targets): break
                    if not (0 <= starty < board.size[1]): break
                    if not (0 <= starty + ship.size <= board.size[1]): break
                    flag = False
                    for i in range(ship.size):
                        flag |= checkcells(board, result[0][0], starty + i)
                        if ((result[0][0], starty + i) not in targets):
                            flag = True
                    if (flag): continue
                    for i in range(ship.size):
                        tgt.append((result[0][0], starty + i))
            total = len(tgt)
            if total == 0: continue #???#
            for pos in tgt:
               for x, y in pos:
                   calculate_board[x][y] += 1/total
        #############################################################################        
        elif len(board.state[ship]) == 1:
            x, y = board.state[ship].pop()
            board.state[ship].add((x, y))
            tgt = []
            for startx in range(x - ship.size + 1, x + 1):
                if not (0 <= startx < board.size[0]): break
                if not (0 <= startx + ship.size <= board.size[0]): break
                flag = False
                for i in range(ship.size):
                    flag |= checkcells(board, startx + i, y)
                    if ((startx + i, y) not in  targets):
                        flag = True
                if (flag): continue
                for i in range(ship.size):
                    tgt.append((startx + i, y))

            for starty in range(y - ship.size + 1, y + 1):
                if not (0 <= starty < board.size[1]): break
                if not (0 <= starty + ship.size <= board.size[1]): break
                flag = False
                for i in range(ship.size):
                    flag |= checkcells(board, x, starty + i)
                    if ((x, starty + i) not in  targets):
                        flag = True
                if (flag): continue
                for i in range(ship.size):
                    tgt.append((x, starty + i))
            
            total = len(tgt)
            if total == 0: continue #???#
            for pos in tgt:
               for x, y in pos:
                   calculate_board[x][y] += 1/total
        #############################################################################
        else:
            tgt = []
            for basex, basey in targets:
                for xadj, yadj in [(1, ship.size), (ship.size, 1)]:
                    if not (0 <= basex + xadj <= board.size[0]): break
                    if not (0 <= basey + yadj <= board.size[1]): break
                    flag = False
                    for i in range(xadj):
                        for j in range(yadj):
                            flag |= checkcells(board, basex + i, basey + j)
                            if ((basex + i, basey + j) not in targets):
                                flag = True
                    if (flag): continue
                    for i in range(xadj):
                        for j in range(yadj):
                            tgt.append((basex + i, basey + j))
                            #calculate_board[basex + i][basey + j] += 1
                            # if (ship.size == 1):
                            #     calculate_board[basex + i][basey + j] -= 0.5
                if (ship.size == 1 and len(tgt) != 0):
                    tgt.pop()
            total = len(tgt)
            if total == 0: continue #???#
            for pos in tgt:
                x, y = pos
                calculate_board[x][y] += 1/total
        #############################################################################
    ans = -1, -1
    probability = -1
    for i in range(board.size[0]):
        for j in range(board.size[1]):
            if (calculate_board[i][j] > probability and (i, j) in targets):
                probability = calculate_board[i][j]
                ans = i, j
    if (ans != (-1, -1)):
        targets.remove(ans)
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
        result = yield tgt

if __name__ == '__main__':
    for i in range(len(static_field)):
        for j in range(len(static_field[i])):
            print(str(static_field[i][j]), end='')
        print()
    board_player = Board.from_random()
    #board_player = Board.set_ship()
    board_computer = Board.from_random()

    # print('Do you want to play versus advance comupter?')
    # print('print 1 if yes')
    # print('print 0 if no')
    # strategy = int(input())

    # strategy = {random_fire(board_player), smart_fire(board_player)}
    strategy_a = smart_fire(board_player)
    strategy_b = random_fire(board_computer)
    result_a, result_b = None, None
    while board_computer.active_ships and board_player.active_ships:
        shot = strategy_a(result_a)
        result = result_a = board_player.strike(shot)

        if isinstance(result, Miss):
            print("A: miss")
        elif isinstance(result, Hit):
            print(f'A: hit {result.ship}')
            if isinstance(result, Sinking):
                print(f'A: sunk {result.ship}')
        
        shot = strategy_b(result_b)
        result = result_b = board_computer.strike(shot)

        if isinstance(result, Miss):
            print("B: miss")
        elif isinstance(result, Hit):
            print(f'B: hit {result.ship}')
            if isinstance(result, Sinking):
                print(f'B: sunk {result.ship}')
        
    if board_computer.active_ships:
        print('A won!')
    elif board_player.active_ships:
        print('B won!')