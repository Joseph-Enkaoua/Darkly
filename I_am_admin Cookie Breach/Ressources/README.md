# I_am_admin Cookie Breach

## How we found the breach

From anywhere on the website, by inspecting the element you can have access the app's cookies.

Where we can found:

```
I_am_admin	68934a3e9455fa72420237eb05902327
```

By googling `68934a3e9455fa72420237eb05902327` it results as the md5 hash of `false`. Then by hashing `true` we get `b326b5062b2f0e69046810717534cb09`. Thanks to our browser devtool we're able to change the cookie's value by the md5 hash of `true`.

After refreshing, there we go the website renders an alert modal containing a flag.

## How to exploit it

### Step-by-step exploitation:

1. **Access the website**: Navigate to `http://localhost:8080` (or the target website).

2. **Inspect cookies**: 
   - Open browser developer tools (F12 or Right-click → Inspect)
   - Go to the "Application" tab (Chrome) or "Storage" tab (Firefox)
   - Navigate to "Cookies" section
   - Look for the `I_am_admin` cookie

3. **Analyze the cookie value**:
   - The cookie value is: `68934a3e9455fa72420237eb05902327`
   - This is an MD5 hash
   - Search online or use a hash cracker to find it's the hash of `false`

4. **Generate the hash for `true`**:
   - MD5 hash of `true` is: `b326b5062b2f0e69046810717534cb09`
   - You can verify this using:
     ```bash
     echo -n "true" | openssl dgst -md5
     ```
   - Or use the provided script: `hash_cookie.py`

5. **Modify the cookie**:
   - In browser dev tools, edit the `I_am_admin` cookie value
   - Change it from `68934a3e9455fa72420237eb05902327` to `b326b5062b2f0e69046810717534cb09`
   - Save the changes

6. **Refresh the page**: After refreshing, the website should render an alert modal containing the flag.

### Alternative method using browser console:

You can also modify cookies using JavaScript in the browser console:

```javascript
document.cookie = "I_am_admin=b326b5062b2f0e69046810717534cb09; path=/";
location.reload();
```

## Why This Is a Problem

* **Client-Side Security Control**: The application relies on client-side cookies to determine admin status, which can be easily manipulated.

* **Predictable Hashing**: Using MD5 to hash boolean values (`true`/`false`) makes it trivial for attackers to:
  - Identify the hash algorithm
  - Generate valid hashes for different values
  - Bypass authentication/authorization checks

* **No Server-Side Validation**: The server appears to trust the cookie value without proper validation, allowing privilege escalation.

* **Insecure Cookie Implementation**: Cookies should not be used to store sensitive authorization information, especially in a way that can be easily tampered with.

* **Real-World Impact**: As mentioned, this vulnerability pattern can be exploited in various scenarios:
  - E-commerce: Modifying cart status or prices
  - User accounts: Escalating privileges
  - Access control: Bypassing restrictions
  - Session manipulation: Corrupting user sessions

## How to Fix It

1. **Server-Side Validation**:
   * Never trust client-side data for authorization decisions.
   * Always validate user permissions on the server side.
   * Use server-side sessions to track user authentication state.

   ```php
   // Bad: Trusting cookie value
   if ($_COOKIE['I_am_admin'] === hash('md5', 'true')) {
       // Grant admin access
   }
   
   // Good: Server-side session check
   session_start();
   if (isset($_SESSION['user_id']) && $_SESSION['is_admin'] === true) {
       // Grant admin access
   }
   ```

2. **Use Secure Session Management**:
   * Implement proper session-based authentication.
   * Store user roles and permissions in server-side sessions, not cookies.
   * Use secure, HTTP-only, and SameSite cookies for session IDs only.

   ```php
   // Set secure session cookie
   ini_set('session.cookie_httponly', 1);
   ini_set('session.cookie_secure', 1);
   ini_set('session.cookie_samesite', 'Strict');
   ```

3. **Avoid Storing Sensitive Data in Cookies**:
   * Cookies should only contain session identifiers, not authorization flags.
   * Never store hashed or encrypted authorization data in cookies.
   * Use server-side databases or session storage for user roles.

4. **Use Strong, Unpredictable Tokens**:
   * If you must use tokens, use cryptographically secure random tokens.
   * Use HMAC with a secret key to sign tokens.
   * Implement token expiration and rotation.

   ```php
   // Good: Signed token with secret
   $secret = 'your-secret-key';
   $token = hash_hmac('sha256', $user_id . $is_admin, $secret);
   ```

5. **Implement Proper Authorization Checks**:
   * Check user permissions on every request.
   * Use middleware or access control lists (ACLs).
   * Log all authorization attempts for security monitoring.

6. **Security Headers**:
   * Implement Content Security Policy (CSP).
   * Use secure cookie flags (HttpOnly, Secure, SameSite).
   * Add security headers to prevent various attacks.

## Additional Notes

This vulnerability demonstrates a critical security flaw where client-side data is trusted for authorization. In real-world applications, this could lead to:

- Unauthorized access to admin panels
- Privilege escalation attacks
- Data breaches
- System compromise

Always remember: **Never trust the client**. All authorization and authentication decisions must be made on the server side.

