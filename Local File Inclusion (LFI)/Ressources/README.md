# Local File Inclusion (LFI)

## How we found the breach

Sources:

[portswigger](https://portswigger.net/web-security/file-path-traversal)

[portswigger](https://owasp.org/www-community/attacks/Path_Traversal)


From the site home page, when clicking the "sign in" button we are riderected to the sign-in page with the url `http://IP/index.php?page=signin`.

Depending on how the server handles the parameter, we could pass any filename containing absolute paths to other file from the server file system.

A commonly hacked sensitive file is the /etc/passwd containing a trace of every computer registered user.

We use the script `traverse.py` to search an alert containing the flag. We add `../` to the searched path every circle until the flag is found or the defined limit is exceeded.

The script can run with xpipe if we want to avoid creating a virtual environment: `pipx run --spec requests python3 traverse.py`


## How to exploit it

By being able to browse the server file system, the hacker could steal sensitive information like user credentials from /etc/passwd or database passwords from config files. He could also execute a previously uploaded script, such as a malicious PHP file in the server’s file tree, to run commands or take control of the system.

## How to fix it

Restrict the page parameter to a whitelist of allowed files (e.g., signin, home) or use basename() to strip ../, ensuring only intended files are included and blocking access to the file system.