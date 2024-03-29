function fadeIn(divs){
    let time = 70;
    for(let div of divs){
    	setTimeout(function(){div.classList.add("fade")}, time);
        setTimeout(function(){div.style.opacity = 1;}, time);
        setTimeout(function(){div.classList.toggle("fade");}, time+1000);
    	time += 800;
    }
}

function fadeInTab(cellules){
    let time = 470;
    for(let cellule of cellules){
    	setTimeout(function(){cellule.classList.add("fade")}, time);
        setTimeout(function(){cellule.style.opacity = 1;}, time);
        setTimeout(function(){cellule.classList.toggle("fade");}, time+1000);
    	time += 40;
    }
}

function fadeInUnique(elem){
    let time = 70;
    setTimeout(function(){elem.classList.add("fade")}, time);
    setTimeout(function(){elem.style.opacity = 1;}, time); 
    setTimeout(function(){elem.classList.toggle("fade");}, time+1000);
}

function fadeInUniqueDark(elem){
    let time = 70;
    setTimeout(function(){elem.classList.add("fade")}, time);
    setTimeout(function(){elem.style.opacity = 0.4;}, time);
    setTimeout(function(){elem.classList.toggle("fade");}, time+1000);
}

function setPlayerName(){
    let namePlayers = document.getElementsByTagName("h2");
    let iPlayer = 1;
    for(let name of namePlayers){
        name.innerHTML = game_state["player"+iPlayer+"_username"];
        iPlayer++;
    }
}

function lightenDarkenColor(col,amt) {
    var usePound = false;
    if ( col[0] == "#" ) {
        col = col.slice(1);
        usePound = true;
    }
    var num = parseInt(col,16);
    var r = (num >> 16) + amt;
    if ( r > 255 ) r = 255;
        else if  (r < 0) r = 0;
    var b = ((num >> 8) & 0x00FF) + amt;
    if ( b > 255 ) b = 255;
        else if  (b < 0) b = 0;
    var g = (num & 0x0000FF) + amt;
    if ( g > 255 ) g = 255;
        else if  ( g < 0 ) g = 0;
    return (usePound?"#":"") + (g | (b << 8) | (r << 16)).toString(16);
}

function setColorPanelLight(){
    document.getElementById("panelPlayer1").style.backgroundColor = COLOR_CHOICES.get(game_state.player1_color);
    document.getElementById("panelPlayer2").style.backgroundColor = COLOR_CHOICES.get(game_state.player2_color);
}

function setColorPanelDark(){
    document.getElementById("panelPlayer1").style.backgroundColor = lightenDarkenColor(COLOR_CHOICES.get(game_state.player1_color), -120);
    document.getElementById("panelPlayer2").style.backgroundColor = lightenDarkenColor(COLOR_CHOICES.get(game_state.player2_color), -120);
}

function setColorInfoJoueurLight(){
    let infos = document.getElementById("panelPlayer1").getElementsByClassName("infoJoueur");
    for(let info of infos){
        info.style.backgroundColor = lightenDarkenColor(COLOR_CHOICES.get(game_state.player1_color), 60);
    }
    infos = document.getElementById("panelPlayer2").getElementsByClassName("infoJoueur");
    for(let info of infos){
        info.style.backgroundColor = lightenDarkenColor(COLOR_CHOICES.get(game_state.player2_color), 60);
    }
}

function setColorInfoJoueurDark(){
    let infos = document.getElementById("panelPlayer1").getElementsByClassName("infoJoueur");
    for(let info of infos){
        info.style.backgroundColor = lightenDarkenColor(COLOR_CHOICES.get(game_state.player1_color), -80);
    }
    infos = document.getElementById("panelPlayer2").getElementsByClassName("infoJoueur");
    for(let info of infos){
        info.style.backgroundColor = lightenDarkenColor(COLOR_CHOICES.get(game_state.player2_color), -80);
    }
}

function casesEmpty(){
    let cellules = document.getElementsByTagName("td");
    let cellulesVides = [];
    for(let cellule of cellules){
        if(cellule.style.backgroundColor == "" || cellule.style.backgroundColor == 'rgb(77, 77, 77)' || cellule.style.backgroundColor == 'rgb(217, 136, 128)')
            cellulesVides.push(cellule);
    }
    return cellulesVides;
}

