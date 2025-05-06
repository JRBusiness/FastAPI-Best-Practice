import pgpy
from pgpy.constants import (
    PubKeyAlgorithm,
    KeyFlags,
    HashAlgorithm,
    SymmetricKeyAlgorithm,
    CompressionAlgorithm,
)

from config.settings import Settings


class Encryption:
    @staticmethod
    def get_key(plain=False):
        try:
            key = pgpy.PGPKey.from_file(Settings.ASC_PATH)[0]
            return str(key) if plain else key
        except Exception:
            return None

    @staticmethod
    def generate_seed_certificates(seed: str):
        key = pgpy.PGPKey.new(PubKeyAlgorithm.RSAEncryptOrSign, 4096)
        uid = pgpy.PGPUID.new(seed)
        key.add_uid(
            uid,
            usage={
                KeyFlags.Sign,
                KeyFlags.EncryptCommunications,
                KeyFlags.EncryptStorage,
            },
            hashes=[HashAlgorithm.SHA512],
            ciphers=[PubKeyAlgorithm.RSAEncryptOrSign, SymmetricKeyAlgorithm.AES256],
            compression=[
                CompressionAlgorithm.ZLIB,
                CompressionAlgorithm.BZ2,
                CompressionAlgorithm.ZIP,
                CompressionAlgorithm.Uncompressed,
            ],
        )
        with open(Settings.ASC_PATH, "wb") as f:
            f.write(bytes(key))

    @staticmethod
    def encrypt(data) -> str:
        k = Encryption.get_key()
        m = k.pubkey.encrypt(
            pgpy.PGPMessage.new(data), cipher=SymmetricKeyAlgorithm.AES256
        )
        return bytes(m).hex()

    @staticmethod
    def decrypt(data) -> bytes:
        data = bytes.fromhex(data)
        k = Encryption.get_key()
        m = k.decrypt(pgpy.PGPMessage.from_blob(data))
        return (
            bytes(m._message.contents)
            if isinstance(m._message.contents, bytearray)
            else m._message.contents
        )
