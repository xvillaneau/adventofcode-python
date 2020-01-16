from hashlib import md5


def get_pass(word: str):
    index = 0
    password = []
    while len(password) < 8:
        indexed = bytes(f'{word}{index}', 'utf-8')
        hex_hash = md5(indexed).hexdigest()
        if hex_hash[:5] == '00000':
            password.append(hex_hash[5])
            print(''.join(password))
        index += 1
    return ''.join(password)


def get_pass_2(word: str):
    index = 0
    password = ['_'] * 8
    while '_' in password:
        indexed = bytes(f'{word}{index}', 'utf-8')
        hex_hash: str = md5(indexed).hexdigest()
        if hex_hash[:5] == '00000':
            pos = int(hex_hash[5], 16)
            if 0 <= pos < 8 and password[pos] == '_':
                password[pos] = hex_hash[6]
                print(''.join(password))
        index += 1
    return ''.join(password)


def main(data: str):
    yield get_pass(data)
    yield get_pass_2(data)
