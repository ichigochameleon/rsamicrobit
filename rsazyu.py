# ここにコードを書いてね :-)
import random
import microbit as mb
import radio
from rsautil import *
mode = 1 # 0クライアント・サーバ操作,1鍵交換,2通信
serveorcri = 1# 1はクライアント、2はサーバ
keypass = 0 # 0公開鍵送信,1共通鍵受信,2test,3go
radio.config(group=22)
radio.on()
r=0
while True:
    if mode == 1:
        if serveorcri == 2:
            if r ==0:
                mb.display.show("s1")
                r=1
            messageto = radio.receive()
            if messageto:
                if messageto == "hello":
                    if keypass == 0:
                        public_key, private_key = keytest()
                        radio.send(str(public_key))
                        keypass = 1
                        mb.display.show("s2")
                elif isinstance(int(messageto), (int, float)):
                    if keypass == 1:
                        wekey = rsa_decrypt(int(messageto), private_key)
                        test37 = encrypt(37, wekey)
                        radio.send(str(test37))
                        mb.display.show("s3")
                        keypass = 2
                elif keypass == 2:
                    if decrypt(int(messageto), wekey) == 38:
                        mode = 2
                        keypass = 3
                        mb.display.show("se")
