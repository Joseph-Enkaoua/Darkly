# Query param driving redirection

## How we found the breach

On the website, we noticed redirect links in the footer (e.g., `index.php?page=redirect&site=facebook`). We discovered that the `site` parameter controls where users are redirected without proper validation. By modifying the parameter to an external URL (e.g., `index.php?page=redirect&site=http://evil.com`), we were able to redirect users to arbitrary external domains. The server accepted the redirect and returned the flag.

## How to exploit the breach / Why is it a problem

To exploit this, craft a malicious URL like `http://localhost:8080/index.php?page=redirect&site=http://evil.com` and share it with victims. When victims click the link, they're redirected to the attacker's site. Attackers can use this for phishing attacks where victims believe they're on a trusted domain (the legitimate site's URL is visible), enabling credential theft, session token harvesting, or malware distribution. This can also bypass security controls, manipulate user behavior, or chain with other attacks. The vulnerability exists because the server trusts user-controlled query parameters for redirect destinations without validation.

## How to avoid the breach

Never trust user-controlled input (query parameters, POST data) for redirect destinations. Always validate redirect URLs against a whitelist of allowed domains or use server-side mapping (e.g., map "facebook" to the actual Facebook URL server-side). Use relative URLs for internal redirects. Implement proper redirect validation that checks the destination is within the same domain or an explicitly allowed list. Consider using redirect tokens or signed URLs instead of direct URL parameters.
