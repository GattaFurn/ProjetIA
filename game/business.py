from django.http import HttpResponse, JsonResponse
import game.ia as ia
import json
from .models import Game
from .models import Player
import datetime 
import itertools 

def gameplay(request):
    data = json.loads(request.body)
    game = Game.objects.get(id = request.session["idGame"])
    game_state = game.__dict__
    game_state["board"] = json.loads(game_state["board"])
    game_state["position_player1"] = json.loads(game_state["position_player1"])
    game_state["position_player2"] = json.loads(game_state["position_player2"])

    current_player = game_state["current_player"]
    positionPlayer = "position_player"+str(current_player+1)
    playerBoxTurn = "player"+str(current_player+1)+"BoxTurn"
    if(game_state["code"] == 0):
        move = data.get("move")
        if(correct_move(game_state,move)):
            if(game_state.get("board")[move[0]][move[1]] == 0):
                game_state["board"][move[0]][move[1]],game_state[positionPlayer] = apply_move(game_state,move)
                game_state[playerBoxTurn] = zone_search(game_state["board"],current_player,game_state[positionPlayer])
            else:
                game_state["board"][move[0]][move[1]],game_state[positionPlayer] = apply_move(game_state,move)
                game_state[playerBoxTurn] = 0
            game_state["code"] = game_is_win(game_state)
            game_state["current_player"] = switch_player(game_state)
        if(game_state["ia_info_id"] != None and game_state["code"] == 0):
             game_state = ia.ia_playing(game_state)
        game_state["max_box_taken_with_area"] = max([game_state["player1_box_turn"],game_state["player2_box_turn"],game_state["max_box_taken_with_area"]])
        save_in_DB(game_state,game,data.get("time"))
    del game_state["_state"]
    del game_state["time"]
    return JsonResponse({"game_state":json.loads(json.dumps(game_state))})

def zone_search(board,current_player,position):
    zone = []
    elem = neighbour(zone,position[0],position[1],board,current_player)
    ind = 0
    while (ind < len(elem) and zone == []):
        zone = zone_block(zone,elem[ind][0],elem[ind][1],board,current_player)
        ind+=1
    zone.sort()
    zone = [i for n, i in enumerate(zone) if i not in zone[:n]]
    fille_zone_blocked(board,zone,current_player)
    return 1 if len(zone) == 0 else len(zone)+1

def fille_zone_blocked(board,zone,current_player):
    for elem in zone:
        board[elem[0]][elem[1]] = current_player + 1

def zone_block(zone,ligne,colonne,board,current_player):
    if(board[ligne][colonne] == ((current_player + 1)%2+1)):
        zone = []
        return zone
    if(board[ligne][colonne] == 0):
        zone.append([ligne,colonne])
        voisincase = neighbour(zone,ligne,colonne,board,current_player)
        ind = 0
        while(ind < len(voisincase) and zone != []):
            zone = zone_block(zone,voisincase[ind][0],voisincase[ind][1],board,current_player)
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
    return ((game_state["current_player"]+1) % 2) if game_state["code"] == 0 else game_state["current_player"]

def game_is_win(game_state):
    code = 0
    nbCasesPlayer1,nbCasesPlayer2 = box_counting(game_state["board"])
    if(nbCasesPlayer1 > 32):
        code = 1
    elif(nbCasesPlayer2 > 32):
        code = 2
    elif(nbCasesPlayer1 == 32 and nbCasesPlayer2 == 32):
        code = 3
    if(game_state["ia_info_id"] != None and game_state["current_player"] == 1):
        return nbCasesPlayer1,nbCasesPlayer2,code
    return code

def box_counting(board):
    nbCasesPlayer1 = 0
    nbCasesPlayer2 = 0
    for line in board:
        nbCasesPlayer1 += line.count(1)
        nbCasesPlayer2 += line.count(2)
    return nbCasesPlayer1,nbCasesPlayer2

def save_in_DB(game_state,game,time):
    game.board = game_state["board"]
    game.max_box_taken_with_area = game_state["max_box_taken_with_area"]
    game.position_player1 = game_state["position_player1"]
    game.position_player2 = game_state["position_player2"]
    game.current_player = game_state["current_player"]
    game.time = datetime.time(int(time[0]),int(time[1:3]),int(time[3:5]))
    game.code = game_state["code"]
    game.player1_box_turn = game_state["player1_box_turn"]
    game.player2_box_turn = game_state["player2_box_turn"]
    game.player1_box_total = game_state["player1_box_total"]+game_state["player1_box_turn"]
    game.player2_box_total = game_state["player2_box_total"]+game_state["player2_box_turn"]
    game.save()