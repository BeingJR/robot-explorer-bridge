window.addEventListener("message", (event) => {
  if (event.source !== window) {
    return;
  }

  const message = event.data;

  if (!message || message.type !== "robot-state") {
    return;
  }

  chrome.runtime.sendMessage(message);
});

chrome.runtime.onMessage.addListener((message) => {
  if (message && message.type === "robot-command") {
    window.postMessage(message, "*");
  }
});
