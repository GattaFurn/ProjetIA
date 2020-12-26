let COLOR_CHOICES = new Map();			
COLOR_CHOICES.set('PK', '#ff99ff');
COLOR_CHOICES.set('YW', '#ffcc66');
COLOR_CHOICES.set('GN', '#d9ffb3');
COLOR_CHOICES.set('VT', '#bf80ff');
COLOR_CHOICES.set('RD', '#b30000');
COLOR_CHOICES.set('OE', '#ff8c1a');
COLOR_CHOICES.set('CN', '#80ffff');

function fadeIn(){
	let divs = document.getElementsByClassName("connect_form");
	let time = 500;
	for(let div of divs){
		setTimeout(function(){div.classList.add("fade")}, time);
		setTimeout(function(){div.style.opacity = 1;}, time);
		time += 400;
	}
}

function colorChoice(){
	let listOptions = document.getElementsByTagName("option");
	for (let elem of listOptions){
		for(let [key, value] of COLOR_CHOICES){
			if(elem.value == key)
				elem.style.backgroundColor = value;
		}
	}
}

window.onload = function(){
	fadeIn();
	colorChoice();
	let forms = document.getElementsByTagName("form");
	for(let form of forms){
		form.classList.add("zoom");
	}
}