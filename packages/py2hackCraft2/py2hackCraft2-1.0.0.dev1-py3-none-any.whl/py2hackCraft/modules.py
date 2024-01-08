import websocket
import threading
import time
import json
import logging
from dataclasses import dataclass
from typing import Callable, Any

def str_to_bool(s):
    """
    文字列をブール値に変換する。

    Args:
        s (str): "true" または "false"（大文字小文字は無視）

    Returns:
        bool: 変換されたブール値。"true"ならTrue、"false"ならFalse
    """
    if s.lower() == 'true':
        return True
    elif s.lower() == 'false':
        return False
    else:
        raise ValueError(f"Cannot covert {s} to a boolean.")  # 有効な文字列でない場合はエラー


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
        self.callbacks = {}  # コールバック関数を保持

    def setCallback(self, eventName, callbackFunc):
            self.callbacks[eventName] = callbackFunc

    def on_message(self, ws, message):
        logging.debug("on_message '%s'" % message)
        try:
            jsonMessage = json.loads(message)
            type = jsonMessage['type']
            data = jsonMessage['data']
            if(type == 'result'):
                self.result = data
            elif(type == 'error'):
                self.error = data
            elif(type == 'connected'):
                self.connected = True
                self.entityUUID = data
            elif(type == 'event'):
                jsonEvent = json.loads(data)
                eventName = jsonEvent['name']
                logging.debug("on event %s '%s'" %(eventName, jsonEvent['data']))
                if eventName in self.callbacks:
                    self.callbacks[eventName](jsonEvent['data'])    
            self.response_event.set()  # イベントをセットして、メッセージの受信を通知
        except json.JSONDecodeError:
            logging.error("JSONDecodeError '%s'" % message)    

    def on_error(self, ws, error):
        logging.debug("on_error '%s'" % error)

    def on_close(self, ws, close_status_code, close_msg):
        logging.debug("### closed ###")
        self.connected = False

    def on_open(self, ws):
        logging.debug("Opened connection")
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

    def sendCall(self, name, args=None):
        data = {"name": name}
        if args is not None:
            data['args'] = args            
        message = {
            "type": "call",
            "data": data
        }
        self.send(json.dumps(message))


@dataclass
class Location:
    x: int
    y: int
    z: int
    world: str = "world"


@dataclass
class ChatMessage:
    """
    チャットメッセージを表すデータクラス。

    Attributes:
        player (str): プレイヤー名または識別子。
        uuid (str): プレイヤーの一意の識別子（UUID）。
        message (str): プレイヤーがチャットで送信したメッセージの内容。
    """
    player: str
    uuid: str
    message: str

@dataclass
class RedstonePower:
    """
    レッドストーン信号を表すデータクラス。

    Attributes:
        oldCurrent (int): 前のレッドストーン信号の強さ
        newCurrent (int): 最新のレッドストーン信号の強さ
    """
    oldCurrent: int
    newCurrent: int

@dataclass
class Block:
    """
    ブロックを表すデータクラス。

    Attributes:
        name (str): ブロックの種類。
        data (int): ブロックのデータ値。
        isLiquid (bool): 液体ブロックかどうか。
        isAir (bool): 空気ブロックかどうか。
        isBurnable (bool): 燃えるブロックかどうか。
        isFuel (bool): 燃料ブロックかどうか。
        isOccluding (bool): 透過しないブロックかどうか。
        isSolid (bool): 壁のあるブロックかどうか。
        isPassable (bool): 通過可能なブロックかどうか。
        x (int): ブロックのX座標。
        y (int): ブロックのY座標。
        z (int): ブロックのZ座標。
    """
    name: str
    data: int
    isLiquid: bool
    isAir: bool
    isBurnable: bool
    isFuel: bool
    isOccluding: bool
    isSolid: bool
    isPassable: bool
    x: int
    y: int
    z: int

