from game.business import apply_move,switch_player,correct_move,zone_search,game_is_win
from game.ia import index,actions
import random
import json
import time
from django.shortcuts import redirect

NB_ITERATION = 20

def training(request):
    eps = 0
    step = 1 / (NB_ITERATION / 2)
    game_state = reset(eps)
    for i in range(NB_ITERATION):
        while(game_state["code"]==0):
            if(game_state["current_player"] == 0):
                move = random_play(game_state)
                game_state["board"][move[0]][move[1]],game_state["players"][game_state["current_player"]]["position"] = apply_move(game_state,move)
                game_state["code"] = game_is_win(game_state)
                game_state["players"][0]["box_taken"],game_state["board"] = zone_search(game_state["board"],0,game_state["players"][0]["position"])
                game_state["current_player"] = switch_player(game_state)
            else:
                game_state = index(game_state)
            #affichage_plateau(game_state)
        print("fini")
        if(eps != 1):
            eps += step
        game_state = reset(eps)
    print("Totalement fini")
    return redirect('../connection')
        

def reset(eps):
    player2 = {"position":[7,7],"st":[7,7],"atp1":0,"at":0,"box_taken":0,"eps":eps,"stp1":0,"type":"IA"}
    player1 = {"position":[0,0],"box_taken":0,"type":"random"}
    game_state = {
    "game_id" : 11,
    "board" : [[1,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,2]],
    "players" : [player1,player2],
    "current_player" : 0,
    "code": 0
    }
    return game_state

def random_play(game_state):
    action = random.randint(0,3)
    move = game_state["players"][0]["position"].copy()
    move[0] += actions[action][0]
    move[1] += actions[action][1]
    while (not correct_move(game_state,move)):
        action = random.randint(0,3)
        move = game_state["players"][0]["position"].copy()
        move[0] += actions[action][0]
        move[1] += actions[action][1]
    return move

def affichage_plateau(game_state):
    """
        Show the grid
    """
    print("---------------------")
    ligne = 0
    for line in game_state["board"]:
        colonne = 0
        print("[",end="")
        for n in line:
            if((game_state["players"][0]["position"] == [ligne,colonne])):
                print("X ,",end="")
            if((game_state["players"][1]["position"] == [ligne,colonne])):
                print("O ,",end="")
            if(game_state["players"][1]["position"] != [ligne,colonne]) and (game_state["players"][0]["position"] != [ligne,colonne]):
                print(n,",",end="")
            colonne += 1
        print("]")
        ligne +=1