# ここにコードを書いてね :-)
import random
import microbit as mb
import radio

def generate_prime():
    while True:
        prime_candidate = random.choice([2,3,5,7,11,13,17,19,23,29,31])
        if is_prime(prime_candidate):
            return prime_candidate

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def extended_gcd(a, b):
    x, last_x = 0, 1
    y, last_y = 1, 0
    while b != 0:
        quotient = a // b
        a, b = b, a % b
        x, last_x = last_x - quotient * x, x
        y, last_y = last_y - quotient * y, y
    return last_x, last_y

def generate_rsa_keypair():
    p = generate_prime()
    q = generate_prime()
    while p == q:
        q = generate_prime()
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 3
    while gcd(e, phi) != 1:
        e += 2
    d, _ = extended_gcd(e, phi)
    d = d % phi
    return (e, n), (d, n)

def rsa_encrypt(plaintext, public_key):
    e, n = public_key
    return (plaintext ** e) % n

def rsa_decrypt(ciphertext, private_key):
    d, n = private_key
    return (ciphertext ** d) % n

def generate_key(bit_length):
    return random.getrandbits(bit_length)

def encrypt(message, key):
    return message ^ key

def decrypt(encrypted_message, key):
    return encrypted_message ^ key
def inter(msg):
    i = msg.find(',')
    return int(msg[:i]),int(msg[i+1:])
mode = 1#1鍵交換,2通信,3通信テスト
keypass = 0 # 0公開鍵送信,1共通鍵受信,2test,3go
radio.config(group=22)
radio.on()
r=0
wekey=0
sku=2#0,サーバー1,クライアント2,選択
sentaku=0#0サーバー1クライアント
zumi=0#テスト37送信未1送信終
sugoi=0
sendme=0
while True:
    if sku==2:
      sku=1
    if sku==1:#クライアント
        if keypass == 0:
            #mb.display.show("c1")
            messageto = radio.receive()
            if messageto:
                #mb.display.scroll(messageto)
                a ,b = inter(messageto)
                public_key = a,b
                keypass = 1
                #mb.display.show("c2")
                del messageto
        elif keypass == 1:
            wekey = generate_key(5)
            mb.sleep(865)
            radio.send(str(rsa_encrypt(wekey, public_key)))
            keypass = 3
            mode=2
            #mb.display.show("c3")
            mb.display.clear()
        elif mode == 2:
            if keypass == 3:
                if mb.button_a.was_pressed() and mb.button_a.was_pressed():
                    mb.display.scroll(sendme)
                    print(str(sendme))
                    radio.send(str(encrypt(sendme, wekey)))
                    mb.sleep(200)
                elif mb.button_a.was_pressed():
                    sendme=sendme-1
                elif mb.button_b.was_pressed():
                    sendme=sendme+1
                if messageto:
                    messageto = int(messageto)
                    if isinstance(messageto, (int, float)):
                        mb.display.scroll(str(decrypt(messageto, wekey)))
    if sku==0:#サーバー
        if mode == 1:
            if r ==0:
                r=1
            if keypass == 0:
                str_public_key = str(public_key)
                radio.send(str_public_key[1:-1])
                mb.sleep(865)
            messageto = radio.receive()
            if messageto:
                if isinstance(int(messageto), int):
                    if keypass==0:
                        wekey = rsa_decrypt(int(messageto), private_key)
                        del messageto
                        mode=2
                        keypass=3
                        mb.display.clear()
        elif mode == 2:
            if keypass == 3:
                if mb.button_a.was_pressed() and mb.button_a.was_pressed():
                    mb.display.scroll(sendme)
                    print(str(sendme))
                    radio.send(str(encrypt(sendme, wekey)))
                    mb.sleep(200)
                elif mb.button_a.was_pressed():
                    sendme=sendme-1
                elif mb.button_b.was_pressed():
                    sendme=sendme+1
                messageto = radio.receive()
                if messageto:
                    messageto = int(messageto)
                    if isinstance(messageto, (int, float)):
                        mb.display.scroll(str(decrypt(messageto, wekey)))
