function fadeIn(){
	let divs = document.getElementsByClassName("panelStat");
	let time = 70;
	let iDiv = 0;
	for(let div of divs){
		setTimeout(function(){div.classList.add("fade")}, time);
		setTimeout(function(){div.style.opacity = 1;}, time);
		setTimeout(function(){div.classList.toggle("fade");}, time+1000);
		if(iDiv == 1)
			time += 400;
		else
			time += 400;
		iDiv ++;
	}
}

window.onload = function(){
	fadeIn();
	let panelLeaderBoard = document.getElementById("panelLeaderBoard");
	let time = 870;
	setTimeout(function(){panelLeaderBoard.classList.add("fade")}, time);
	setTimeout(function(){panelLeaderBoard.style.opacity = 1;}, time);
	setTimeout(function(){panelLeaderBoard.classList.toggle("fade");}, time+1000);
	let divs = document.getElementsByClassName("panelStat");
	for(let div of divs){
		div.classList.add("zoom");
	}
	panelLeaderBoard.classList.add("zoom");
}