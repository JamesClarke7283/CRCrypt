import unittest
from src.core import CRCrypt

class TestEncrypt(unittest.TestCase):
    def setUp(self):
        self.key = "test_key_123"
        self.crcrypt = CRCrypt(self.key)

    def test_encrypt_decrypt(self):
        original_message = "Hello, World! This is a test message."
        encrypted = self.crcrypt.encrypt(original_message)
        decrypted = self.crcrypt.decrypt(encrypted)
        self.assertEqual(original_message, decrypted)

    def test_different_keys(self):
        message = "Secret message"
        encrypted1 = CRCrypt("key1").encrypt(message)
        encrypted2 = CRCrypt("key2").encrypt(message)
        self.assertNotEqual(encrypted1, encrypted2)
        
        # Ensure that each key can decrypt its own message
        decrypted1 = CRCrypt("key1").decrypt(encrypted1)
        decrypted2 = CRCrypt("key2").decrypt(encrypted2)
        
        self.assertEqual(message, decrypted1)
        self.assertEqual(message, decrypted2)

    def test_empty_message(self):
        empty_message = ""
        encrypted = self.crcrypt.encrypt(empty_message)
        decrypted = self.crcrypt.decrypt(encrypted)
        self.assertEqual(empty_message, decrypted)

    def test_long_message(self):
        long_message = "A" * 10000
        encrypted = self.crcrypt.encrypt(long_message)
        decrypted = self.crcrypt.decrypt(encrypted)
        self.assertEqual(long_message, decrypted)

    def test_invalid_decryption(self):
        with self.assertRaises(ValueError):
            self.crcrypt.decrypt("invalid_base64_string")

    def test_message_too_long(self):
        too_long_message = "A" * (CRCrypt.MAX_MESSAGE_LENGTH + 1)
        with self.assertRaises(ValueError):
            self.crcrypt.encrypt(too_long_message)

    def test_wrong_key_decryption(self):
        message = "This is a secret message"
        encrypted = self.crcrypt.encrypt(message)
        wrong_key_crcrypt = CRCrypt("wrong_key")
        decrypted = wrong_key_crcrypt.decrypt(encrypted)
        self.assertNotEqual(message, decrypted)

if __name__ == '__main__':
    unittest.main()