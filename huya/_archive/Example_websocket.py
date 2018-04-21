# import base64
# import hashlib
# import socket
#
# if __name__ == "__main__":
#     serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     host = ("125.88.153.35", 80)
#     serverSocket.bind(host)
#     serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#     serverSocket.listen(5)
#     print("server running")
#     while True:
#         print("getting connection")
#         clientSocket, addressInfo = serverSocket.accept()
#         print("get connected")
#         receivedData = str(clientSocket.recv(2048))
#         # print(receivedData)
#         entities = receivedData.split("\\r\\n")
#         Sec_WebSocket_Key = entities[11].split(":")[1].strip() + '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
#         print("key ", Sec_WebSocket_Key)
#         response_key = base64.b64encode(hashlib.sha1(bytes(Sec_WebSocket_Key, encoding="utf8")).digest())
#         response_key_str = str(response_key)
#         response_key_str = response_key_str[2:30]
#         # print(response_key_str)
#         response_key_entity = "Sec-WebSocket-Accept: " + response_key_str +"\r\n"
#         clientSocket.send(bytes("HTTP/1.1 101 Web Socket Protocol Handshake\r\n", encoding="utf8"))
#         clientSocket.send(bytes("Upgrade: websocket\r\n", encoding="utf8"))
#         clientSocket.send(bytes(response_key_entity, encoding="utf8"))
#         clientSocket.send(bytes("Connection: Upgrade\r\n\r\n", encoding="utf8"))
#         print("send the hand shake data")

# import asyncio
# import websockets
#
# async def hello(uri):
#     async with websockets.connect(uri) as websocket:
#         await websocket.send("Hello world!")
#
# asyncio.get_event_loop().run_until_complete(
#     hello('ws://125.88.153.35:80'))
import websocket
# from websocket import create_connection
# ws = create_connection("ws://125.88.153.35:80")
#
# print("Sending 'Hello, World'...")
# ws.send("Hello, World")
# print("Sent")
# print("Receiving...")
# result =  ws.recv()
# print(type(result))
# print("Received '%s'" % result)
# ws.close()


# import asyncio
import websockets

# async def hello():
#     async with websockets.connect('ws://125.88.153.35:80') as websocket:
#         name = input("What's your name? ")
#         await websocket.send(name)
#         print("> {}".format(name))
#         greeting = await websocket.recv()
#         print("< {}".format(greeting))
#
# asyncio.get_event_loop().run_until_complete(hello())



# import asyncio
# import websockets
#
# async def echo(websocket, path):
#     async for message in websocket:
#         await websocket.send(message)
#
# asyncio.get_event_loop().run_until_complete(
#     websockets.serve(echo, 'ws://125.88.153.35', 80))
# asyncio.get_event_loop().run_forever()

import websocket
try:
    import thread
except ImportError:
    import _thread as thread
import time

def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def run(*args):
        for i in range(3):
            time.sleep(1)
            ws.send("Hello %d" % i)
        time.sleep(1)
        ws.close()
        print("thread terminating...")
    thread.start_new_thread(run, ())


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://125.88.153.35:80",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    # ws.on_open = on_open
    ws.run_forever()