from hashlib import sha256, md5
from base64 import b64encode

# Steam To Dayz GUID
def steam_to_uid_dayz(steam_id):
    hashed = sha256()
    hashed.update(str(steam_id).encode('utf-8'))

    return b64encode(hashed.digest())


# Steam ID BE GUID
def steam_to_uid_be(steam_id):
    temp = ['BE']
    for _ in range(8):
        temp.append(chr(steam_id & 0xFF))
        steam_id = steam_id >> 8

    return md5(''.join(temp).encode("latin1")).hexdigest()