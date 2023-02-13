var rotation = 0;
var rotated;
var list;
var angle = 5;
var home; 

function onload() {
	console.log("loaded!")
	if (document.getElementById('rotateDanny')){
		rotated = document.getElementById('rotateDanny');
		list = document.getElementById('Club Members');
		rotated.addEventListener("click", rotate);
		console.log("Valid Onload");
	}
	else{
		home = document.getElementById('returnButton');
		home.addEventListener("click", returnHome);
		console.log("Invalid Onload")
	}
	
}

function rotate(){
	console.log("attempting to rotate")
	rotation = (rotation + angle) % 360;
	rotated.style.transform = `rotate(${rotation}deg)`;
	console.log("Rotating")
}

function addMember(){
	var li = document.createElement("li");
	var candidate = document.getElementById('name')
	li.appendChild(document.createTextNode(candidate.value));
    list.appendChild(li);
}

function returnHome(){
	location.href = '/'
}

function goToSurvey(){
	location.href = '/survey'
}