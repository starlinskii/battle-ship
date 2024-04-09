from include.headers import *

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