from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64

def decrypt_aes_string(encrypted_string, key):
    # Convert the key to 32 bytes (AES-256 requires a 32-byte key)
    key = key.encode('utf-8')
    key = key.ljust(32, b'\0')  # Pad the key to 32 bytes if shorter

    # Decode the base64-encoded string (assuming it was base64 encoded)
    encrypted_data = base64.b64decode(encrypted_string)

    # Extract IV (first 16 bytes) and ciphertext (the rest)
    iv = encrypted_data[:16]
    ciphertext = encrypted_data[16:]

    # Initialize AES decryption
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Decrypt and unpad the data
    decrypted_data = unpad(cipher.decrypt(ciphertext), AES.block_size)

    # Convert decrypted bytes back to a string
    return decrypted_data.decode('utf-8')

# Example Usage
encrypted_string = "ReplaceThisWithYourBase64EncodedEncryptedString"
password = "your_password_here"

try:
    decrypted_text = decrypt_aes_string(encrypted_string, password)
    print("Decrypted Text:", decrypted_text)
except Exception as e:
    print("Decryption failed:", e)
