# Htpasswd Admin Authentication Breach

## How we found the breach

Searching the `robots.txt` file revealed hidden directories (`/whatever`, `/.hidden`). In the `/whatever` directory, we downloaded an htpasswd file containing `root:437394baff5aa33daa618be47b75cb49`. We used the `crack_hash.py` script to crack the MD5 hash, which revealed the password `qwerty123@`. After navigating to `/admin` and logging in with these credentials, we obtained the flag.

## How to exploit the breach / Why is it a problem

The robots.txt file reveals hidden directories containing sensitive information. Using MD5 for password hashing is insecure as it's fast to compute and vulnerable to rainbow table attacks. Storing htpasswd files in web-accessible directories allows attackers to download and crack passwords, leading to unauthorized admin access.

## How to avoid the breach

Don't expose sensitive directories in robots.txt. Move htpasswd files outside the web root directory and use proper file permissions. Replace MD5 with modern hashing algorithms like bcrypt or Argon2. Use non-obvious routes for admin panels and implement strong password policies.
