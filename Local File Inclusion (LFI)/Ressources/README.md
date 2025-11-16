# Local File Inclusion (LFI)

## How we found the breach

From the site home page, clicking the "sign in" button redirects to `http://localhost:8080/index.php?page=signin`. We discovered that the `page` parameter could be manipulated to include files from the server file system using path traversal techniques. We used the `traverse.py` script to automate the attack by adding `../` to the path until the flag was found.

## How to exploit the breach / Why is it a problem

By being able to browse the server file system, attackers can steal sensitive information like user credentials from `/etc/passwd` or database passwords from config files. They could also execute previously uploaded malicious scripts to run commands or take control of the system, leading to complete server compromise.

## How to avoid the breach

Restrict the page parameter to a whitelist of allowed files (e.g., signin, home) or use `basename()` to strip `../` sequences, ensuring only intended files are included and blocking access to the file system.
