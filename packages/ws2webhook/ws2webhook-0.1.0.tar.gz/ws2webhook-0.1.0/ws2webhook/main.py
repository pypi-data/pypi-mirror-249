import json
import requests
import websocket

class Ws2webhook:
    def __init__(self, ws_endpoint: str, webhook_endpoint: str) -> None:
        self.ws_endpoint = ws_endpoint
        self.webhook_endpoint = webhook_endpoint
        self.ws_app = websocket.WebSocketApp(ws_endpoint, on_open=self._on_open, on_message=self._on_message, on_error=self._on_error, on_close=self._on_close)

    def run(self):
        self.ws_app.run_forever()

    def _on_message(self, ws, message) -> None:
        data = json.loads(message)
        req = requests.post(self.webhook_endpoint, json=data)
        print('got a message: ', data, '\n', 'data sent: ', req.status_code, ' ', req.json())

    def _on_error(self, ws, error) -> None:
        print('error occurred: ', error)

    def _on_close(self, ws, close_status_code, close_msg) -> None:
        print('disconnected streaming server: ', close_status_code, close_msg)

    def _on_open(self, ws) -> None:
        print('connected streaming server')
