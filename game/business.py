from django.http import HttpResponse, JsonResponse
import game.ia as ia
import json
from .models import Game
from .models import Player
import datetime 

def index(request):
    data = json.loads(request.body)
    game_state = data.get("game_state")
    if(game_state["code"] == 0):
        move = data.get("move")
        if(correct_move(game_state,move)):
            if(game_state.get("board")[move[0]][move[1]] == 0):
                game_state["board"][move[0]][move[1]],game_state["players"][game_state["current_player"]]["position"] = apply_move(game_state,move)
                game_state["players"][game_state["current_player"]]["box_taken"],game_state["board"] = zone_search(game_state["board"],game_state["current_player"],game_state["players"][game_state["current_player"]]["position"])
            else:
                game_state["board"][move[0]][move[1]],game_state["players"][game_state["current_player"]]["position"] = apply_move(game_state,move)
                game_state["players"][game_state["current_player"]]["box_taken"] = 0
            game_state["code"] = game_is_win(game_state)
            game_state["current_player"] = switch_player(game_state)
        if(game_state["players"][game_state["current_player"]]["type"] == "IA"):
             game_state = ia.index(game_state)
        if(game_state["code"] != 0):
            save_in_db(game_state)
    return JsonResponse({"game_state":game_state})
    
def zone_search(board,current_player,position):
    zone = []
    elem = neighbour(zone,position[0],position[1],board,current_player)
    ind = 0
    while (ind < len(elem) and zone == []):
        zone = zone_blocker(zone,elem[ind][0],elem[ind][1],board,current_player)
        ind+=1
    board = fill_zone_blocked(board,zone,current_player)
    return len(zone)+1, board

def fill_zone_blocked(board,zone,current_player):
    for elem in zone:
        board[elem[0]][elem[1]] = current_player + 1
    return board

def zone_blocker(zone,ligne,colonne,board,current_player):
    if(board[ligne][colonne] == ((current_player + 1)%2+1)):
        zone = []
        return zone
    if(board[ligne][colonne] == 0):
        zone.append([ligne,colonne])
        voisin_case = neighbour(zone,ligne,colonne,board,current_player)
        ind = 0
        while(ind < len(voisin_case) and zone != []):
            zone = zone_blocker(zone,voisin_case[ind][0],voisin_case[ind][1],board,current_player)
            ind+=1 
    return zone

def neighbour(zone,ligne,colonne,board,current_player):
    voisin = []
    if(ligne-1 >= 0 and [ligne-1, colonne] not in zone and board[ligne-1][colonne] != current_player+1): #Haut
        voisin.append([ligne-1,colonne])
    if(colonne+1 <= 7 and [ligne, colonne+1] not in zone and board[ligne][colonne+1] != current_player+1): #droite
        voisin.append([ligne,colonne+1])
    if(ligne+1 <= 7 and [ligne+1, colonne] not in zone and board[ligne+1][colonne] != current_player+1):#bas
        voisin.append([ligne+1,colonne])
    if(colonne-1 >=0 and [ligne, colonne-1] not in zone and board[ligne][colonne-1] != current_player+1):#gauche
        voisin.append([ligne,colonne-1])
    return voisin

def correct_move(game_state,move):
    return ((move[0]>=0 and move[1]>=0 and move[0]<=7 and move[1]<=7) and (game_state["board"][move[0]][move[1]] != (((game_state["current_player"]+1)%2)+1)))

def apply_move(game_state,move) :
    return (game_state["current_player"] + 1), move
    
def switch_player(game_state):
    return (game_state["current_player"]+1) % 2 if game_state["code"] == 0 else game_state["current_player"]

def game_is_win(game_state):
    code = 0
    nb_cases_player1,nb_cases_player2 = box_counting(game_state["board"])
    if(nb_cases_player1 > 32):
        code = 1
    elif(nb_cases_player2 > 32):
        code = 2
    elif(nb_cases_player1 == 32 and nb_cases_player2 == 32):
        code = 3
    if(game_state["players"][game_state["current_player"]]["type"] == "IA"):
        return nb_cases_player1,nb_cases_player2,code
    return  code

def box_counting(board):
    nb_cases_player1 = 0
    nb_cases_player2 = 0
    for line in board:
        nb_cases_player1 += line.count(1)
        nb_cases_player2 += line.count(2)
    return nb_cases_player1,nb_cases_player2

def save_in_db(game_state):
    player_1 =  Player.objects.get(id = game_state["players"][0]["id"])
    player_2 =  Player.objects.get(id = game_state["players"][1]["id"])
    nb_cases_player1,nb_cases_player2 = box_counting(game_state["board"])
    play_time = datetime.time(int(game_state["time"][0]),int(game_state["time"][1:3]),int(game_state["time"][3:5]))
    Game.objects.create(board = game_state["board"], positionPlayer1 = game_state.get("players")[0]["position"],currentPlayer = game_state["current_player"],positionPlayer2 = game_state.get("players")[1]["position"] ,player1 = player_1, player2 = player_2,time = play_time,player1Box = nb_cases_player1, player2Box = nb_cases_player2)