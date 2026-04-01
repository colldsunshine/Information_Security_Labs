def rsa_encrypt(m, e, n):
    return pow(m, e, n)

def rsa_decrypt(c, d, n):
    return pow(c, d, n)

p = 7
q = 17
e = 5
d = 77

n = p * q

messages = [7, 17, 73]

print(f"n = {n}")

for m in messages:
    c = rsa_encrypt(m, e, n)
    dec = rsa_decrypt(c, d, n)
    print(f"m = {m}, c = {c}, decrypted = {dec}")
