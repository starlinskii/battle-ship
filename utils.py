from headers import *

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

#check can we place the ship to requirement cord
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

#check is the shot correct or not
def player_fire(board, history):
        print('Choose the cell, where do you want to shot: ')
        print('Print number of line: (0, 1, 2, 3, 4, 5, 6, 7, 8)')
        x = input()
        while (len(x) != 1 or not (0 <= (ord(x) - ord('0')) < 9)):
            print('Please, enter the correct line!')
            x = input()
        while not (0 <= (ord(x) - ord('0')) < 9):
            print('Please, enter the correct line!')
            x = input()
        y = input()
        while (len(y) > 1):
            print('Please, enter the correct column!')
            y = input()
        while not (0 <= (ord(y) - ord('0')) < 9):
            print('Please, enter the correct column!')
            y = input()
        x, y = int(x), int(y)
        tgt = x, y

        if not (0 <= x < board.size[0]): return -1, -1
        if not (0 <= y < board.size[1]): return -1, -1
        if tgt in history:
            return -1, -1
        history.add(tgt)
        return tgt

#check and place the ship to user's requirement cord
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
        return False
    else:
        print('Sorry, thats incorrect')
        return True
