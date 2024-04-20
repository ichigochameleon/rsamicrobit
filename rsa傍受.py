import random
import microbit as mb
import radio
radio.config(group=22)
radio.on()
while True:
    messageto = radio.receive()
    if messageto:
            mb.display.scroll(messageto)

