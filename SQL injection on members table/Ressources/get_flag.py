#!/usr/bin/env python3
"""
Script to decrypt MD5 hash and generate SHA256 flag
"""

import hashlib

# MD5 hash found in the countersign column
md5_hash = "5ff9d0165b4f92b14994e5c685cdce28"

# Known MD5 decryption result (FortyTwo)
# In practice, you would use an MD5 lookup service or dictionary
plaintext = "FortyTwo"

print(f"MD5 hash: {md5_hash}")
print(f"MD5 decrypt result: {plaintext}")

# Lowercase the result
lowercased = plaintext.lower()
print(f"Lowercased: {lowercased}")

# Generate SHA256 hash
flag = hashlib.sha256(lowercased.encode()).hexdigest()
print(f"\nFlag: {flag}")

