import unittest
from src.core import CRCrypt
import base64

class TestDecrypt(unittest.TestCase):
    def setUp(self):
        self.key = "test_key_456"
        self.crcrypt = CRCrypt(self.key)

    def test_decrypt_encrypted_message(self):
        original_message = "This is a secret message for decryption testing."
        encrypted = self.crcrypt.encrypt(original_message)
        decrypted = self.crcrypt.decrypt(encrypted)
        self.assertEqual(original_message, decrypted)

    def test_decrypt_with_wrong_key(self):
        original_message = "Another secret message"
        encrypted = self.crcrypt.encrypt(original_message)
        wrong_key_crcrypt = CRCrypt("wrong_key")
        decrypted = wrong_key_crcrypt.decrypt(encrypted)
        self.assertNotEqual(original_message, decrypted)

    def test_decrypt_invalid_ciphertext(self):
        invalid_ciphertext = "not_a_valid_base64_string"
        with self.assertRaises(ValueError):
            self.crcrypt.decrypt(invalid_ciphertext)

    def test_decrypt_modified_ciphertext(self):
        original_message = "Message to be tampered with"
        encrypted = self.crcrypt.encrypt(original_message)
        tampered_ciphertext = base64.b64encode(base64.b64decode(encrypted)[:-1] + b'\x00').decode('ascii')
        decrypted = self.crcrypt.decrypt(tampered_ciphertext)
        self.assertNotEqual(original_message, decrypted)

    def test_decrypt_empty_message(self):
        empty_message = ""
        encrypted = self.crcrypt.encrypt(empty_message)
        decrypted = self.crcrypt.decrypt(encrypted)
        self.assertEqual(empty_message, decrypted)

if __name__ == '__main__':
    unittest.main()