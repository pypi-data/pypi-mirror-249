if __name__ == "__main__":
    client = WebSocketClient("ws://localhost:25570/ws")
    client.run_forever()
    time.sleep(1)  # Give time for connection to establish
    client.send(json.dumps({
        "type": "connect2",
        "data": {
            "player": "masafumi_t",
            "entity": "test",
        }
    }))
    time.sleep(1)  # Keep application open to receive message
    client.send(json.dumps({
        "type": "call",
        "data": {
            "name": "forward"
        }
    }))


    client.close()