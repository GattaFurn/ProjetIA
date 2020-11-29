from game.business import * 
import random
import numpy as np

actions = [
        [-1, 0], # Up
        [1, 0], #Down
        [0, -1], # Left
        [0, 1] # Right
    ]

def index(request):
    data = json.loads(request.body)
    direction = [0,1,2,3]
    game_state = data.get("game_state")
    IA = game_state.get("players")[game_state["current_player"]]
    st = game_state.get("players")[game_state["current_player"]]["position"]
    fake_row_q_table = list(IA.get("Q_table")[st[0]*8+st[1]])
    at = take_action(fake_row_q_table, 0.4, direction)
    stp1 = step(at,st)
    while(stp1 == st or not correct_move(game_state,stp1)):
            fake_row_q_table[at] = 0
            at = take_action(fake_row_q_table, 0.4,direction)
            stp1 = step(at,st)
    if(game_state.get("board")[stp1[0]][stp1[1]] == 0):
        apply_move(game_state,stp1)
        zone_search(game_state["board"],game_state["current_player"],stp1)
    else:
        square_taken = 0
    game_state.get("players")[game_state["current_player"]]["position"] = stp1
    game_state.get("players")[game_state["current_player"]]["atp1"] = take_action(IA.get("Q_table")[stp1[0]*8+stp1[1]], 0.0,[0,1,2,3])
    switch_player(game_state)
    return JsonResponse({"game_state":game_state})

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

def reward(self,):
    reward = IA.square_taken - player[IA.player_nb % 2].square_taken
    IA.update_q_function(reward)

def update_q_function(reward,IA):
    stp1 =  IA["position"]
    step = stp1[0]*8+stp1[1]
    pos = IA["st"][0]*8+IA["st"][1]
    at =  IA["at"]
    atp1 = IA["atp1"]
    IA["Q_table"][pos][at] = IA.get("Q_table")[pos][at] + 0.1*(reward + 0.9*IA.Q_table[step][atp1] - IA.get("Q_table")[pos][at])
    IA["st"] = stp1