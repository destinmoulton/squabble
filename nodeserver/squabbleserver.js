var net = require('net');
var events = require('events');
var context = {};
var settings = require('./settings.js');

var clients = [];

context.settings = settings;

var squabbledb = require('./squabbledb.js');

// Connect to the database and then setup the chat server
squabbledb.connect(context, function(){
	setupChatServer();
});


function setupChatServer(){
	var server = net.createServer(function(c){
		
		console.log('Client connected.');

		clients.push(c);

		c.on('end', function(){
			console.log('Client disconnected.');
		});

		// Data received from user
		c.on('data', function(dataChunk){

			// Make sure the chunk is a string
			var stringData = dataChunk.toString();

			// Remove nebulous newlines
			//var cleanData = stringData.replace(/(\n|\r|\r\n)$/, '');
			
			//Expects a JSON string
			var jsonData = JSON.parse(stringData);

			var command = jsonData['command'];
			
			if(command === 'quit'){
				console.log('Client sent quit command.');
				c.end('Quit command received. Ending connection.\r\n');
			} else if(command === 'broadcast'){
				console.log(jsonData['message']);
				var newMessage = {
					user: jsonData['user'],
					message: jsonData['message'],
					timestamp: jsonData['timestamp']					
				};
				squabbledb.messages.add(newMessage);
			} else if(command === 'acquire'){

				squabbledb.messages.getNew(jsonData['user'], jsonData['time_last_checked'], function(newMessages){
					jsonString = String(JSON.stringify(newMessages));

					broadcast(jsonString, c);
					//connection.write(jsonString);
				});
			} 
		});

		function broadcast(message, receiver){
			clients.forEach(function(client){
				if(client===receiver){
					client.write(message);
				}
			});
		}

		// Error handling
		c.on('error', function(err){
			console.error(err);
		});

		c.write('Hello client!\0');	
		//c.pipe(c);
	});

	server.listen(7777, function(){
		console.log('Server listening on port 7777.');
	});
}
