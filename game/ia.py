import random
import numpy as np
from game.models import Qtable
from django.core.exceptions import ObjectDoesNotExist
import game.business
from django.http import HttpResponse, JsonResponse

actions = [
        [-1, 0], # Up
        [1, 0], #Down
        [0, -1], # Left
        [0, 1] # Right
    ]

def index(game_state):
    new_game_state = game_state.copy()
    direction = [0,1,2,3]
    IA = new_game_state.get("players")[1]
    row_q_table = get_qTable(new_game_state)
    IA["at"] = take_action(row_q_table, 0.4,direction)
    IA["stp1"] = step(IA["at"],IA["st"])
    while(IA["stp1"] == IA["st"] or not game.business.correct_move(new_game_state,IA["stp1"])):
            row_q_table[IA["at"]] = 0
            IA["at"] = take_action(row_q_table, 0.4,direction)
            IA["stp1"] = step(IA["at"],IA["st"])
    if(new_game_state.get("board")[IA["stp1"][0]][IA["stp1"][1]] == 0):
        game.business.apply_move(new_game_state,IA["stp1"])
        IA["box_taken"] = game.business.zone_search(new_game_state["board"],new_game_state["current_player"],IA["stp1"])
    else:
        IA["box_taken"] = 0
    IA["position"] = IA["stp1"]
    fake_row_q_table = get_qTable(new_game_state)
    IA["atp1"] = take_action(fake_row_q_table, 0.0,[0,1,2,3])
    update_q_function(game_state,new_game_state,row_q_table,fake_row_q_table)
    game.business.switch_player(new_game_state)
    return JsonResponse({"game_state":new_game_state})

def get_qTable(game_state):
    try:
        qTable = Qtable.objects.get(board = game_state["board"], posP1 = game_state.get("players")[0]["position"],posP2 = game_state.get("players")[1]["position"],playerTurn = game_state["current_player"])
    except ObjectDoesNotExist:
        qTable = Qtable.objects.create(board = game_state["board"], posP1 = game_state.get("players")[0]["position"],posP2 = game_state.get("players")[1]["position"],playerTurn = game_state["current_player"])
    return [qTable.up,qTable.down,qTable.left,qTable.right]


def step(action, st): #OK
    """
        Action: 0, 1, 2, 3
    """
    colone = max(0, min(st[1] + actions[action][1],7)) #On prend une action en évitant que la personne ne dépasse le tableau
    ligne = max(0, min(st[0] + actions[action][0],7)) #On prend une action en évitant que la personne ne dépasse le tableau

    return  [ligne,colone]

def take_action(Q_table, eps, direction): #Permet de savoir s'il doit explorer ou exploiter 
    # Take an action
    if random.uniform(0, 1) < eps:
        random.shuffle(direction)
        action = direction.pop()
    else: # Or greedy action
        if(Q_table.count(0) == 4):
            random.shuffle(direction)
            action = direction.pop()
        else:
            action = np.argmax(Q_table)
    return action

def reward(game_state):
    r = 0
    r += game_state["players"][1]["box_taken"] - game_state["players"][0]["box_taken"] #Pour avoir le nombre de case prise pour le tour
    case1,case2 = game.business.game_is_win(game_state)
    if(game_state["code"] != 0 and game_state["code"] != 3):
        r += (100 + case1) if(game_state["code"] == 2) else (-100 - case2)
    return r

def update_q_function(game_state,new_game_state,row_q_table,fake_row_q_table):
    IA = new_game_state.get("players")[1]
    r = reward(new_game_state) 
    stp1 =  IA["stp1"]
    step = stp1[0]*8+stp1[1]
    pos = IA["st"][0]*8+IA["st"][1]
    at =  IA["at"]
    atp1 = IA["atp1"]
    Q = row_q_table[at] + 0.1*(r + 0.9*fake_row_q_table[atp1] - row_q_table[at])
    qTable = Qtable.objects.get(board = game_state["board"], posP1 = game_state.get("players")[0]["position"],posP2 = game_state.get("players")[1]["position"],playerTurn = game_state["current_player"])
    if(at == 0):
        qTable.up = Q
    elif(at == 1):
        qTable.down = Q
    elif(at == 2):
        qTable.left = Q
    else:
        qTable.right = Q
    qTable.save()
    IA["st"] = stp1