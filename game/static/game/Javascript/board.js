let tableau = new Array();

function createBoard(){
    let info = document.getElementsByClassName("infoJoueur");
    info[0].innerHTML = 0;
    info[2].innerHTML = 0;
    let current_board = game_state["board"];
    let table = document.createElement("table");
    table.id = "board_letter_number";

    let ligne = document.createElement("tr");
    let celulle = document.createElement("td");
    ligne.appendChild(celulle);
	for (let i = 1; i <= 8; i++) {
        let celulle = document.createElement("td");
        celulle.innerHTML = i
        ligne.appendChild(celulle);
    }
    table.appendChild(ligne);

    for (let iLig = 0; iLig < 8; iLig++){
        tableau[iLig] = new Array();
        let ligne = document.createElement("tr");
        table.appendChild(ligne);

        let celulle = document.createElement("td");
        celulle.innerHTML = iLig+1;
        ligne.appendChild(celulle);
        for (let iCol = 0; iCol < 8; iCol++){
            let celulle = document.createElement("td");
            box_distribution(celulle,current_board[iLig][iCol],info)
            ligne.appendChild(celulle);
            tableau[iLig][iCol] = celulle;
        }
    }
    player_position(game_state.players[0].position,game_state.players[1].position)
    document.getElementById("my_board").appendChild(table);
}

function updateBoard(game){
    let info = document.getElementsByClassName("infoJoueur");
    info[0].innerHTML = 0;
    info[2].innerHTML = 0;
    game_state = JSON.parse(game);
    current_board = game_state["board"]
    for (let iLig = 0; iLig < 8; iLig++){
        for (let iCol = 0; iCol < 8; iCol++){
            box_distribution(tableau[iLig][iCol],current_board[iLig][iCol],info);
        }
    }
    game_state["time"] = get_time();
    player_position(game_state.players[0].position,game_state.players[1].position);
    game_state["board"] = current_board;
    if(game_state["code"] != 0){
        if(game_state.code == 3)
            alert("And it's a tie!");
        else{
            if(game_state.code == 1)
                alert(`Congratulations ${game_state.players[0].username}, you are the winner!`);
            else
                alert(`Congratulations ${game_state.players[1].username}, you are the winner!`);
        }
    }    
}


function get_time(){
    let time = document.getElementById("chrono");
    let result = `${time.innerHTML.substr(0,1)}`;
    result += `${time.innerHTML.substr(2,2)}`;
    result += `${time.innerHTML.substr(5,6)}`;
    return result;
  }

let COLOR_CHOICES = new Map();
                COLOR_CHOICES.set('BL', '#0099ff');
                COLOR_CHOICES.set('PK', '#ff99ff');
                COLOR_CHOICES.set('YW', '#ffcc66');
                COLOR_CHOICES.set('GN', '#80ff80');
                COLOR_CHOICES.set('VT', '#bf80ff');
                COLOR_CHOICES.set('RD', '#b30000');
                COLOR_CHOICES.set('OE', '#ff8c1a');
                COLOR_CHOICES.set('CN', '#80ffff');
                


function box_distribution(box,number_player,info,){
    if(number_player == 1){
        info[0].innerHTML = parseInt(info[0].innerHTML) + 1;
        box.style.background = COLOR_CHOICES.get(game_state.players[0].color);
    }
    else{
        if(number_player == 2){
            info[2].innerHTML = parseInt(info[2].innerHTML) + 1;;
            box.style.background = COLOR_CHOICES.get(game_state.players[1].color);
        }
    }
    if(box.childElementCount != 0){
        box.childNodes[0].remove();
    }
}

function player_position(posPlayer1,posPlayer2){
    let image = document.createElement("img");
    image.src = pic1;
    image.className ="image_joueur";
    tableau[posPlayer1[0]][posPlayer1[1]].appendChild(image);
    image = document.createElement("img");
    image.className ="image_joueur";
    image.src = pic2;
    tableau[posPlayer2[0]][posPlayer2[1]].appendChild(image);
}
