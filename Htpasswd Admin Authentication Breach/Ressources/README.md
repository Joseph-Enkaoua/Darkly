# Htpasswd Admin Authentication Breach

## How we found the breach

Searching inside the robots.txt file, we could find:

```
User-agent: *
Disallow: /whatever
Disallow: /.hidden
```

Searching in the `/whatever` directory we were able to download the htpasswd file containing:

```
root:437394baff5aa33daa618be47b75cb49
```

By googling the retrieved hash, we can find it's the md5 hash of `qwerty123@`.

It's really common to find admin panel using the route `/admin` on any web apps, this is also the case here.

After navigating to `/admin` we can find an authentication form, asking for a username and a password.

Fill the username with `root` and password by `qwerty123@` to finally submit. Bim there we go, a flag appears.

## How to exploit it

1. **Access robots.txt**: Navigate to `http://localhost:8080/robots.txt` to discover hidden directories.

2. **Explore hidden directories**: Check directories listed in robots.txt (e.g., `/whatever`, `/.hidden`) for sensitive files.

3. **Download htpasswd file**: Access `http://localhost:8080/whatever/htpasswd` to retrieve authentication credentials.

4. **Crack the hash**: Use online MD5 lookup tools or hash cracking tools to decode the password hash:
   - Online tools: md5decrypt.net, md5online.org, crackstation.net
   - Command line: `echo -n "password" | openssl dgst -md5` to verify
   - Python script: Calculate MD5 hash and compare

5. **Access admin panel**: Navigate to `http://localhost:8080/admin` and login with the cracked credentials.

## Why This Is a Problem

* **Information Disclosure**: The robots.txt file reveals hidden directories that may contain sensitive information.

* **Weak Password Storage**: Using MD5 for password hashing is insecure as it's fast to compute and vulnerable to rainbow table attacks.

* **Exposed Credentials**: Storing htpasswd files in web-accessible directories allows attackers to download and crack passwords.

* **Predictable Admin Routes**: Using common routes like `/admin` makes it easier for attackers to find authentication endpoints.

* **Weak Passwords**: Simple passwords like `qwerty123@` are easily cracked, especially when using weak hashing algorithms.

## How to Fix It

1. **Secure robots.txt**:
   * Don't expose sensitive directories in robots.txt if they contain confidential information.
   * Use proper access controls (e.g., .htaccess) to protect sensitive directories.

2. **Use Strong Password Hashing**:
   * Replace MD5 with modern, secure hashing algorithms like bcrypt, Argon2, or PBKDF2.
   * These algorithms are designed to be slow and resistant to brute-force attacks.

   ```php
   // Bad: MD5 (fast, insecure)
   $hash = md5($password);
   
   // Good: bcrypt (slow, secure)
   $hash = password_hash($password, PASSWORD_BCRYPT);
   ```

3. **Protect Sensitive Files**:
   * Move htpasswd files outside the web root directory.
   * Use proper file permissions (e.g., 600) to restrict access.
   * Configure web server to deny access to sensitive file types.

   ```apache
   # .htaccess example
   <FilesMatch "\.(htpasswd|htaccess)$">
       Order allow,deny
       Deny from all
   </FilesMatch>
   ```

4. **Implement Strong Passwords**:
   * Enforce password complexity requirements.
   * Use password managers to generate and store strong passwords.
   * Implement password policies (minimum length, special characters, etc.).

5. **Secure Admin Routes**:
   * Use non-obvious routes for admin panels.
   * Implement additional security measures like IP whitelisting or two-factor authentication.
   * Use session-based authentication instead of basic HTTP authentication when possible.

6. **Regular Security Audits**:
   * Regularly scan for exposed sensitive files.
   * Monitor access logs for suspicious activity.
   * Keep software and dependencies up to date.

