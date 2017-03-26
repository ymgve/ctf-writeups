#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from argparse import ArgumentParser
from binascii import a2b_hex
from struct import pack, unpack
from socket import socket
from secret import KEY_HMAC, KEY_ENCRYPT
from Crypto.Cipher import AES
from Crypto.Hash import SHA256, HMAC
from base64 import b64decode, b64encode


class CryptoClient:
    def __init__(self, host, port, timestamp, data):
        self.__timestamp = timestamp
        self.__KEY_HMAC = a2b_hex(KEY_HMAC)
        self.__KEY_ENCRYPT = a2b_hex(KEY_ENCRYPT)
        sock = socket()
        sock.connect((host, port))
        try:
            sock.send(b64encode(self.__encrypt(data)))
            sock.send(b'\x0A')
            self.check_response(b64decode(sock.recv(1024)))
        finally:
            sock.close()

    def check_response(self, msg):
        if len(msg) != 35:
            print('Message from server has invalid length !')
        else:
            code = msg[0]
            if code < 0xA0 or code > 0xA3:
                print('Message from server has invalid code !')
            else:
                r_timestamp = unpack('>q', msg[1:9])
                r_ciphertext = msg[9:-10]
                r_tag = msg[-10:]
                if r_timestamp[0] < self.__timestamp:
                    print('Message from server has invalid timestamp !')
                else:
                    iv = b'\x00' * 8 + pack('>q', r_timestamp[0])
                    r_data = AES.new(self.__KEY_ENCRYPT, AES.MODE_CBC, iv).decrypt(r_ciphertext)
                    if HMAC.new(self.__KEY_HMAC, r_data, SHA256).digest()[:10] != r_tag:
                        print('Message from server has invalid MAC !')
                    else:
                        if code == 0xA0:
                            print('OK !')
                        elif code == 0xA1:
                            print('Wrong timestamp !')
                        elif code == 0xA2:
                            print('Padding error !')
                        elif code == 0xA3:
                            print('MAC error !')
                        else:
                            print('Unknown error !')

    def __encrypt(self, data):
        iv = b'\x00' * 8 + pack('>q', self.__timestamp)
        to_pad = 16 - (len(data) % 16)
        plaintext = data.encode() + pack('B', to_pad) * to_pad
        ciphertext = AES.new(self.__KEY_ENCRYPT, AES.MODE_CBC, iv).encrypt(plaintext)
        tag = HMAC.new(self.__KEY_HMAC, plaintext, SHA256).digest()[:10]
        return b'\x00' + pack('>q', self.__timestamp) + ciphertext + tag

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('-host', metavar='<HOST>', type=str, default='127.0.0.1', help='The oracle ip address')
    parser.add_argument('-port', metavar='<PORT>', type=int, default=7000, help='The port number of the oracle')
    parser.add_argument('timestamp', metavar='<timestamp>', type=int, help='The timestamp used to encrypt data')
    parser.add_argument('data', metavar='data', type=str, help='The data to encrypt and to send to the oracle.')
    args = parser.parse_args()
    CryptoClient(args.host, args.port, args.timestamp, args.data)
