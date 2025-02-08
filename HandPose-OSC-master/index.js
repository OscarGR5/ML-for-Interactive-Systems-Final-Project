const io = require("socket.io")();
const { Client } = require('node-osc');
const client = new Client('127.0.0.1', 8008);

io.on("connection", (socket) => {
	console.log("Socket is connected with Electron App");
	socket.on("dispatch", (data) => {
		if (data.oscFormatting.handInViewConfidence) {
			client.send("/handInViewConfidence", data.predictions.handInViewConfidence)
		}
		if (data.oscFormatting.boundingBox) {
			client.send("/boundingBox/topLeft", data.predictions.boundingBox.topLeft)
			client.send("/boundingBox/bottomRight", data.predictions.boundingBox.bottomRight)
		}
		if (data.oscFormatting.landmarks) {
			client.send("/landmarks", data.predictions.landmarks)
		}
		if (data.oscFormatting.annotations) {
			let annotations = data.predictions.annotations;
			for (var key in annotations) {
				if (annotations.hasOwnProperty(key)) {
					client.send("/annotations/" + key, annotations[key]);
				}
			}
		}
	});

	socket.on("oscPortSet", (port) => {
		client.port = port;
		console.log('OSC port set to', client.port);
	});

	socket.on("hostSet", (host) => {
		client.host = host;
		console.log('Host set to', client.host);
	});
});

io.listen(3000);