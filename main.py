import random
def generate_prime():
    while True:
        prime_candidate = random.choice([2,3,5,7,11,13,17,19,23,29,31,37,41,
43,47,53,59,61])#this 6bit.5bit is 2,3,5,7,11,13,17,19,23,29,31
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
def main():
    test_values = list(range(0, 41))
    while True:
        public_key, private_key = generate_rsa_keypair()
        failed = False
        for test_value in test_values:
            encrypted_message = rsa_encrypt(test_value, public_key)
            decrypted_message_numeric = rsa_decrypt(encrypted_message, private_key)
            if decrypted_message_numeric != test_value:
                failed = True
                break
        if failed:
            continue
        message_numeric = 40
        encrypted_message = rsa_encrypt(message_numeric, public_key)
        decrypted_message_numeric = rsa_decrypt(encrypted_message, private_key)
        print(encrypted_message)
        print(decrypted_message_numeric)
        break
main()

