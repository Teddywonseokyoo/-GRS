var mongoose = require('mongoose'),
	Schema = mongoose.Schema;

var GrsTaskSchema = new Schema({
	userid : String ,
	dautukey : String ,
	inputdate : { type: Date, default: Date.now } ,
	starttime : { type: Date } ,
	endtime : { type: Date } ,
	superviser : String,
	importance : Number,
	orgsourcepath : String,
	orgsourcefilename : String,
	gaugeid : String,
	result : Boolean,
});

mongoose.model('grstask', GrsTaskSchema);

