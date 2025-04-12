# Brute-Force Login Attack


## How we found the breach

We analyzed the login functionality of the web application hosted at:

`http://localhost:8080/index.php?page=signin`

This page contains a login form that accepts a username and password via query parameters in a GET-style request. During analysis, we noticed that:

* The application does not rate-limit login attempts.

* There is no account lockout mechanism after multiple failed logins.

* All login attempts return visible feedback (e.g., a flag string in the response) that can be used to detect a successful login.

* The login form is accessible via a crafted GET request:
`http://localhost:8080/index.php?page=signin&username=USER&password=PASS&Login=Login`

These characteristics make the login endpoint vulnerable to a brute-force attack.

We use a [Bash Script]() to automate a dictionary-based attack using a password list.


## How to exploit it

Once access is obtained using a valid password, an attacker may:

* Escalate privileges or access restricted areas of the site.

* Use exposed features to upload malicious files or extract sensitive data.

* Chain this with other vulnerabilities (e.g., LFI, RCE, SQLi) to compromise the system.

Additionally, if error messages or feedback from failed attempts are too specific, they may help attackers fine-tune their strategy.


## How to fix it

To secure the application against brute-force attacks:

1. Implement account lockout policies:

* Lock accounts after 5–10 failed login attempts.

* Use exponential backoff or CAPTCHA after repeated failures.

2. Rate-limit login attempts:

* Limit login requests per IP or per user account.

3. Use secure password storage:

* Store hashed and salted passwords with modern algorithms (e.g., bcrypt, Argon2).

4. Avoid GET requests for login:

* Accept credentials via POST only, and do not reflect them in the URL.

5. Generic error messages:

* Always show the same message for incorrect username and/or password (e.g., "Invalid credentials").

Enable monitoring and alerting:

Detect and alert unusual login behavior (e.g., hundreds of attempts in short time).
