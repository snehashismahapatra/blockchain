import secrets
import hashlib
from ecdsa import SigningKey,SECP256k1
import binascii
import codecs

bits = secrets.randbits(256)
#while bits not in range(1,115792089237316195423570985008687907852837564279074904382605163141518161494337):
#    bits = secrets.randbits(256)
bits_hex = hex(bits)
private_key = bits_hex[2:]
sk = SigningKey.generate(curve=SECP256k1)
print(private_key)
signature = sk.sign(private_key.encode("utf-8"))
eliptic_public_key=binascii.b2a_hex(signature).decode("ascii")
public_key="0x04"+eliptic_public_key
public_key_bytes = codecs.decode(public_key,"hex")
hash1_public_key=hashlib.sha256(public_key_bytes).digest()
print(hash1_public_key)
