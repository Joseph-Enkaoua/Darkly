# Brute-Force Login Attack

## How we found the breach

We analyzed the login functionality at `http://localhost:8080/index.php?page=signin`. The application does not rate-limit login attempts, has no account lockout mechanism, and accepts credentials via GET request parameters. All login attempts return visible feedback that can be used to detect successful logins. We used the `bruteforce.sh` script with a password list to automate the brute-force attack.

## How to exploit the breach / Why is it a problem

Once access is obtained using a valid password, attackers can escalate privileges, access restricted areas, upload malicious files, extract sensitive data, or chain this vulnerability with others (LFI, RCE, SQLi) to compromise the system. The lack of rate limiting allows unlimited automated attempts.

## How to avoid the breach

Implement account lockout policies (lock accounts after 5-10 failed attempts), rate-limit login attempts per IP or user account, use secure password storage (bcrypt, Argon2), accept credentials via POST only, show generic error messages, and enable monitoring for unusual login behavior.
