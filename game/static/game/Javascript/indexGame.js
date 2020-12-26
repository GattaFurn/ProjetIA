let COLOR_CHOICES = new Map();
COLOR_CHOICES.set('BL', '#0099ff');
COLOR_CHOICES.set('PK', '#ff99ff');
COLOR_CHOICES.set('YW', '#ffcc66');
COLOR_CHOICES.set('GN', '#d9ffb3');
COLOR_CHOICES.set('VT', '#bf80ff');
COLOR_CHOICES.set('RD', '#b30000');
COLOR_CHOICES.set('OE', '#ff8c1a');
COLOR_CHOICES.set('CN', '#80ffff');
    

function createDiv(){
  let div = document.getElementById("connect_div");
  let button = document.createElement("button");
  button.append(document.createElement("a"));
  button.childNodes[0].href = "/connection";
  button.childNodes[0].innerHTML = "Connection";
  let h2;
  let p = [];
  let div_player = [];
  let ind = 0;
  for(player of [player1,player2]){
    div_player[ind] = document.createElement("div");
    div_player[ind].className = "connect_form";
    h2 = document.createElement("h2");
    h2.innerHTML = "Player "+(ind+1);
    div_player[ind].append(h2);
    if(player == null){
      div_player[ind].append(button); 
    }
    else{
      p[0] = document.createElement("p");
      p[0].classList.add("playerName");
      p[0].innerHTML = "Player name"

      p[1] = document.createElement("p");
      p[1].classList.add("infoJoueur");
      p[1].innerHTML = player.username;

      p[2] = document.createElement("p");
      p[2].classList.add("playerColor");
      p[2].innerHTML = "Player color"

      p[3] = document.createElement("div");
      p[3].classList.add("divCouleur");
      p[3].style.backgroundColor = COLOR_CHOICES.get(player.color);
      div_player[ind].append(p[0],p[1], p[2], p[3]);
    }
    ind++;
  }
  div.append(div_player[0]);
  div.append(div_player[1]);
}

function fadeIn(){
	let divs = document.getElementsByClassName("connect_form");
	let time = 70;
	for(let div of divs){
		setTimeout(function(){div.classList.add("fade")}, time);
    setTimeout(function(){div.style.opacity = 1}, time);
    setTimeout(function(){div.classList.toggle("fade");}, time+1000);
		time += 800;
	}
  time = 470;
  let butStart = document.getElementById("startGame");
  setTimeout(function(){butStart.classList.add("fade")}, time);
  setTimeout(function(){butStart.style.opacity = 1}, time);
  setTimeout(function(){butStart.classList.toggle("fade");}, time+1000);

  time += 800;
  let disconnection = document.getElementById("disconnection");
  setTimeout(function(){disconnection.classList.add("fade")}, time);
  setTimeout(function(){disconnection.style.opacity = 1}, time);
  setTimeout(function(){disconnection.classList.toggle("fade");}, time+1000);
}

function zoom(){
  let divs = document.getElementsByClassName("connect_form");
  for(let div of divs){
    div.classList.add("zoom");
  }
  let butStart = document.getElementById("startGame");
  butStart.classList.add("zoom");
  let butDisc = document.getElementById("disconnection");
  butDisc.classList.add("zoom");
}

window.onload = function(){
  createDiv();
  let connectDiv = document.getElementById("connect_div");
  
  let versusDiv = document.createElement("div");
  versusDiv.id = "versusDiv";
  let div3 = connectDiv.lastChild;
  connectDiv.insertBefore(versusDiv, div3);
  
  let divV = document.createElement("div");
  divV.id = "divV";
  versusDiv.appendChild(divV);
  
  let pVersus = document.createElement("p");
  pVersus.innerHTML = "VERSUS";
  pVersus.id = "pVersus";
  divV.appendChild(pVersus);
  
  let buttonStart = document.createElement("button");
  buttonStart.type = "submit";
  buttonStart.id = "startGame";
  buttonStart.classList.add("aniBut");
  buttonStart.innerHTML = "Start the game";
  versusDiv.appendChild(buttonStart);
  zoom();
  fadeIn();
}

