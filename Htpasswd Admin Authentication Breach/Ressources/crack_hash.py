#!/usr/bin/env python3
"""
MD5 Hash Cracker for htpasswd files
This script attempts to crack MD5 hashes from htpasswd files by testing common passwords.
"""
import hashlib
import sys

def crack_md5_hash(target_hash, password_list):
    """
    Attempts to crack an MD5 hash by testing passwords from a list.
    
    Args:
        target_hash: The MD5 hash to crack
        password_list: List of passwords to test
    
    Returns:
        The password if found, None otherwise
    """
    print(f"Attempting to crack MD5 hash: {target_hash}\n")
    print("Testing passwords...\n")
    
    for password in password_list:
        # Calculate MD5 hash of the password
        md5_hash = hashlib.md5(password.encode()).hexdigest()
        
        if md5_hash == target_hash:
            print(f"✓ FOUND! Password is: {password}")
            print(f"  Hash: {md5_hash}")
            return password
        else:
            print(f"✗ {password:20} -> {md5_hash}")
    
    print("\n✗ Password not found in the provided list.")
    print("  Try:")
    print("  - Adding more passwords to the list")
    print("  - Using online MD5 lookup tools:")
    print("    * https://md5decrypt.net/")
    print("    * https://md5online.org/")
    print("    * https://crackstation.net/")
    return None

if __name__ == "__main__":
    # The hash from the htpasswd file
    target_hash = "437394baff5aa33daa618be47b75cb49"
    
    # Common passwords to test
    common_passwords = [
        "password",
        "123456",
        "qwerty",
        "qwerty123",
        "qwerty123@",
        "admin",
        "root",
        "password123",
        "12345678",
        "letmein",
        "welcome",
        "monkey",
        "1234567890",
        "password1",
        "root123",
        "admin123",
        "qwerty@",
        "qwerty123!",
        "qwerty123#",
        "qwerty123$",
    ]
    
    # Allow hash to be passed as command line argument
    if len(sys.argv) > 1:
        target_hash = sys.argv[1]
    
    # Allow password list file to be passed as argument
    if len(sys.argv) > 2:
        try:
            with open(sys.argv[2], 'r') as f:
                common_passwords = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"Error: File {sys.argv[2]} not found.")
            sys.exit(1)
    
    result = crack_md5_hash(target_hash, common_passwords)
    
    if result:
        print(f"\n✓ Successfully cracked the hash!")
        print(f"  Username: root")
        print(f"  Password: {result}")
        print(f"\n  You can now login at: http://localhost:8080/admin")
        sys.exit(0)
    else:
        sys.exit(1)

