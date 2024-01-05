import json
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64

def encrypt_text(text, mode, key, initialization_vector=None):
    # JSON format
    json_string = json.dumps(text)
    
    # Ensure key is in bytes
    key = key.encode('utf-8')
    
    # Ensure IV is in bytes
    if initialization_vector is None:
        # Generate a random IV if not provided
        initialization_vector = ((get_random_bytes(AES.block_size)).hex()[:16]).encode('utf-8')
    else:
        # Ensure provided IV is in bytes
        initialization_vector = initialization_vector.encode('utf-8')

    # Perform encryption
    cipher = AES.new(key, mode) if mode == AES.MODE_ECB or mode == AES.MODE_CTR else AES.new(key, mode, initialization_vector)   
    ciphertext = cipher.encrypt(pad(json_string.encode(), AES.block_size))
    
    # Combine IV and ciphertext with delimiter "$"
    if mode != AES.MODE_ECB and mode != AES.MODE_CTR:
        encrypted_value = f"{base64.b64encode(initialization_vector).decode('utf-8')}${base64.b64encode(ciphertext).decode('utf-8')}"
        return encrypted_value, initialization_vector.decode('utf-8')
    else:
        encrypted_value = f"{base64.b64encode(ciphertext).decode('utf-8')}"
        return encrypted_value, None

def decrypt_text(encrypted_text, mode, key, initialization_vector=None):
    ciphertext = encrypted_text
    if mode != AES.MODE_ECB and mode != AES.MODE_CTR:
        # Split IV and ciphertext
        iv, ciphertext = encrypted_text.split('$')
        
        # Decode IV from base64
        iv = base64.b64decode(iv)
        
        # Use the provided initialization_vector if available
        if initialization_vector:
            iv = initialization_vector.encode('utf-8')
            
    ciphertext = base64.b64decode(ciphertext)
    
    # Ensure key and IV are in bytes
    key = key.encode('utf-8')
    
    # Perform decryption
    if mode in [AES.MODE_ECB, AES.MODE_CTR]:
        cipher = AES.new(key, mode)
    else:
        cipher = AES.new(key, mode, iv)
    decrypted_text = unpad(cipher.decrypt(ciphertext), AES.block_size)
    
    # Convert decrypted text to JSON object
    json_string = decrypted_text.decode('utf-8')
    decrypted_value = json.loads(json_string)
    
    return decrypted_value