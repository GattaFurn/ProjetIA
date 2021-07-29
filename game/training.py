from game.business import *
from game.ia import *
import random
import json
import time
from django.shortcuts import redirect

NB_ITERATION = 200000

def training(request):
    eps = max(1 * 0.996, 0.05)
    #step = 0.01
    #reach = NB_ITERATION/100
    game_state = reset(eps)
    for i in range(NB_ITERATION):
        while(game_state["code"] == 0):
                move = random_play(game_state)
                game_state["board"][move[0]][move[1]],game_state["position_player1"] = apply_move(game_state,move)
                game_state["code"] = game_is_win(game_state)
                game_state["player1_box_turn"] = zone_search(game_state["board"],0,game_state["position_player1"])
                game_state["current_player"] = switch_player(game_state)
                if(game_state["code"] == 0):
                    game_state = iaPlaying(game_state)
            #display_board(game_state)
        print(i+1)
        # if(i % reach == 0):
        #   eps += step
        if(eps != 1):
            eps =  max(eps * 0.996, 0.05)
        game_state = reset(eps)
    print("Totalement fini")
    return redirect('../connection')
        

def reset(eps):
    game_state = {
    "board" : [[1,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,2]],
    "position_player1":[0,0],
    "position_player2":[7,7],
    "player1_box_turn":0,
    "player2_box_turn":0,
    "current_player" : 0,
    "code": 0,
    "ia_info":'{"st":[7,7],"atp1":0,"at":0,"eps":'+str(eps)+',"stp1":0}'
    }
    return game_state

def random_play(game_state):
    action = random.randint(0,3)
    move = game_state["position_player1"].copy()
    move[0] += actions[action][0]
    move[1] += actions[action][1]
    while (not correct_move(game_state,move)):
        action = random.randint(0,3)
        move = game_state["position_player1"].copy()
        move[0] += actions[action][0]
        move[1] += actions[action][1]
    return move

def display_board(game_state):
    """
        Show the grid
    """
    print("---------------------")
    ligne = 0
    for line in game_state["board"]:
        colonne = 0
        print("[",end="")
        for n in line:
            if((game_state["position_player1"] == [ligne,colonne])):
                print("X ,",end="")
            if((game_state["position_player2"] == [ligne,colonne])):
                print("O ,",end="")
            if(game_state["position_player2"] != [ligne,colonne]) and (game_state["position_player1"] != [ligne,colonne]):
                print(n,",",end="")
            colonne += 1
        print("]")
        ligne +=1