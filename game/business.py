from django.http import HttpResponse, JsonResponse
import json

import random

def index(request):
    data = json.loads(request.body)
    game_state = data.get("game_state")
    move = data.get("move")
    if(correct_move(game_state,move)):
        game_state = apply_move(game_state,move)
        #zone_block()
    return JsonResponse({"game_state":game_state})

#def zone_block():
    #remplissage_zone_block()

def correct_move(game_state,move):
    position_player = game_state["players"][game_state["current_player"]]["position"]
    board = game_state["board"]
    if(move[0]>=0 and move[1]>=0 and move[0]<=7 and move[1]<=7): #pas en dehors du tableau
        if(position_player[0] == move[0] or position_player[1] == move[1]): #pas de diagonal
            if(board[move[0]][move[1]] != (game_state["current_player"]+1%2)+1): #pas sur la case d'une autre joueur
                return True
    return False

#def remplissage_zone_block():

def apply_move(game_state,move) :
    game_state["board"][move[0]][move[1]] = (game_state["current_player"] + 1)
    game_state["players"][game_state["current_player"]]["position"] = move
    game_state["current_player"] = (game_state["current_player"]+1) % 2
    return game_state
    
