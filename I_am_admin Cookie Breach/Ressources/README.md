# I_am_admin Cookie Breach

## How we found the breach

By inspecting the website's cookies, we found `I_am_admin` with value `68934a3e9455fa72420237eb05902327`. We used the `hash_cookie.py` script to verify this is the MD5 hash of `false` and generate the MD5 hash of `true` (`b326b5062b2f0e69046810717534cb09`). We then modified the cookie value using browser dev tools. After refreshing, the website rendered an alert modal containing the flag.

## How to exploit the breach / Why is it a problem

The application relies on client-side cookies to determine admin status, which can be easily manipulated. Using MD5 to hash boolean values makes it trivial for attackers to identify the algorithm and generate valid hashes. The server trusts the cookie value without proper validation, allowing privilege escalation. This pattern can be exploited in e-commerce (modifying cart status/prices), user accounts (escalating privileges), or access control (bypassing restrictions).

## How to avoid the breach

Never trust client-side data for authorization decisions. Always validate user permissions on the server side using secure sessions. Store user roles in server-side sessions, not cookies. Use cryptographically secure random tokens with HMAC signing if tokens are necessary. Implement proper authorization checks on every request.
