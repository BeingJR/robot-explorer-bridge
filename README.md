# PROXIE Studio DevOps Evaluation — Round 1

## Project

Bridge a Hosted Web App to a Local Python IDE Project.

## Hosted Application

GitHub Pages:

https://beingjr.github.io/robot-explorer-bridge/

## Architecture

The hosted Three.js Robot Explorer communicates with a Chrome Extension using
`window.postMessage()`.

The Chrome Extension communicates with the local Python program using a
WebSocket running on `127.0.0.1:8765`.

```text
Hosted Robot Explorer
        ↕
window.postMessage()
        ↕
Chrome Extension
        ↕
WebSocket
        ↕
Local Python
```

## How It Works

The Robot Explorer sends its position and rotation as `robot-state` messages.

The Chrome Extension receives these messages and forwards them to the local
Python WebSocket server.

Python can also send `robot-command` messages such as forward, backward,
left, right and run. The extension forwards these commands to the hosted
browser using `window.postMessage()`.

The hosted website remains a static GitHub Pages application. No backend was
added to the hosted website.

## Project Structure

```text
proxie_bridge/
├── server.py
├── requirements.txt
├── README.md
└── extension/
    ├── manifest.json
    ├── content.js
    └── background.js
```

## Setup

### 1. Install the Python Dependency

Open Command Prompt and run:

```text
pip install websockets
```

### 2. Start the Python Bridge

Open Command Prompt in the project folder and run:

```text
python server.py
```

The bridge runs at:

```text
ws://127.0.0.1:8765
```

### 3. Load the Chrome Extension

Open Chrome and go to:

```text
chrome://extensions
```

Enable **Developer mode**.

Click **Load unpacked** and select the `extension` folder.

### 4. Open the Hosted Application

Open the hosted Robot Explorer in Chrome:

```text
https://beingjr.github.io/robot-explorer-bridge/
```

The Python terminal should show:

```text
Browser connected!
Browser connected to local Python bridge
```

### 5. Test the Bridge

Type the following command in the Python terminal:

```text
w
s
a
d
run
stop
```

### 6. Demo

The demo should show the hosted Robot Explorer and the Python terminal at the same time.

The Python terminal displays the robot's live position, while commands entered in Python control the robot in the hosted browser.

Example:

```text
Python > w
Robot State: x=0.000 z=19.879 rotation=0.000
```

## 7. How It Works

The hosted Robot Explorer sends its current robot position using `window.postMessage()`.

The Chrome extension receives this browser data and forwards it to the local Python WebSocket server.

Python can also send movement commands back through the WebSocket, and the extension passes them to the hosted page.

The communication path is:

```text
Hosted Browser
      ↕
Chrome Extension
      ↕
WebSocket
      ↕
Local Python
```

## 8. Trade-offs and Security

The solution uses a Chrome extension because the hosted website is static and cannot directly connect to the local Python program.

The local WebSocket uses `ws://127.0.0.1:8765`, so the bridge is intended for local development and demonstration.

For security, the extension is restricted to the hosted Robot Explorer URL, and the Python WebSocket server listens only on `127.0.0.1`.

The main trade-off is that the user must install and enable the Chrome extension before the bridge can work.

## 9. Limitations

The bridge requires the Chrome extension to be installed and the local Python program to be running.

The WebSocket connection is local, so the Python program must run on the same computer as the browser.

The solution is designed for demonstration and development purposes rather than production use.

## 10. Conclusion

This project successfully connects a publicly hosted static Three.js application with a local Python program.

The Chrome extension acts as a bridge, allowing live robot state to be sent to Python and movement commands to be sent back to the browser in real time.
