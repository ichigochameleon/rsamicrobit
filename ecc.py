class Point:
    def __init__(self, x, y, curve):
        self.x = x
        self.y = y
        self.curve = curve

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.curve == other.curve

    def add(self, other):
        if self.curve != other.curve:
            raise ValueError("Points are not on the same curve")
        if self == Point(None, None, self.curve):
            return other
        if other == Point(None, None, self.curve):
            return self
        if self.x == other.x and self.y != other.y:
            return Point(None, None, self.curve)  # Point at infinity
        if self == other:
            s = ((3 * self.x**2 + self.curve.a) * self.inverse_mod(2 * self.y, self.curve.p)) % self.curve.p
        else:
            s = ((other.y - self.y) * self.inverse_mod(other.x - self.x, self.curve.p)) % self.curve.p
        x3 = (s**2 - self.x - other.x) % self.curve.p
        y3 = (s * (self.x - x3) - self.y) % self.curve.p
        return Point(x3, y3, self.curve)

    def multiply(self, n):
        result = Point(None, None, self.curve)
        for _ in range(n):
            result = result.add(self)
        return result

    def inverse_mod(self, a, m):
        if a < 0 or m <= a:
            a = a % m
        c, d = a, m
        uc, vc, ud, vd = 1, 0, 0, 1
        while c != 0:
            q, c, d = divmod(d, c) + (c,)
            uc, vc, ud, vd = ud - q*uc, vd - q*vc, uc, vc
        return ud % m

class EllipticCurve:
    def __init__(self, a, b, p):
        self.a = a
        self.b = b
        self.p = p

    def is_on_curve(self, x, y):
        return (y**2 - x**3 - self.a * x - self.b) % self.p == 0

def encrypt(message, public_key, base_point):
    k = 3  # Random value
    c1 = base_point.multiply(k)
    c2 = Point(message, message, public_key.curve).add(public_key.multiply(k))
    return c1, c2

def decrypt(c1, c2, private_key):
    return c2.add(c1.multiply(private_key.curve.p - 1 - private_key.x))

# Example parameters for a simple elliptic curve y^2 = x^3 + ax + b (mod p)
a = 0
b = 7
p = 17

curve = EllipticCurve(a, b, p)
base_point = Point(5, 1, curve)  # Base point (G) on the curve
private_key = Point(9, None, curve)  # Private key
public_key = Point(9, 12, curve)  # Public key (Q = private_key * G)

# Encryption
message = 7  # Message to encrypt
c1, c2 = encrypt(message, public_key, base_point)

# Decryption
decrypted_message = decrypt(c1, c2, private_key)

print("Decrypted message:", decrypted_message.x)  # Should output the original message
