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
	complete_number();
}

function complete_number(){
	document.getElementById("GamePlayed").append(nbGamePlayed);
	document.getElementById("IaGame").append(nbIaGame);
	document.getElementById("PlayerGame").append(nbPlayerGame);
	document.getElementById("averageDuration").append(averageTime.toFixed(2));
	document.getElementById("maxDuration").append(maxTime);
	document.getElementById("minDuration").append(minTime);
	document.getElementById("totalBox").append(totalBoxTaken);
	document.getElementById("maxBox").append(maxBoxTaken);
	document.getElementById("averageBox").append(averageBoxTaken.toFixed(2));
} 