const { app, BrowserWindow, Menu } = require("electron");
const server = require('./index')


function createWindow() {
	// Create the browser window.
	const win = new BrowserWindow({ width: 800, height: 600 });
	
	//uncomment for debug console:
	//win.webContents.openDevTools();

	// and load the html of the app.
	win.loadFile("./camera.html");
}

app.on("ready", createWindow);
