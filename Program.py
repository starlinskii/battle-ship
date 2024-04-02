from headers import *
from Field_and_Strategy import *

if __name__ == '__main__':
    for i in range(len(static_field)):
        for j in range(len(static_field[i])):
            print(str(static_field[i][j]), end='')
        print()
    
    board_player = Board.set_ship()
    board_computer = Board.from_random()

    print('Do you want to play versus advance comupter?')
    print('print 1 if yes')
    print('print 0 if no')

    var = int(input())
    strategy = [strategies_prefomancer.random_fire, strategies_prefomancer.smart_fire]
    strategy_a = strategy[var](board_player)
    result_a, result_b = None, None
    
    while board_computer.active_ships and board_player.active_ships:
        shot = strategy_a(result_a)
        result = result_a = board_player.strike(shot)

        if isinstance(result, Miss):
            print("A: miss")
        elif isinstance(result, Hit):
            print(f'A: hit {result.ship.name}')
            if isinstance(result, Sinking):
                print(f'A: sunk {result.ship.name}')
        
        history = set()
        shot = player_interface.fire(board_computer, history)
        result = result_b = board_computer.strike(shot)

        if isinstance(result, Miss):
            print("B: miss")
        elif isinstance(result, Hit):
            print(f'B: hit {result.ship.name}')
            if isinstance(result, Sinking):
                print(f'B: sunk {result.ship.name}')
        
    if board_computer.active_ships:
        print('Computer won!')
    elif board_player.active_ships:
        print('You won!')
    else:
        print('Draw!')
