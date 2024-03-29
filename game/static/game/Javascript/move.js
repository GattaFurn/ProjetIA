function button_function(){
  let list_buttons = document.getElementsByClassName("button_move");
  
  for(let button of list_buttons){
    button.addEventListener("click", () => {main(button.moveset)});
  }
}

async function main(action) {
  let current_player = game_state["current_player"];
  let move = [];
  let positionPlayer = "position_player"+(current_player+1)
  for(let i = 0; i<action.length;i++){
    move[i]=(action[i]+game_state[positionPlayer][i]);
  }
  var response = await jsonRPC("/game/move",{"time": get_time(),"move": move});
  updateBoard(JSON.stringify(response.game_state));
  player_focused(response.game_state["current_player"],game_state["code"]);
} 

function player_focused(player_turn,code){
  let panel_player2 = document.getElementById("panelPlayer2");
  let panel_player1 = document.getElementById("panelPlayer1");
  if(code != 0){
    panel_player1.classList.add("player_panel_not_your_turn");
    panel_player1.style.opacity = 0.3;
    panel_player2.classList.add("player_panel_not_your_turn");
    panel_player2.style.opacity = 0.3;
    
    
  }else{
    if(player_turn == 1){
      panel_player1.classList.add("player_panel_not_your_turn");
      panel_player1.style.opacity = 0.3;
      panel_player2.classList.remove("player_panel_not_your_turn");
      panel_player2.style.opacity = 1;
      modified_state_button(panel_player1,panel_player2)
    }
    else{
      panel_player2.classList.add("player_panel_not_your_turn");
      panel_player2.style.opacity = 0.3;
      panel_player1.classList.remove("player_panel_not_your_turn");
      panel_player1.style.opacity = 1;
      modified_state_button(panel_player2,panel_player1)
    }
  }
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
      if (this.status >= 200 && this.status <= 300) {
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