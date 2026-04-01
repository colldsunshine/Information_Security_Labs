def hashvar7(message):
    """Хэш-функция: блоки по 16 бит + XOR + циклический сдвиг"""
    if not message:
        return 0

    bits = ''.join(format(ord(c), '08b') for c in message)

    while len(bits) % 16 != 0:
        bits += '0'

    h = 0

    for i in range(0, len(bits), 16):
        block = int(bits[i:i+16], 2)
        h ^= block
        h = ((h >> 1) | ((h & 1) << 15)) & 0xFFFF

    return h


def generatesignature(message, p, q, a, x, k):
    Hm = hashvar7(message)
    h = Hm % q
    if h == 0:
        h = 1

    r = pow(a, k, p)
    r1 = r % q

    s = (x * r1 + k * h) % q

    return r1, s


def verifysignature(message, r1, s, p, q, a, y):
    if not (0 < r1 < q and 0 < s < q):
        return False

    Hm = hashvar7(message)
    h = Hm % q
    if h == 0:
        h = 1

    v = pow(h, q - 2, q)
    z1 = (s * v) % q
    z2 = ((q - r1) * v) % q

    u = (pow(a, z1, p) * pow(y, z2, p)) % p
    u = u % q

    return u == r1


# Параметры
p, q, a = 23, 11, 2
x = 7
y = pow(a, x, p)
k = 3

message = "AB"

print("Параметры:", p, q, a, x, y)

r1, s = generatesignature(message, p, q, a, x, k)

print("Сообщение:", message)
print("Хэш:", hashvar7(message))
print("Подпись:", r1, s)

print("Проверка:", verifysignature(message, r1, s, p, q, a, y))

print("Проверка измененной подписи:",
      verifysignature(message, r1, s+1, p, q, a, y))
