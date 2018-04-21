from ws4py.client.threadedclient import WebSocketClient

class DummyClient(WebSocketClient):
    def opened(self):
        self.send("www.baidu.com")

    def closed(self, code, reason=None):
        print("Closed down", code, reason)

    def received_message(self, message):
        print(message)


if __name__ == '__main__':
    try:
        ws = DummyClient('ws://124.232.141.2:80/websocket', protocols=['chat'])
        ws.connect()
        ws.run_forever()

    except KeyboardInterrupt:
        ws.close()



# ylog.hiido.com

# act: /event
# mid=C7EC370DD7600001F4C11580B55012AE&bve=chrome/65.0.3325.181&lla=zh-CN&os=Windows7&sco=24&sre=1440.900&fve=29.00&jav=0&coo=1&domain=www.huya.com&fla=Y&sdk_ver=js-ya.huya-1.0&pageType=root&yyuid=2232479408&pro=huya_web&pas=2232684128yy&dty=live&session_id=C7F3C8F4BD400001765BC1A06C29D400&sguid=0e74abbb3bffb65a032cc646c7468f6b&eid=click/zhibo/sendwords&eid_desc=点击/直播间/发言按钮&ayyuid=2234554035&gameId=3203&dur=492180&furl=http://www.huya.com/&curl=http%3A%2F%2Fwww.huya.com%2F15159082:
# __yafm: i
# ati:


# Request URL: http://ylog.hiido.com/j.gif?act=/event&mid%3DC7EC370DD7600001F4C11580B55012AE%26bve%3Dchrome%2F65.0.3325.181%26lla%3Dzh-CN%26os%3DWindows7%26sco%3D24%26sre%3D1440.900%26fve%3D29.00%26jav%3D0%26coo%3D1%26domain%3Dwww.huya.com%26fla%3DY%26sdk_ver%3Djs-ya.huya-1.0%26pageType%3Droot%26yyuid%3D2232479408%26pro%3Dhuya_web%26pas%3D2232684128yy%26dty%3Dlive%26session_id%3DC7F3C8F4BD400001765BC1A06C29D400%26sguid%3D0e74abbb3bffb65a032cc646c7468f6b%26eid%3Dclick%2Fzhibo%2Fsendwords%26eid_desc%3D%E7%82%B9%E5%87%BB%2F%E7%9B%B4%E6%92%AD%E9%97%B4%2F%E5%8F%91%E8%A8%80%E6%8C%89%E9%92%AE%26ayyuid%3D2234554035%26gameId%3D3203%26dur%3D492180%26furl%3Dhttp%3A%2F%2Fwww.huya.com%2F%26curl%3Dhttp%253A%252F%252Fwww.huya.com%252F15159082&__yafm=i&ati=
# Request Method: GET
# Status Code: 200 OK
# Remote Address: 124.232.141.2:80
# Referrer Policy: no-referrer-when-downgrade