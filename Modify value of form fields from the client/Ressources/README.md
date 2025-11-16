# Modify value of form fields from the client

## How we found the breach

From the page `http://localhost:8080/?page=recover` (Sign In -> I forgot my password), we found a hidden input field: `<input type="hidden" name="mail" value="webmaster@borntosec.com" maxlength="15" />`. This input is within a password recovery form. After modifying its value using browser developer tools and submitting, the server returned a page containing the flag.

## How to exploit the breach / Why is it a problem

The server trusts the submitted email value without proper validation. Client-side restrictions like `maxlength` can be easily bypassed. Hidden fields often store sensitive data that should not be client-modifiable. This allows attackers to change the recipient of password reset emails, hijack password recovery processes, or access accounts by receiving reset tokens meant for others. Modifying hidden fields can also bypass business logic (e.g., changing prices, user IDs, permissions).

## How to avoid the breach

Never trust client-side data. All form data must be validated on the server side. Don't store email addresses, user IDs, or other sensitive data in hidden form fields. Use server-side sessions or tokens instead. Verify that the email belongs to the requesting user before allowing password recovery. Implement rate limiting, use time-limited single-use tokens, and add CSRF protection.
