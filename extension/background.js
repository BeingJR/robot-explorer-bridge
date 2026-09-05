const BRIDGE_URL = "ws://127.0.0.1:8765";

let socket = null;

function connect() {
  console.log("[PROXIE] Connecting to Python...");

  socket = new WebSocket(BRIDGE_URL);

  socket.addEventListener("open", () => {
    console.log("[PROXIE] Connected to Python");

    socket.send(
      JSON.stringify({
        type: "bridge-info",
        message: "Browser connected to local Python bridge",
      }),
    );
  });

  socket.addEventListener("message", (event) => {
    try {
      const message = JSON.parse(event.data);

      if (message.type === "robot-command") {
        chrome.tabs.query({}, (tabs) => {
          tabs.forEach((tab) => {
            if (
              tab.url &&
              tab.url.startsWith(
                "https://beingjr.github.io/robot-explorer-bridge/",
              )
            ) {
              chrome.tabs.sendMessage(tab.id, message);
            }
          });
        });
      }
    } catch (error) {
      console.error("[PROXIE] Invalid message", error);
    }
  });

  socket.addEventListener("close", () => {
    console.log("[PROXIE] Python disconnected. Reconnecting...");
    setTimeout(connect, 1000);
  });

  socket.addEventListener("error", () => {
    socket.close();
  });
}

chrome.runtime.onMessage.addListener((message) => {
  if (message.type === "robot-state") {
    if (socket && socket.readyState === WebSocket.OPEN) {
      socket.send(JSON.stringify(message));
    }
  }
});

connect();
