import binascii
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding


def aes_256_cbc_decrypt(ivhex, encrypted_hex, hexSharedSecret="375b5cf795c4bbff0d2d4925622eda6afaf8666db4d2758ca24e972174b237a4"):
    iv = binascii.unhexlify(ivhex)

    key = binascii.unhexlify(hexSharedSecret)

    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    decryptor = cipher.decryptor()

    padder = padding.PKCS7(128).unpadder()  # 使用 PKCS7 填充方式

    # Convert encrypted hex string to bytes
    encrypted_bytes = binascii.unhexlify(encrypted_hex)

    decrypted_data = decryptor.update(encrypted_bytes) + decryptor.finalize()
    unpadded_data = padder.update(decrypted_data) + padder.finalize()
    print(unpadded_data.decode())
    return unpadded_data.decode()

if __name__ == '__main__':
    # hexSharedSecret = "375b5cf795c4bbff0d2d4925622eda6afaf8666db4d2758ca24e972174b237a4"
    # key = binascii.unhexlify(hexSharedSecret)
    # encrypted_hex = "10a61efae56f4612b5aa05c31ee3f55b7abbb8d4668b5e870ac47d5a88c5985c8f70d44ebbc5d8046b8ff4dc409237ea"
    # iv = binascii.unhexlify("d24e52704159d9acf361f784f564a8db")
    # result = aes_256_cbc_decrypt(iv, encrypted_hex, key)
    # result = result.decode()
    # print(result)  # Assuming the decrypted data is a UTF-8 string
    aes_256_cbc_decrypt("d24e52704159d9acf361f784f564a8db",
                        "10a61efae56f4612b5aa05c31ee3f55b7abbb8d4668b5e870ac47d5a88c5985c8f70d44ebbc5d8046b8ff4dc409237ea")
