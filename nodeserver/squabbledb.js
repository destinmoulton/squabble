var mongoose = require('mongoose');
var squabbledb;
var dbConnection = {};
var messageModel = {};
var context;
var settings;

module.exports = squabbledb = {
	connect: function(contextArg, callback){
		context = contextArg;
		settings = context.settings;
		
		mongoose.connect(settings.db.uri);

		dbConnection = mongoose.connection;

		// Mongoose error handler
		dbConnection.on('error', console.error.bind(console, 'connection error:'));

		dbConnection.once('open', function(){
			console.log("database connected");
			// Create the message model
			messageModel = squabbledb.messages.instantiateModel();

			callback();
		});
	},

	messages: {
		instantiateModel: function(){
			var Schema = mongoose.Schema;

			var messageSchema = new Schema({
				user: String,
				message: String,
				timestamp: Number,
				date: {type: Date, default: Date.now}
			});

			var Message = mongoose.model('Message', messageSchema, 'messages');
			return Message;	
		},

		add: function(messageObj){
			var message = messageModel(messageObj);
			message.save(function(error,message){
				if(error){
					return console.error(error);
				}
			});
		},

		getNew: function(user, beginTimestamp, callback){
			// Build the date query

			var query = messageModel.find()
								.where('user').ne(user)
								.where('timestamp').gte(beginTimestamp);
		//						.sort('date');

			query.exec(function(err, newMessages){
				if(err) return handleError(err);
				callback(newMessages);
			});

		}
	}
};
