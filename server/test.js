var PythonShell = require('python-shell');

var options = {
  args: ['userPhoto-1482481080957.jpg']
};

PythonShell.run('./engine_grs/manager.py', options, function (err, results) {
  if (err) throw err;
  // results is an array consisting of messages collected during execution
  console.log('results: %j', results);
});
