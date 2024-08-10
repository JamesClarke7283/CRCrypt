import argparse
from src.core import CRCrypt
import sys

def encrypt_message(args):
    crcrypt = CRCrypt(key=args.key, cube_dim=args.cube_dim)
    encrypted = crcrypt.encrypt(args.message)
    print(f"Encrypted message: {encrypted}")

def decrypt_message(args):
    crcrypt = CRCrypt(key=args.key, cube_dim=args.cube_dim)
    try:
        decrypted = crcrypt.decrypt(args.ciphertext)
        print(f"Decrypted message: {decrypted}")
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description="CRCrypt: Clarke's Rubik's Cube Cryptography CLI")
    subparsers = parser.add_subparsers()

    # Encrypt subcommand
    parser_encrypt = subparsers.add_parser('encrypt', help="Encrypt a message")
    parser_encrypt.add_argument('key', type=str, help="Encryption key")
    parser_encrypt.add_argument('message', type=str, help="Message to encrypt")
    parser_encrypt.add_argument('--cube_dim', type=int, default=4, help="Cube dimension (default: 4x4)")
    parser_encrypt.set_defaults(func=encrypt_message)

    # Decrypt subcommand
    parser_decrypt = subparsers.add_parser('decrypt', help="Decrypt a message")
    parser_decrypt.add_argument('key', type=str, help="Decryption key")
    parser_decrypt.add_argument('ciphertext', type=str, help="Ciphertext to decrypt")
    parser_decrypt.add_argument('--cube_dim', type=int, default=4, help="Cube dimension (default: 4x4)")
    parser_decrypt.set_defaults(func=decrypt_message)

    # Parse arguments and call the appropriate function
    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
