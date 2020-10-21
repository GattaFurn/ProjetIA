let tableau = new Array();
function createBoard(current_board){
    let table = document.createElement("table");
    table.id = "grid";
    for (let iLig = 0; iLig < 8; iLig++){
        tableau[iLig] = new Array();
        let ligne = document.createElement("tr");
        table.appendChild(ligne);
        for (let iCol = 0; iCol < 8; iCol++){
            let celulle = document.createElement("td");
            box_distribution(celulle,current_board[iLig][iCol])
            ligne.appendChild(celulle);
            tableau[iLig][iCol] = celulle;
        }
    }   
    document.getElementById("my_board").appendChild(table);
}

function updateBoard(current_board){
    current_board = JSON.parse(current_board)
    for (let iLig = 0; iLig < 8; iLig++){
        for (let iCol = 0; iCol < 8; iCol++){
            box_distribution(tableau[iLig][iCol],current_board[iLig][iCol])
        }
    }   
}

function box_distribution(box,number_player){
    if(number_player == 1){
        box.style.background = "blue";
    }
    else{
        if(number_player == 2)
        box.style.background = "red";
    }
}
