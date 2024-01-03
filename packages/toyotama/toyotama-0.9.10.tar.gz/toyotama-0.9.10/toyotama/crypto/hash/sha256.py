import hashlib
import random
import struct

from toyotama.util.log import get_logger

logger = get_logger(__name__)


class SHA256(object):
    BLOCK_SIZE: int = 64
    MOD: int = 1 << 32
    # fmt: off
    ROUND_CONSTANTS: list[int] = [0x428A2F98, 0x71374491, 0xB5C0FBCF, 0xE9B5DBA5, 0x3956C25B, 0x59F111F1, 0x923F82A4, 0xAB1C5ED5, 0xD807AA98, 0x12835B01, 0x243185BE, 0x550C7DC3, 0x72BE5D74, 0x80DEB1FE, 0x9BDC06A7, 0xC19BF174, 0xE49B69C1, 0xEFBE4786, 0x0FC19DC6, 0x240CA1CC, 0x2DE92C6F, 0x4A7484AA, 0x5CB0A9DC, 0x76F988DA, 0x983E5152, 0xA831C66D, 0xB00327C8, 0xBF597FC7, 0xC6E00BF3, 0xD5A79147, 0x06CA6351, 0x14292967, 0x27B70A85, 0x2E1B2138, 0x4D2C6DFC, 0x53380D13, 0x650A7354, 0x766A0ABB, 0x81C2C92E, 0x92722C85, 0xA2BFE8A1, 0xA81A664B, 0xC24B8B70, 0xC76C51A3, 0xD192E819, 0xD6990624, 0xF40E3585, 0x106AA070, 0x19A4C116, 0x1E376C08, 0x2748774C, 0x34B0BCB5, 0x391C0CB3, 0x4ED8AA4A, 0x5B9CCA4F, 0x682E6FF3, 0x748F82EE, 0x78A5636F, 0x84C87814, 0x8CC70208, 0x90BEFFFA, 0xA4506CEB, 0xBEF9A3F7, 0xC67178F2]
    INITIAL_VECTOR: list[int] = [0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A, 0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19]
    # fmt: on

    def __init__(self, data: bytes, iv: list[int] | None = None, input_bytes: int = 0):
        self.data: bytes = data
        self.hashes: list[int] = iv or self.INITIAL_VECTOR

        self.preprocessed_data: bytes = self._pad_data(self.data, input_bytes)
        self._compute_hash()

    def _pad_data(self, data: bytes, input_bytes: int) -> bytes:
        pad = b"\x80" + bytes(63 - (len(data) + input_bytes + 8) % self.BLOCK_SIZE)
        length = struct.pack(">Q", ((len(data) + input_bytes) * 8))  # 64bit-big
        return data + pad + length

    def _compute_hash(self) -> None:
        self.blocks = [self.preprocessed_data[i : i + self.BLOCK_SIZE] for i in range(0, len(self.preprocessed_data), self.BLOCK_SIZE)]

        for block in self.blocks:
            words = list(struct.unpack(">16L", block))
            words += [0] * 48

            a, b, c, d, e, f, g, h = self.hashes

            for i in range(64):
                if i >= 16:
                    s0 = self.ror(words[i - 15], 7) ^ self.ror(words[i - 15], 18) ^ (words[i - 15] >> 3)
                    s1 = self.ror(words[i - 2], 17) ^ self.ror(words[i - 2], 19) ^ (words[i - 2] >> 10)

                    words[i] = (words[i - 16] + s0 + words[i - 7] + s1) % self.MOD

                s1 = self.ror(e, 6) ^ self.ror(e, 11) ^ self.ror(e, 25)
                ch = (e & f) ^ (~e % self.MOD) & g
                temp1 = (h + s1 + ch + self.ROUND_CONSTANTS[i] + words[i]) % self.MOD
                s0 = self.ror(a, 2) ^ self.ror(a, 13) ^ self.ror(a, 22)
                maj = (a & b) ^ (b & c) ^ (c & a)
                temp2 = (s0 + maj) % self.MOD

                a, b, c, d, e, f, g, h = (temp1 + temp2) % self.MOD, a, b, c, (d + temp1) % self.MOD, e, f, g
            mutated_hash_values = [a, b, c, d, e, f, g, h]
            self.hashes = [(x + mutated_hash_values[i]) % self.MOD for i, x in enumerate(self.hashes)]

        self.hash = b"".join(x.to_bytes(4, "big") for x in self.hashes)

    def ror(self, x: int, n: int) -> int:
        return (x << (32 - n)) | (x >> n) % self.MOD

    def digest(self) -> bytes:
        return self.hash

    def hexdigest(self) -> str:
        return self.hash.hex()


if __name__ == "__main__":
    x = random.randbytes(100)
    h1 = SHA256(x).digest()
    h2 = hashlib.sha256(x).digest()

    assert h1 == h2

    logger.info("%s (length=%d)", h1, len(h1))
    logger.info("%s (length=%d)", h2, len(h2))