let isDarkMode = false;
function darkMode(){
    let chrono = document.getElementById("chrono");
    let body = document.body;
    let cellulesTab = casesEmpty();
    let buttons = document.getElementsByTagName("button");
    let liens = document.getElementsByTagName("a");

    if(isDarkMode){
        document.querySelector("*").style.color = "black";
        body.style.backgroundColor = "#C0392B";
        for(let cellule of cellulesTab){
            cellule.style.backgroundColor = "#D98880";
        }
        setColorPanelLight();
        setColorInfoJoueurLight();
        for(let button of buttons){
            button.style.backgroundColor = "#28B463";
            button.style.color = "black";
        }
        for(let lien of liens){
            lien.style.color = "black";
        }
        chrono.style.backgroundColor = "rgb(239, 60, 60)";
        chrono.style.color = 'black';
        this.innerHTML = "Dark mode";
        isDarkMode = false;
    }
    else{
        document.querySelector("*").style.color = "white";
        body.style.backgroundColor = "#262626";
        for(let cellule of cellulesTab){
            cellule.style.backgroundColor = "#4d4d4d";
        }
        setColorPanelDark();
        setColorInfoJoueurDark();
        for(let button of buttons){
            button.style.backgroundColor = "#145214";
            button.style.color = "white";
        }
        for(let lien of liens){
            lien.style.color = "white";
        }
        chrono.style.backgroundColor = "rgb(99, 0, 0)";
        chrono.style.color = 'white';
        this.innerHTML = "Light mode";
        isDarkMode = true;
    }
}

let startTime = 0;
let start = 0;
let end = 0;
let diff = 0;
let timerID = 0;

function chrono(){
    end = new Date();
    diff = end - start;
    diff = new Date(diff);
    var sec = diff.getSeconds();
    var min = diff.getMinutes();
    var hr = diff.getHours()-1;
    if (min < 10){
        min = "0" + min;
    }
    if (sec < 10){
        sec = "0" + sec;
    }
    document.getElementById("chrono").innerHTML = hr + ":" + min + ":" + sec;
    timerID = setTimeout("chrono()", 10);
    if(game_state.code != 0){
        chronoStop();
    }
}

function chronoStart(){
    start = new Date();
    chrono();
    let buttonsMove = document.getElementsByClassName("button_move");
    for(let but of buttonsMove){
        but.removeEventListener("click", chronoStart);
    }
}

function chronoStop(){
    clearTimeout(timerID);
}

function bouton_creation(){
    const flèches = new Map();
    flèches.set("↑",[-1,0]);
    flèches.set("←",[0,-1]);
    flèches.set("↓",[1,0]);
    flèches.set("→",[0,1]);
    let divs = document.getElementsByClassName("button");
    for(div of divs){
        for (const[key,value] of flèches){
            let button = document.createElement("button");
            if(key == "↑")
                button.id = "boutonHaut";
            button.classList.add("button_move");
            button.classList.add("zoom");
            button.innerHTML = key;
            button.moveset = value;
            div.appendChild(button);
        }
    }
}

window.onload = function(){
    bouton_creation();
    button_function();
    createBoard();
    setColorPanelLight();
    setPlayerName();
    setColorInfoJoueurLight();

    let disconnection = document.getElementById("disconnection")
    fadeInUnique(disconnection);

    let darkModeButton = document.getElementById("dark_mode");
    fadeInUnique(darkModeButton);
    darkModeButton.addEventListener("click", darkMode);

    let newGame = document.getElementById("newGame");
    fadeInUnique(newGame);

    let chrono = document.getElementById("chrono");
    fadeInUnique(chrono);

    let panelPlayer1 = document.getElementById("panelPlayer1");
    fadeInUnique(panelPlayer1);

    let panelPlayer2 = document.getElementById("panelPlayer2");
    fadeInUniqueDark(panelPlayer2);

    let blackPanels = document.getElementsByClassName("blackPanel");
    fadeIn(blackPanels);

    let cases = document.getElementsByTagName("td");
    fadeInTab(cases);

    player_focused(game_state["current_player"],game_state["code"]);

    let buttonsMove = document.getElementsByClassName("button_move");
    for(let but of buttonsMove){
        but.addEventListener("click", chronoStart);
    }
}