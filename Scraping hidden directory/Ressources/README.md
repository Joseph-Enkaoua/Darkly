# Scraping .hidden folder file tree

## How we found the breach

The `robots.txt` file contained `Disallow: /.hidden`, revealing a hidden directory. When accessing `/.hidden`, we discovered directory listing was enabled, showing a recursive structure of subdirectories, each containing a `README` file with random sentences. We used the `fetch.js` script to scrape all `README` files recursively and concatenate their content into `all_readmes.txt`. Then we used `post-processing.js` to filter lines containing at least one digit (hashes contain digits, unlike plain text sentences), which identified the line containing the flag. To run: `cd Ressources && node fetch.js && node post-processing.js`.

## How to exploit the breach / Why is it a problem

Directory listing allows attackers to browse the server file system structure, enabling scraping of sensitive files. Attackers could search for private files such as `/etc/hosts`, `.env`, `/etc/passwd`, RSA keys, source code, or configuration files. Depending on the web server configuration, scrapers could access any folder on the computer, download sensitive data, or discover application internals. This information disclosure can lead to further attacks or complete system compromise.

## How to avoid the breach

Disable directory listing in the web server configuration (Nginx, Apache, etc.). Use a strong and secure server configuration that prevents browsing of the file system. Restrict access to sensitive directories using proper access controls. Never expose hidden directories or sensitive files through directory listings. Implement proper file permissions and use server-side access control lists.
