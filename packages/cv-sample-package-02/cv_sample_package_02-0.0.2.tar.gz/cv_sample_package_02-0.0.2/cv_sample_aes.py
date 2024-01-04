from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

# Random Key
SECRET_KEY = '464f6cc46e7e8bf35195a62165969453'

def base64_decode(data):
    str_to_bytes = data.encode('utf-8')
    decode =  base64.b64decode(str_to_bytes)
    bytes_to_str = decode
    return bytes_to_str

def base64_encode(data):
    if isinstance(data, str):
        data = data.encode('utf-8')
    else:
        data = data
    str_to_bytes = data
    encode = base64.b64encode(str_to_bytes)
    bytes_to_str = encode.decode('utf-8')
    return bytes_to_str

def encrypt_text(text, key = SECRET_KEY):
    key= key.encode('utf-8')
    # iv = get_random_bytes(AES.block_size)  # Generate a random IV
    iv = "9aa9bf96df4cfcwq".encode('utf-8')
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(text.encode(), AES.block_size))
    encrypted_value = base64_encode(ciphertext)
    return encrypted_value

def decrypt_text(encrypted_text, key = SECRET_KEY):
    key= key.encode('utf-8')
    decoded = base64_decode(encrypted_text)
    iv = "9aa9bf96df4cfcwq".encode('utf-8')
    encrypted = decoded[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(decoded)
    decrypted_value = unpad(decrypted, AES.block_size).decode()
    return decrypted_value