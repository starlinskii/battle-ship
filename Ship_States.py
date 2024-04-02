from headers import *
from Ships import Ship

@dataclass(frozen=True)
class Miss:
    pass

@dataclass(frozen=True)
class Hit:
    ship : Ship

@dataclass(frozen=True)
class Sinking(Hit):
    pass
