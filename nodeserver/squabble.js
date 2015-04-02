/**
 * The Squabble Chat Client
 * 
 * @author Destin Moulton
 */

var readline = require('readline');
var username = "";
var rl = readline.createInterface({
	input: process.stdin,
	output: process.stdout
});
rl.write("******************\r\n");
rl.write("**** SQUABBLE ****\r\n");
rl.write("******************\r\n");
rl.question('What is your username? ', function(userAnswer){
	username = userAnswer;
	messagePrompt();
});

function messagePrompt(){
	rl.setPrompt(username+'> ');
	rl.prompt();
	rl.on('line', function (cmd){
		console.log('You just typed: '+cmd);
		rl.prompt();
	});

	rl.on('pause', function (){
		console.log('readline paused');
	});

	rl.on('resume', function (){
		console.log('readline resumed');
	});
}
