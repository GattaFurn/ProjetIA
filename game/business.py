from django.http import HttpResponse, JsonResponse
import game.ia
import json

def index(request):
    data = json.loads(request.body)
    game_state = data.get("game_state")
    move = data.get("move")
    if(correct_move(game_state,move)):
        if(game_state.get("board")[move[0]][move[1]] == 0):
            apply_move(game_state,move)
            position = game_state["players"][game_state["current_player"]]["position"]
            game_state["players"][game_state["current_player"]]["box_taken"] = zone_search(game_state["board"],game_state["current_player"],position)
        else:
            apply_move(game_state,move)
            game_state["players"][game_state["current_player"]]["box_taken"] = 0
        switch_player(game_state)
    if(game_state["players"][game_state["current_player"]]["type"] == "IA"):
        return game.ia.index(game_state)
    return JsonResponse({"game_state":game_state})
    
def zone_search(board,current_player,position):
    zone = []
    elem = voisin(zone,position[0],position[1],board,current_player)
    ind = 0
    while (ind < len(elem) and zone == []):
        zone = zone_blocker(zone,elem[ind][0],elem[ind][1],board,current_player)
        ind+=1
    remplissage_zone_block(board,zone,current_player)
    return len(zone) + 1

def remplissage_zone_block(board,zone,current_player):
    for elem in zone:
        board[elem[0]][elem[1]] = current_player+1

def zone_blocker(zone,ligne,colonne,board,current_player):
    if(board[ligne][colonne] == ((current_player + 1)%2+1)):
        zone = []
        return zone
    if(board[ligne][colonne] == 0):
        zone.append([ligne,colonne])
        voisin_case = voisin(zone,ligne,colonne,board,current_player)
        ind = 0
        while(ind < len(voisin_case) and zone != []):
            zone = zone_blocker(zone,voisin_case[ind][0],voisin_case[ind][1],board,current_player)
            ind+=1 
    return zone

def voisin(zone,ligne,colonne,board,current_player):
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
    position_player = game_state["players"][game_state["current_player"]]["position"]
    board = game_state["board"]
    if(move[0]>=0 and move[1]>=0 and move[0]<=7 and move[1]<=7): #pas en dehors du tableau
        if(board[move[0]][move[1]] != (((game_state["current_player"]+1)%2)+1)): #pas sur la case d'une autre joueur
            return True
    return False

def apply_move(game_state,move) :
    game_state["board"][move[0]][move[1]] = (game_state["current_player"] + 1)
    game_state["players"][game_state["current_player"]]["position"] = move
    
def switch_player(game_state):
    game_state["current_player"] = (game_state["current_player"]+1) % 2

def game_is_win(game_state):
    nb_cases_player1 = 0
    nb_cases_player2 = 0
    for line in game_state["board"]:
        nb_cases_player1 += line.count(1)
        nb_cases_player2 += line.count(2)
    if(nb_cases_player1 > 32):
        game_state["code"] = 1
    elif(nb_cases_player2 > 32):
        game_state["code"] = 2
    elif(nb_cases_player1 == 32 and nb_cases_player2 == 32):
        game_state["code"] = 3
    if(game_state["players"][1]["type"] == "IA"):
        return nb_cases_player1,nb_cases_player2


    