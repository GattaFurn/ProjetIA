import random
import numpy as np
from game.models import Qtable,AIInfo
import game.business as business
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
import json
from copy import copy

actions = [
        [-1, 0], # Up
        [1, 0], #Down
        [0, -1], # Left
        [0, 1] # Right
    ]

def ia_playing(game_state):
    new_game_state = copy(game_state)
    IA = AIInfo.objects.get(id=new_game_state.get("ia_info_id")).__dict__
    q_table,row_q_table = get_q_table(new_game_state)
    IA["st"] = json.loads(IA["st"])
    IA["at"] = take_action(row_q_table, IA["eps"])
    IA["stp1"] = step(IA["at"],IA["st"])
    while(IA["stp1"] == IA["st"] or not business.correct_move(new_game_state,IA["stp1"])):
            row_q_table[IA["at"]] = 0
            IA["at"] = take_action(row_q_table, IA["eps"])
            IA["stp1"] = step(IA["at"],IA["st"])
    if(new_game_state.get("board")[IA["stp1"][0]][IA["stp1"][1]] == 0):
        new_game_state["board"][IA["stp1"][0]][IA["stp1"][1]], new_game_state["position_player2"] = business.apply_move(new_game_state,IA["stp1"])
        new_game_state["player2_box_turn"] = business.zone_search(new_game_state["board"],new_game_state["current_player"],IA["stp1"])
    else:
        new_game_state["board"][IA["stp1"][0]][IA["stp1"][1]], new_game_state["position_player2"] = business.apply_move(new_game_state,IA["stp1"])
        new_game_state["player2_box_turn"] = 0
    new_game_state["position_player2"] = IA["stp1"]
    fake_q_table,fake_row_q_table = get_q_table(new_game_state)
    IA["atp1"] = take_action(fake_row_q_table,IA["eps"])
    new_game_state["code"]= update_q_function(new_game_state,IA,row_q_table,fake_row_q_table,q_table)
    IA["st"] = IA["stp1"]
    new_game_state["current_player"] = business.switch_player(new_game_state)
    update_ia_info(IA)
    return new_game_state

def get_q_table(game_state):
    try:
        q_table = Qtable.objects.get(board = game_state["board"], pos_p1 = game_state["position_player1"],pos_p2 = game_state["position_player2"],player_turn = game_state["current_player"])
    except ObjectDoesNotExist:
        q_table = Qtable.objects.create(board = game_state["board"], pos_p1 = game_state["position_player1"],pos_p2 = game_state["position_player2"],player_turn = game_state["current_player"])
    return q_table,[q_table.up,q_table.down,q_table.left,q_table.right]

def step(action, st): #OK
    """
        Action: 0, 1, 2, 3
    """
    return[max(0, min(st[0] + actions[action][0],7)),max(0, min(st[1] + actions[action][1],7))]

def take_action(Q_table, eps): #Permet de savoir s'il doit explorer ou exploiter 
    # Take an action
    if random.uniform(0, 1) < eps:
        return(random.randint(0,3))
    else: # Or greedy action
        if(Q_table.count(0) == 4):
            return(random.randint(0,3))
        else:
            return(int(np.argmax(Q_table)))

def reward(game_state):
    r = 0
    r += game_state["player2_box_turn"] - game_state["player1_box_turn"] #Pour avoir le nombre de case prise pour le tour
    if(r == 0):
        r = 1
    case1,case2,code = business.game_is_win(game_state)
    if(code != 0 and code != 3):
        r += (100 + (case1-33)) if(code == 2) else (-100 - (case2-33))
    return r,code

def update_q_function(new_game_state,IA,row_q_table,fake_row_q_table,q_table):
    r,code = reward(new_game_state) 
    stp1 =  IA["stp1"]
    at =  IA["at"]
    atp1 = IA["atp1"]
    Q = row_q_table[at] + 0.1*(r + 0.9*fake_row_q_table[atp1] - row_q_table[at])
    if(at == 0):
        Qtable.objects.filter(id = q_table.id).update(up = Q)
    elif(at == 1):
        Qtable.objects.filter(id = q_table.id).update(down = Q)
    elif(at == 2):
        Qtable.objects.filter(id = q_table.id).update(left = Q)
    else:
        Qtable.objects.filter(id = q_table.id).update(right = Q)
    return code

def update_ia_info(IA):
    AIInfo.objects.filter(id = IA["id"]).update(st = IA["st"],stp1= IA["stp1"],at =IA["at"] ,atp1=IA["atp1"])