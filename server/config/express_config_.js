var express = require('express'),
	morgan = require('morgan'),
   	compress = require('compression'),
   	bodyParser = require('body-parser'),
    	methodOverride = require('method-override'),
    	config = require('./config'),
    	session = require('express-session');


module.exports = function() {
	var app = express();
	if(process.env.NODE_ENV == 'development'){
		app.use(morgan('dev'));
	}
	else if(process.env.NODE_ENV == 'production'){
		app.use(compress());
	}
	app.use(bodyParser.urlencoded({
        	extended : true
    	}));
	app.use(bodyParser.json());
	app.use(methodOverride());
  app.use(function(req, res, next) {
    //모든 도메인의 요청을 허용하지 않으면 웹브라우저에서 CORS 에러를 발생시킨다.
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'X-Requested-With,content-type, Authorization');
    next();
  });

	app.use(session({
		saveUninitialized : true,
        	resave : true,
        	secret : config.sessionSecret
	}));
	app.set('views','../app/views');
	app.set('view engine','ejs');
	require('../app/routes/index.server.routes.js')(app);
	require('../app/routes/grs.server.routes.js')(app);
	app.use(express.static('../static'));
	return app;
}
