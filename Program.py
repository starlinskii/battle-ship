from headers import *
from utils import *
from Field import Board
from Strategy import strategies_prefomancer
from Ship_States import *
from Player import player_interface

#the main core of the game
def play():
    global static_field
    for i in range(len(static_field)):
        for j in range(len(static_field[i])):
            print(str(static_field[i][j]), end='')
        print()
    
    board_player = Board.set_ship()
    board_computer = Board.from_random()

    print('Do you want to play versus advance comupter?')
    print('print 1 if yes')
    print('print 0 if no')

    var = input()
    while (var != '0' and var != '1'):
        print('Please, enter correct orientation')
        var = input()
    strategy = [strategies_prefomancer.random_fire, strategies_prefomancer.smart_fire]
    strategy_a = strategy[int(var)](board_player)
    result_a, result_b = None, None
    history = set()

    while board_computer.active_ships and board_player.active_ships:
        shot = strategy_a(result_a)
        result = result_a = board_player.strike(shot)

        if isinstance(result, Miss):
            print("A: miss")
        elif isinstance(result, Hit):
            print(f'A: hit {result.ship.name}')
            if isinstance(result, Sinking):
                print(f'A: sunk {result.ship.name}')
        
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
