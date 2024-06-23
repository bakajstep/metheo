import ujson


def api_key_required(handler):
    def check_api_key(request, *args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        API_KEYS = load_encrypted_api_keys()
        if api_key not in API_KEYS:
            return {'error': 'Unauthorized'}, 401
        return handler(request, *args, **kwargs)

    return check_api_key


def encrypt_decrypt(key, text):
    encrypted_decrypted = ''.join(chr(ord(c) ^ key) for c in text)
    return encrypted_decrypted


def save_encrypted_api_keys(api_keys, filename='config.enc', key=129):
    encrypted_keys = [encrypt_decrypt(key, k) for k in api_keys]
    with open(filename, 'w') as file:
        ujson.dump(encrypted_keys, file)


def load_encrypted_api_keys(filename='config.enc', key=129):
    try:
        with open(filename, 'r') as file:
            encrypted_keys = ujson.load(file)
            decrypted_keys = set(encrypt_decrypt(key, k) for k in encrypted_keys)
            return decrypted_keys
    except Exception as e:
        print("Error loading API keys:", e)
        return set()
