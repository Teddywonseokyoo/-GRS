var file = require('../controllers/grs.server.controller');
var file2 = require('../controllers/grs.server.controller2');
module.exports = function(app) {
  	app.post('/api/req_grs', file.upload);
        app.post('/api/req_grs2', file2.upload);	
}

