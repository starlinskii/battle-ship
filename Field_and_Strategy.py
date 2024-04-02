import Advance_Strategy
from headers import *

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
    if (x + ship.size >= len(field) and y + ship.size >= len(field)): return False
    
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
                flag = player_interface.watch(orientation, x, y, ship, ships)
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
        

class strategies_prefomancer:
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

    @lambda coro: lambda *a, **kw: [ci := coro(*a, **kw), next(ci), ci.send][-1]
    def smart_fire(board):
        targets = set()
        for x, y in [*product(range(board.size[0]), range(board.size[1]))]:
            targets.add((x, y))
        result = yield
        while len(targets) > 0:
            tgt = Advance_Strategy.calculate_probabilities(board, targets)
            result = yield tgt

class player_interface:
    
    def fire(board, history):
        player_fire(board, history)
    
    def watch(orientation, x, y, ship, ships):
        watch_field(orientation, x, y, ship, ships)

def player_fire(board, history):
        print('Choose the cell, where do you want to shot: ')
        print('Print number of line: (0, 1, 2, 3, 4, 5, 6, 7, 8)')
        x = int(input())
        print('Print number of column: (0, 1, 2, 3, 4, 5, 6, 7, 8)')
        y = int(input())
        tgt = x, y

        if not (0 <= x < board.size[0]): return -1, -1
        if not (0 <= y < board.size[1]): return -1, -1
        if tgt in history:
            return -1, -1
        history.add(tgt)
        return tgt

def watch_field(orientation, x, y, ship, ships):
    global static_field
    cpy = copy.deepcopy(static_field)
    ans = False
    kx, ky = orientation, 1 - orientation

    if (y + (ship.size - 1)*ky >= len(static_field) or x + (ship.size - 1)*kx >= len(static_field)):
        ans = True

    for i in range(ship.size):
        for dx, dy in product([-1, 0, 1], repeat=2):
            if not (0 <= x + i*kx + dx < len(static_field)): continue
            if not (0 <= y + i*ky + dy < len(static_field)): continue
            if (cpy[x + i*kx + dx][y + i*ky + dy] == 'o'):
                ans = True
                print('gg')

    for i in range(ship.size):
        if not (0 <= x + i*kx < len(static_field)): continue
        if not (0 <= y + i*ky < len(static_field)): continue
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
