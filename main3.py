import random
import microbit as mb
import radio






        elif serveorcri == 1:
            if keypass == 0:
                radio.config(group=22)
                radio.on()
                radio.send("hello")
                mb.display.show("c1")
                messageto = radio.receive()
                if messageto:
                    try:
                        public_key = int(messageto)
                        keypass = 1
                        mb.display.show("c2")
                    except:
                        continue
            elif keypass == 1:
                wekey = generate_key(5)
                radio.send(str(rsa_encrypt(wekey, public_key)))
                keypass = 2
                mb.display.show("c3")
            elif keypass == 2:
                messageto = radio.receive()
                if messageto:
                    messageto = int(messageto)
                    if decrypt(messageto, wekey) == 37:
                        radio.send(str(encrypt(38, wekey)))
                        mode = 2
                        keypass = 3
                        mb.display.show("c4")
    elif mode == 2:
        if keypass == 3:
            if serveorcri == 2:
                messageto = radio.receive()
                if messageto:
                    messageto = int(messageto)
                    if isinstance(messageto, (int, float)):
                        mb.display.scroll(str(decrypt(messageto, wekey)))
            if serveorcri == 1:
                if mb.button_a.was_pressed():
                    sendme = random.randint(0, 41)
                    print(str(sendme))
                    radio.send(str(encrypt(sendme, wekey)))
