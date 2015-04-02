
var net = require('net');

var server = net.createServer(function(c){
	console.log('Client connected.');


	c.on('end', function(){
		console.log('Client disconnected.');
	});

	// Data received from user
	c.on('data', function(dataChunk){

		// Make sure the chunk is a string
		var stringData = dataChunk.toString();

		// Remove nebulous newlines
		var cleanData = stringData.replace(/(\n|\r|\r\n)$/, '');
		
		if(cleanData === 'quit'){
			console.log('Client sent quit command.');
			c.end('Quit command received. Ending connection.\r\n');
			
		} else {
			c.write('Command Received: '+cleanData+'\r\n');
		}
	});

	// Error handling
	c.on('error', function(err){
		console.error(err);
	});

	c.write('Hello client!\r\n');	
	c.pipe(c);
});

server.listen(7777, function(){
	console.log('Server listening on port 7777.');
});
