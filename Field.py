from utils import check_and_place
from headers import *
from Ships import Ship, ships_list
from Player import player_interface
from Ship_States import *

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

    #check the correction of person's requirement
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
                orientation = input()
                if (len(orientation) != 1 or (orientation != '0' and orientation != '1')):
                    print('sorry that is incorrect, please try again')
                    flag = True
                    continue
                orientation = int(orientation)
                print('Great! Now, Lets choose the place: ')
                print('Print number of line: (0, 1, 2, 3, 4, 5, 6, 7, 8)')
                x = input()
                if (len(x) != 1 or not (0 <= (ord(x) - ord('0')) < 9)):
                    print('sorry that is incorrect, please try again')
                    flag = True
                    continue
                x = int(x)
                print('Print number of column: (0, 1, 2, 3, 4, 5, 6, 7, 8)')
                y = input()
                if (len(y) != 1 or not (0 <= (ord(y) - ord('0')) < 9)):
                    print('sorry that is incorrect, please try again')
                    flag = True
                    continue
                y = int(y)
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

