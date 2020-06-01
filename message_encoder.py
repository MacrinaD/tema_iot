"""
functii ajutatoare pentru reprezentarea mesajelor intre procese
sursa: https://www.eadan.net/blog/ipc-with-named-pipes/
"""
import struct


def encode_msg_size(size: int) -> bytes:
    return struct.pack('<I', size)


def create_msg(content: bytes) -> bytes:
    dim = len(content)
    return encode_msg_size(dim) + content
