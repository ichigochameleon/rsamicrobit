import random

# 素数p, 楕円曲線係数a, b, 基準点Gの設定
p = 23
a = 1
b = 1
G = (1, 1)

# プライベートキーの生成
private_key = random.randint(1, p-1)

# パブリックキーの計算
def point_add(p1, p2):
    lam = ((p2[1] - p1[1]) * pow(p2[0] - p1[0], -1, p)) % p
    x3 = (lam**2 - p1[0] - p2[0]) % p
    y3 = (lam * (p1[0] - x3) - p1[1]) % p
    return (x3, y3)

def point_multiply(k, P):
    Q = (0, 0)
    for i in range(k.bit_length()):
        if k & (1 << i):
            Q = point_add(Q, P)
        P = point_add(P, P)
    return Q

public_key = point_multiply(private_key, G)

# メッセージの暗号化と復号化
def encrypt(number, public_key):
    k = random.randint(1, p-1)
    C1 = point_multiply(k, G)
    C2 = point_add(point_multiply(k, public_key), (number, 0))
    return (C1, C2)

def decrypt(C, private_key):
    C1, C2 = C
    M = point_add(C2, (-1) * point_multiply(private_key, C1))[0]
    return M

# メッセージの暗号化と復号化の例
number = 5
print("元の数字:", number)

encrypted_number = encrypt(number, public_key)
print("暗号化された数字:", encrypted_number)

decrypted_number = decrypt(encrypted_number, private_key)
print("復号化された数字:", decrypted_number)
