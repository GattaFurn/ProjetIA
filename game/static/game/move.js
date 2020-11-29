function button_function(){
  list_buttons = document.getElementsByClassName("button_move");
  
  for(let button of list_buttons){
    button.addEventListener("click", () => {main(button.moveset)});
  }
}

async function main(action) {
  let current_player = game_state["players"][game_state["current_player"]];
  let move = [];
  for(let i = 0; i<2;i++){
    move[i]=action[i]+current_player["position"][i];
  }
  var response = await jsonRPC("/game/move",{"game_state": game_state,"move": move});
  updateBoard(JSON.stringify(response.game_state));
  player_focused(response.game_state["current_player"]);
}

async function ia_play(){
  if(game_state["players"][game_state["current_player"]]["Q_table"] != undefined){
    var response = await jsonRPC("/game/iamove",{"game_state": game_state});
    updateBoard(JSON.stringify(response.game_state));
    player_focused(response.game_state["current_player"]);
  }
}

function player_focused(player_turn){
  let panel_player2 = document.getElementById("player2_panel_color");
  let panel_player1 = document.getElementById("player1_panel_color"); 
  if(player_turn == 1){
    panel_player1.classList.add("player_panel_not_your_turn");
    panel_player2.classList.remove("player_panel_not_your_turn");
    modified_state_button(panel_player1,panel_player2)
  }
  else{
    panel_player2.classList.add("player_panel_not_your_turn");
    panel_player1.classList.remove("player_panel_not_your_turn");
    modified_state_button(panel_player2,panel_player1)
  }
  ia_play();
}

function modified_state_button(button_1,button_2){
  for(let button of button_1.querySelectorAll("button")){
    button.setAttribute("disabled", "");
  }
  for(let button of button_2.querySelectorAll("button")){
    button.removeAttribute("disabled");
  }
}

function jsonRPC(url, data) {
  return new Promise(function (resolve, reject) {
    let xhr = new XMLHttpRequest();
    xhr.open("POST", url);
    xhr.setRequestHeader("Content-type", "application/json");
    const csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;
    xhr.setRequestHeader("X-CSRFToken", csrftoken);
    xhr.onload = function () {
      if (this.status >= 200 && this.status <= 500) {
        resolve(JSON.parse(xhr.response));
      } else {
        reject({
          status: this.status,
          statusText: xhr.statusText,
        });
      }
    };
    xhr.onerror = function () {
      reject({
        status: this.status,
        statusText: xhr.statusText,
      });
    };
    xhr.send(JSON.stringify(data));
  });
}