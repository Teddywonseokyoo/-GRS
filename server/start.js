process.env.NODE_ENV = 'development';
process.env.NODE_ENV = process.env.NODE_ENV || 'development';

console.log("start server");

var express = require('./config/express_config'),
	mongoose = require('./config/mongoose');

var db = mongoose();
var app = express();
app.listen(8081);
module.exprots = app;

