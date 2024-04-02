from headers import *

inf = 1e9

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

def checkcells(board, x, y):
    ans = False
    for dx, dy in product([-1, 0, 1], repeat=2):
        if not (0 <= x + dx < board.size[0]): continue
        if not (0 <= y + dy < board.size[1]): continue
        if ((x + dx, y + dy) in board.layout and (x + dx, y + dy) in board.state[board.layout[(x + dx, y + dy)]]):
            ans = True
    return ans

def calculate_probabilities(board, targets):
    calculate_board = [[0 for _ in range(board.size[1])] for __ in range(board.size[0])]
    for ship in board.active_ships:
        tgt = []
        #############################################################################
        if len(board.state[ship]) >= 2:
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
        #############################################################################        
        elif len(board.state[ship]) == 1:
            x, y = board.state[ship].pop()
            board.state[ship].add((x, y))
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
        #############################################################################
        else:
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
        total = len(tgt)
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