class Entity:
    """
    エンティティを表すクラス。
    """
    def __init__(self, url: str, player: str, entity: str):
        self.client = None  # 初期化時にはWebSocketClientはNone
        self.url = url
        self.player = player
        self.entity = entity

    def connect(self):
        """
        設定されているプレイヤーのエンティティに接続する。
        """
        logging.debug("Connecting to %s %s %s" %( self.url, self.player, self.entity))
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
        """
        接続しているエンティティから切断する。
        """
        if self.client:
            self.client.close()
            self.client = None            
            self.player = None
            self.entity = None

    def setOnPlayerChat(self, callbackFunc: Callable[['Entity', 'ChatMessage'], Any]):
        """
        チャットを受信したときに呼び出されるコールバック関数を設定する。
        """
        def callbackWrapper(data):
            logging.debug("callbackWrapper '%s'" % data)
            chatMessage = ChatMessage(**data)
            callbackFunc(self, chatMessage)
        self.client.setCallback('onPlayerChat', callbackWrapper)

    def setOnRedstoneChange(self, callbackFunc: Callable[['Entity', 'RedstonePower'], Any]):
        """
        レッドストーンを受信したときに呼び出されるコールバック関数を設定する。
        """
        def callbackWrapper(data):
            logging.debug("callbackWrapper '%s'" % data)
            power = RedstonePower(**data)
            callbackFunc(self, power)
        self.client.setCallback('onEntityRedstone', callbackWrapper)

    def forward(self):
        """
        エンティティを前方に移動させる。
        """
        self.client.sendCall("forward")

    def back(self):
        """
        エンティティを後方に移動させる。
        """
        self.client.sendCall("back")

    def up(self):
        """
        エンティティを上方に移動させる。
        """
        self.client.sendCall("up")

    def down(self):
        """
        エンティティを下方に移動させる。
        """
        self.client.sendCall("down")

    def turnLeft(self):
        """
        エンティティを左に回転させる。
        """
        self.client.sendCall("turnLeft")

    def turnRight(self):
        """
        エンティティを右に回転させる。
        """
        self.client.sendCall("turnRight")

    def place(self):
        """
        エンティティの前方にブロックを設置する。
        """
        self.client.sendCall("placeFront")

    def placeUp(self):
        """
        エンティティの真上にブロックを設置する。
        """
        self.client.sendCall("placeUp")

    def placeDown(self):
        """
        エンティティの真下にブロックを設置する。
        """
        self.client.sendCall("placeDown")

    def useItem(self):
        """
        エンティティの前方にアイテムを使う
        """
        self.client.sendCall("useItemFront")

    def useItemUp(self):
        """
        エンティティの真上にアイテムを使う
        """
        self.client.sendCall("useItemUp")

    def useItemDown(self):
        """
        エンティティの真下にアイテムを使う
        """
        self.client.sendCall("useItemDown")

    def dig(self):
        """
        エンティティの前方のブロックを壊す。
        """
        self.client.sendCall("digFront")

    def digUp(self):
        """
        エンティティの真上のブロックを壊す。
        """
        self.client.sendCall("digUp")

    def digDown(self):
        """
        エンティティの真下のブロックを壊す。
        """
        self.client.sendCall("digDown")

    def setItem(self, slot: int, block: str):
        """
        エンティティのインベントリにアイテムを設定する。

        Args:
            slot (int): 設定するアイテムのスロット番号。
            block (str): 設定するブロックの種類。
        """
        self.client.sendCall("setItem", [slot, block])

    def holdItem(self, slot: int):
        """
        指定されたスロットからアイテムをエンティティの手に持たせる。

        Args:
            slot (int): アイテムを持たせたいスロットの番号。
        """
        self.client.sendCall("grabItem", [slot])

    def say(self, message: str):
        """
        エンティティに指定されたメッセージをチャットとして送信させる。

        Args:
            message (str): エンティティがチャットで送信するメッセージの内容。
        """
        self.client.sendCall("sendChat", [message])

    def inspect(self, x: int, y: int, z: int) -> Block :
        """
        指定された座標のブロックを調べる。

        Args:
            x (int): 相対的なX座標。
            y (int): 相対的なY座標。
            z (int): 相対的なZ座標。
        Returns:
            Block: 調べたブロックの情報。    
        """
        self.client.sendCall("inspect", [x, y, z])
        block = Block(** json.loads(self.client.result))
        return block

    def getLocation(self) -> Location :
        """
        エンティティの現在位置を調べる。
        Returns:
            Location: 調べた位置情報。    
        """
        self.client.sendCall("getPosition")
        location = Location(** json.loads(self.client.result))
        return location
    
    def teleport(self, x: int, y: int, z: int) :
        """
        指定された座標に移動する。
        Args:
            x (int): 絶対的なX座標。
            y (int): 絶対的なY座標。
            z (int): 絶対的なZ座標。
        """
        self.client.sendCall("teleport", [x, y, z])

    def isBlocked(self) -> str :
        """
        エンティティの前方にブロックがあるかどうか調べる。
        Returns:
            bool: 調べた結果。    
        """
        self.client.sendCall("isBlockedFront")
        return str_to_bool(self.client.result)

    def isBlockedUp(self) -> str :
        """
        エンティティの真上にブロックがあるかどうか調べる。
        Returns:
            bool: 調べた結果。    
        """
        self.client.sendCall("isBlockedUp")
        return str_to_bool(self.client.result)

    def isBlockedDown(self) -> bool :
        """
        エンティティの真下にブロックがあるかどうか調べる。
        Returns:
            bool: 調べた結果。    
        """
        self.client.sendCall("isBlockedDown")
        return str_to_bool(self.client.result)
