# Modify value of form fields from the client

## How we found the breach

From the page `http://localhost:8080/?page=recover` (Sign In -> I forgot my password). By inspecting the page we can find the following HTML tag:

```html
<input
  type="hidden"
  name="mail"
  value="webmaster@borntosec.com"
  maxlength="15"
/>
```

This input is within a recover password form. Here we can find the admin email, statically defined in the client code. After modifying its value and submitting, the server returns a page containing the flag.

## How to exploit it

### Step-by-step exploitation:

1. **Navigate to the recovery page**:

   - Go to `http://localhost:8080/?page=recover`

2. **Inspect the page source**:

   - Right-click on the page → "Inspect" or "View Page Source"
   - Look for hidden form fields, especially those with `type="hidden"`

3. **Identify the vulnerable field**:

   - Find the hidden input field: `<input type="hidden" name="mail" value="webmaster@borntosec.com" maxlength="15">`
   - Note that it has a `maxlength="15"` attribute, which is a client-side validation

4. **Modify the hidden field**:

   - Using browser developer tools, locate the hidden input element
   - Change the `value` attribute from `webmaster@borntosec.com` to your own email address
   - You may also need to remove or modify the `maxlength` attribute if your email is longer than 15 characters

5. **Submit the form**:
   - Fill in any other required fields (if any)
   - Click the submit button
   - The server should return a page containing the flag

### Using browser developer tools:

**Method 1: Direct HTML modification**

1. Open Developer Tools (F12)
2. Go to the "Elements" or "Inspector" tab
3. Find the hidden input field
4. Double-click on the `value` attribute
5. Change it to your email address
6. Submit the form

**Method 2: Using JavaScript console**

```javascript
// Find and modify the hidden input
document.querySelector('input[name="mail"]').value = "your-email@example.com";
// Remove maxlength restriction if needed
document.querySelector('input[name="mail"]').removeAttribute("maxlength");
// Submit the form
document.querySelector("form").submit();
```

### Using curl (if the form uses GET method):

```bash
# Replace with your email and check the form method first
curl "http://localhost:8080/?page=recover&mail=your-email@example.com&submit=Submit"
```

## Why This Is a Problem

- **Client-Side Validation Only**: The `maxlength="15"` attribute is a client-side restriction that can be easily bypassed. Server-side validation is missing or insufficient.

- **Hidden Field Manipulation**: Hidden form fields are often used to store sensitive data (like user IDs, email addresses, prices) that should not be client-modifiable.

- **Information Disclosure**: The hidden field reveals the admin email address (`webmaster@borntosec.com`), which could be used for social engineering or targeted attacks.

- **No Server-Side Validation**: The server appears to trust the submitted email value without proper validation, allowing attackers to:

  - Change the recipient of password reset emails
  - Potentially hijack password recovery processes
  - Access accounts by receiving reset tokens meant for others

- **Real-World Impact**:
  - **Account Takeover**: Attackers could change the email in password recovery forms to their own, gaining access to victim accounts.
  - **Email Enumeration**: Testing different email addresses could reveal which accounts exist in the system.
  - **Business Logic Bypass**: Modifying hidden fields can bypass intended business logic (e.g., changing prices, user IDs, permissions).

## How to Fix It

1. **Never Trust Client-Side Data**:

   - All form data must be validated on the server side.
   - Never use hidden fields to store sensitive or security-critical data.
   - Always verify the user's identity and permissions server-side.

   ```php
   // Bad: Trusting hidden field value
   $email = $_POST['mail']; // Can be modified by client
   sendPasswordReset($email);

   // Good: Server-side validation
   session_start();
   $email = $_SESSION['user_email']; // From authenticated session
   // Or verify the email belongs to the current user
   if ($email === $_SESSION['user_email']) {
       sendPasswordReset($email);
   }
   ```

2. **Remove Sensitive Data from Hidden Fields**:

   - Don't store email addresses, user IDs, or other sensitive data in hidden form fields.
   - Use server-side sessions or tokens instead.
   - If you must use hidden fields, sign them cryptographically.

   ```php
   // Bad: Hidden field with email
   <input type="hidden" name="mail" value="webmaster@borntosec.com">

   // Good: Use session or token
   <?php
   session_start();
   // Email stored in session, not in form
   ?>
   ```

3. **Implement Server-Side Validation**:

   - Validate all input on the server, regardless of client-side restrictions.
   - Check that the email belongs to the requesting user.
   - Verify user identity before allowing password recovery.

   ```php
   // Good: Server-side validation
   function requestPasswordReset($email) {
       // Validate email format
       if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
           return false;
       }

       // Verify email belongs to authenticated user
       session_start();
       if (!isset($_SESSION['user_id'])) {
           return false;
       }

       $user = getUserById($_SESSION['user_id']);
       if ($user['email'] !== $email) {
           return false; // Email doesn't match user's account
       }

       // Proceed with password reset
       sendPasswordResetToken($email);
       return true;
   }
   ```

4. **Use Secure Password Recovery**:

   - Require additional verification (security questions, SMS, etc.).
   - Implement rate limiting to prevent abuse.
   - Use time-limited, single-use tokens.
   - Log all password recovery attempts.

   ```php
   // Good: Secure password recovery
   function securePasswordRecovery($email) {
       // Rate limiting
       if (getRecoveryAttempts($email) > 5) {
           return "Too many attempts. Please try again later.";
       }

       // Generate secure token
       $token = bin2hex(random_bytes(32));
       $expires = time() + 3600; // 1 hour

       // Store token in database (not in hidden field)
       storeRecoveryToken($email, $token, $expires);

       // Send email with token
       sendRecoveryEmail($email, $token);

       return "Recovery email sent.";
   }
   ```

5. **Remove Client-Side Restrictions for Security**:

   - Don't rely on `maxlength`, `min`, `max`, or other HTML5 attributes for security.
   - These are for user experience only, not security.
   - Always enforce limits server-side.

   ```html
   <!-- Bad: Client-side only restriction -->
   <input type="hidden" name="mail" value="admin@example.com" maxlength="15" />

   <!-- Good: No sensitive data in form -->
   <!-- Email retrieved from server-side session -->
   ```

6. **Implement CSRF Protection**:

   - Use CSRF tokens for all forms.
   - Verify tokens on form submission.
   - Prevent cross-site request forgery attacks.

   ```php
   // Generate CSRF token
   $_SESSION['csrf_token'] = bin2hex(random_bytes(32));

   // In form
   <input type="hidden" name="csrf_token" value="<?php echo $_SESSION['csrf_token']; ?>">

   // On submission
   if ($_POST['csrf_token'] !== $_SESSION['csrf_token']) {
       die("Invalid CSRF token");
   }
   ```

## Additional Notes

This vulnerability is similar to the "Form Tampering" vulnerability but focuses specifically on hidden fields. Hidden fields are particularly dangerous because:

- They're not visible to users, making them seem "secure"
- Developers often use them to store data they don't want users to see
- They're easily modifiable with browser developer tools
- They're often trusted by server-side code without validation

**Key Takeaway**: Never store sensitive or security-critical data in hidden form fields. Always validate and verify all data on the server side.
