#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from sys import stdin, stdout
from signal import alarm
from binascii import a2b_hex
from struct import pack, unpack
from secret import KEY_HMAC, KEY_ENCRYPT
from Crypto.Cipher import AES
from Crypto.Hash import SHA256, HMAC
from base64 import b64decode, b64encode


class CryptOracle(object):
    def __init__(self, ):
        self.__socket = ''
        self.__KEY_HMAC = a2b_hex(KEY_HMAC)
        self.__KEY_ENCRYPT = a2b_hex(KEY_ENCRYPT)
        self.__timestamp = -1
        self.__run()

    def __generate_response(self, error_type=None):
        self.__timestamp += 1
        tsp = pack('>q', self.__timestamp)
        plaintext = b'\x00' * 16
        iv = b'\x00' * 8 + tsp
        ciphertext = AES.new(self.__KEY_ENCRYPT, AES.MODE_CBC, iv).encrypt(plaintext)
        tag = HMAC.new(self.__KEY_HMAC, plaintext, SHA256).digest()[:10]
        if error_type == 'MAC':
            return b'\xA3' + tsp + ciphertext + tag
        elif error_type == 'PAD':
            return b'\xA2' + tsp + ciphertext + tag
        elif error_type == 'TSP':
            return b'\xA1' + tsp + ciphertext + tag
        else:
            return b'\xA0' + tsp + ciphertext + tag

    def __decrypt(self, data):
        if (len(data) - 19) % 16 != 0:
            return None
        else:
            if data[0] != 0:
                return None
            r_timestamp = data[1:9]
            r_ciphertext = data[9:-10]
            r_tag = data[-10:]
            tsp = unpack('>q', r_timestamp)
            if tsp[0] > self.__timestamp and tsp[0] > self.__timestamp:
                self.__timestamp = tsp[0]
            else:
                return self.__generate_response(error_type='TSP')
            iv = b'\x00' * 8 + r_timestamp
            r_plaintext = AES.new(self.__KEY_ENCRYPT, AES.MODE_CBC, iv).decrypt(r_ciphertext)
            count = r_plaintext[-1]
            if count == 0 or count > 16:
                return self.__generate_response(error_type='PAD')
            else:
                for i in range(1, count + 1):
                    if r_plaintext[-i] != count:
                        return self.__generate_response(error_type='PAD')
                if HMAC.new(self.__KEY_HMAC, r_plaintext, SHA256).digest()[:10] != r_tag:
                    return self.__generate_response(error_type='MAC')
                else:
                    return self.__generate_response()

    def __run(self):
        while True:
            msg = b64decode(stdin.buffer.readline())
            msg = self.__decrypt(msg)
            if msg is None:
                break
            else:
                stdout.buffer.write(b64encode(msg))
                stdout.buffer.write(b'\x0A')
                stdout.flush()
        stdout.buffer.write(b64encode(bytes('Something went wrong... maybe not !', 'utf-8')))
        stdout.buffer.write(b'\x0A')
        stdout.flush()

if __name__ == '__main__':
    CryptOracle()
