import random
import microbit as mb
import radio

def generate_prime():
    while True:
        prime_candidate = random.choice([2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31])
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
    parts = msg.split()
    return int(parts[0]), int(parts[1])

mode = 1
keypass = 0
radio.config(group=22)
radio.on()
r = 0
wekey = 0

while True:
    if keypass == 0:
        messageto = radio.receive()
        if messageto:
            a, b = inter(messageto)
            public_key = a, b
            keypass = 1
            del messageto
    elif keypass == 1:
        wekey = generate_key(5)
        mb.sleep(865)
        radio.send(str(rsa_encrypt(wekey, public_key)))
        keypass = 3
        mode = 2
        mb.display.clear()
    elif mode == 2:
        if keypass == 3:
            if mb.button_a.was_pressed():
                sendme = random.randint(0, 41)
                mb.display.scroll(sendme)
                radio.send(str(encrypt(sendme, wekey)))
            messageto = radio.receive()
            if messageto and messageto.isdigit():
                messageto = int(messageto)
                mb.display.scroll(str(decrypt(messageto, wekey)))
