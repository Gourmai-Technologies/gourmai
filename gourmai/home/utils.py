from cryptography.fernet import Fernet

fernet_key = b'q0HBjD4zYAYemNmtM6VLSqu8y5CLvZIHou_JI_Z5M44='


# Encrypt an ID
def hash_id(id_to_hash):
    cipher_suite = Fernet(fernet_key)
    encrypted_id = cipher_suite.encrypt(str(id_to_hash).encode())

    encrypted_id_str = encrypted_id.decode('utf-8')

    encrypted_id_link = f"https://gourmai.co.uk/load-recipe/{encrypted_id_str}"
    return encrypted_id_link

# Decrypt an ID
def unhash_id(encrypted_id):
    cipher_suite = Fernet(fernet_key)
    decrypted_id = cipher_suite.decrypt(encrypted_id).decode()
    return decrypted_id


#key = unhash_id('gAAAAABl9woadtnIYllI89lsJS4QBPSxmEQShvtbt1dBKPOCdFkbgjxVvEbAsU_LXfxe_OVpZXSZJtiINkgzN28y75ufpBuIKw==')


