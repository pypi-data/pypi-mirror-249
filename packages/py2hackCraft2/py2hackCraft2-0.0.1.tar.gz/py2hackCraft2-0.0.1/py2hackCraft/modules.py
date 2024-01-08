import websocket
import threading
import time
import json

class WebSocketClient:
    def __init__(self, url):
        self.url = url
        self.ws = websocket.WebSocketApp(url,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)
        self.ws.on_open = self.on_open
        self.thread = threading.Thread(target=self.ws.run_forever)
        self.thread.daemon = True
        self.lock = threading.Lock()
        self.connected = False
        self.response_event = threading.Event()  # イベントオブジェクトを追加
        self.last_message = None  # 最後に受信したメッセージを保持

    def on_message(self, ws, message):
        print("Received '%s'" % message)
        self.last_message = message  # 最後に受信したメッセージを更新
        self.response_event.set()  # イベントをセットして、メッセージの受信を通知

    def on_error(self, ws, error):
        print("Error '%s'" % error)

    def on_close(self, ws, close_status_code, close_msg):
        print("### closed ###")
        self.connected = False

    def on_open(self, ws):
        print("Opened connection")
        self.connected = True

    def run_forever(self):
        self.thread.start()

    def wait_for_connection(self):
        while not self.connected:
            time.sleep(0.1)  # Wait for connection to be established

    def send(self, message):
        self.wait_for_connection()
        with self.lock:
            self.response_event.clear()  # イベントをクリアして新しいレスポンスの準備をする
            self.ws.send(message)
            self.response_event.wait()  # サーバーからのレスポンスを待つ
        return self.last_message  # 最後に受信したメッセージを返す

    def close(self):
        self.ws.close()
        self.thread.join()


class Entity:
    def __init__(self, url, player, entity):
        self.client = None  # 初期化時にはWebSocketClientはNone
        self.url = url
        self.player = player
        self.entity = entity

    def connect(self):
        print("Connecting to %s %s %s" %( self.url, self.player, self.entity))
        if not self.client:
            self.client = WebSocketClient(self.url)  # 遅延初期化
            self.client.run_forever()
            self.client.send(json.dumps({
                "type": "connect2",
                "data": {
                    "player": self.player,
                    "entity": self.entity,
                }
            }))

    def disconnect(self):
        if self.client:
            self.client.close()
            self.client = None            
            self.player = None
            self.entity = None

    def forward(self):
        message = {
            "type": "call",
            "data": {
                "name": "forward"
            }
        }
        self.client.send(json.dumps(message))

    def back(self):
        message = {
            "type": "call",
            "data": {
                "name": "back"
            }
        }
        self.client.send(json.dumps(message))

    def up(self):
        message = {
            "type": "call",
            "data": {
                "name": "up"
            }
        }
        self.client.send(json.dumps(message))

    def down(self):
        message = {
            "type": "call",
            "data": {
                "name": "down"
            }
        }
        self.client.send(json.dumps(message))

    def turnLeft(self):
        message = {
            "type": "call",
            "data": {
                "name": "turnLeft"
            }
        }
        self.client.send(json.dumps(message))        

    def turnRight(self):
        message = {
            "type": "call",
            "data": {
                "name": "turnRight"
            }
        }
        self.client.send(json.dumps(message))               