from Advance_Strategy import calculate_probabilities
from Ship_States import *
from headers import *

class strategies_prefomancer:
    #random strategy
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
    #advance strategy
    @lambda coro: lambda *a, **kw: [ci := coro(*a, **kw), next(ci), ci.send][-1]
    def smart_fire(board):
        targets = set()
        for x, y in [*product(range(board.size[0]), range(board.size[1]))]:
            targets.add((x, y))
        result = yield
        while len(targets) > 0:
            tgt = calculate_probabilities(board, targets)
            result = yield tgt