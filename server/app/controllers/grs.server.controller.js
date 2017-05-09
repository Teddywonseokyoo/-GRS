var Grstask = require('mongoose').model('grstask');
var multer  =   require('multer');
var config = require('../../config/config');
//var sourcepath = '/home/aeye_grs/storage/org_files/';
exports.upload  = function(req,res) {
	var orgsourcepath = '';
	var storage =   multer.diskStorage({
  		destination: function (req, file, callback){
    			callback(null, config.uploadpath);
  		},
  		filename: function (req, file, callback)
  		{
			//var fdata_ = JSON.parse(req.body.fdata);
			//console.log(req);
			var filename = file.fieldname+ '-' + Date.now() + '.jpg';
    			callback(null, filename );
 			orgsourcefilename =  filename;
		}
	});	
	multer({ storage : storage}).single('userPhoto')(req,res,function(err) {
    		if(err) {
			console.log(err);
			return res.end("Error uploading file.");
  		}
		var fdata = JSON.parse(req.body.fdata);
		fdata.newProperty = 'inputdata';
		fdata.newProperty = 'starttime';
		fdata.newProperty = 'endtime';
		fdata.newProperty = 'superviser';
		fdata.newProperty = 'importance';
		fdata.newProperty = 'orgsourcepath';
		fdata.newProperty = 'orgsourcefilename';
		fdata.newProperty = 'gaugeid';
		fdata.newProperty = 'result';
		var curdatetime = new Date();
		fdata.inputdata = curdatetime;
		fdata.starttime = ''
		fdata.endtime = ''
		fdata.superviser = ''; 
		fdata.importance = 1;
		fdata.orgsourcepath = config.uploadpath;
		fdata.orgsourcefilename = orgsourcefilename;
		fdata.gaugeid = '';
		fdata.result = false;
		console.log(fdata);
		var data = new Grstask(fdata);
		data.save(function(err){
        		if(err) {
           	 		res.status(500);
        		} else {
            			res.json(data);
        		}
		});
		//console.log(req.file);
  		//res.end("File is uploaded");
		//res.status.(204).end();
	});
};
