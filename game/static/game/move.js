window.onload = function() {
    list_buttons = document.getElementsByClassName("button_move");
    
    for(let button of list_buttons){
      button.addEventListener("click", () => {main()});
    }

}

async function main() {
    const response = await jsonRPC("/game/move",{game_state: game_state,move: [1, 0]});
    //document.getElementById("my_board").textContent = JSON.stringify(response.board)
    updateBoard(JSON.stringify(response.game_state))
}

function jsonRPC(url, data) {
    return new Promise(function (resolve, reject) {
      let xhr = new XMLHttpRequest();
      xhr.open("POST", url);
      xhr.setRequestHeader("Content-type", "application/json");
      const csrftoken = document.querySelector("[name=csrfmiddlewaretoken]")
        .value;
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