import config from '../core/config';

export const connectWebSocket = (token, onMessage, threadId) => {
  const url = new URL(config.WEBSOCKET_URL);
  url.searchParams.append('token', token);
  url.searchParams.append('thread_id', threadId);

  const socket = new WebSocket(url.toString());

  socket.onopen = function () {
    console.log("Connected to WebSocket");
  };

  socket.onmessage = function (event) {
    console.log("Received:", event.data);
    if (onMessage) {
      onMessage(event.data);
    }
  };

  socket.onclose = function (event) {
    console.log("WebSocket closed:", event);
  };

  socket.onerror = function (error) {
    console.error("WebSocket error:", error);
  };

  return socket;
};
