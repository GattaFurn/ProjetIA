def index(request,game_state,move):
    if(correct_move(game_state,move)):
        apply_move()
        zone_block()

def zone_block():
    remplissage_zone_block()

def correct_move(game_state,move):
    position_player = game_state["players"][game_state["current_player"]].position
    if(move[0]>=0 and move[1]>=0 and move[0]<=7 and move[1]<=7): #pas en dehors du tableau
        if(position_player[0] == move[0] or position_player[1] == move[1]): #pas de diagonal
            if(game_state.board[move[0]][move[1]] != (game_state["current_player"]+1%2)+1): #pas sur la case d'une autre joueur
                return True
    return False

#def remplissage_zone_block():
    #remplir case zone bloquée
def send(request,game_state):
    game_state["current_player"] += 1 % 2

def apply_move(request) :
    random_board = [[random.randint(0,2) for i in range(8)]for i in range(8)]
    game_state = {
        "game_id" : 11,
        "board" : random_board,
        "players" : [{
                "id" :  10,
                "name" : "Alice",
                "color" : "cyan",
                "position" : [0,0]
            },{
                "id" :  20,
                "name" : "Bob",
                "color" : "orange",
                "position" : [7,7]
            }],
        "current_player" : 1,
        "code" : 0
    }
    return JsonResponse(game_state)
