# XSS Breach on feedbacks page

## How we found the breach

The feedback page at `http://localhost:8080/?page=feedback` contains a form with two input fields: one for the user's name and another for the feedback message. When a feedback is submitted, it gets displayed at the bottom of the page.

### Initial XSS testing

We started by testing if the application was vulnerable to Cross-Site Scripting (XSS) by attempting to inject JavaScript code. Our first approach was to insert a `<script>` tag into one of the form fields.

However, the name input field has a `maxlength` attribute set to 10 characters, which limits the length of input we can submit:

```html
<input name="txtName" type="text" size="30" maxlength="10" />
```

Using browser developer tools, we modified this attribute to allow longer input:

```html
<input name="txtName" type="text" size="30" maxlength="4200" />
```

We then attempted to inject a simple script tag in both fields:

```html
<script>
  alert("XSS");
</script>
```

The server appears to filter or escape `<script>` tags, preventing this basic XSS payload from executing.

### Bypassing script tag filtering

Since the server was blocking `<script>` tags, we tried a different approach using HTML event handlers. We injected an `<img>` tag with an `onerror` attribute that executes JavaScript when the image fails to load:

```html
<img src=a onerror=alert("XSS")>
```

This payload successfully bypassed the filtering. When the page reloads and displays the feedback, the malicious code is rendered as HTML. The browser attempts to load the image from an invalid source (`src=a`), which triggers the `onerror` event handler, executing the JavaScript and displaying an alert.

The rendered HTML shows:

```html
<td>
  Name :
  <img src="a" onerror='alert("XSS")' />
</td>
```

While this confirmed the XSS vulnerability, it didn't immediately reveal the flag. Through further testing, we discovered that simply entering the word `script` in one of the input fields causes the server to return the flag.

## How to exploit the breach / Why is it a problem

**Important distinction**: Simply modifying HTML in your browser's developer tools only affects your own view - it doesn't impact other users. The critical difference with XSS is that the malicious code gets **submitted to the server** through the form and then **rendered back** in the response.

In this vulnerability:

1. An attacker submits malicious HTML/JavaScript through the feedback form
2. The server processes the form submission and includes the malicious content in the response
3. The malicious code is rendered as HTML without proper sanitization
4. The JavaScript executes in the attacker's browser when the page reloads

This demonstrates that the server doesn't properly sanitize user input before displaying it. While in this specific case the XSS executes in the attacker's own browser (self-XSS), the same vulnerability could be exploited to affect other users if the feedbacks were stored and displayed to all visitors, or if the malicious payload was reflected in a way that other users could access it.

Cross-Site Scripting (XSS) vulnerabilities can lead to:

- **Session hijacking**: Stealing user session cookies and authentication tokens
- **Phishing attacks**: Injecting fake login forms to steal credentials
- **Keylogging**: Capturing user keystrokes and sensitive information
- **Defacement**: Modifying page content to display malicious content
- **Malware distribution**: Redirecting users to malicious websites
- **Account takeover**: Using stolen session tokens to impersonate users
- **Data exfiltration**: Sending sensitive data to attacker-controlled servers

## How to avoid the breach

- **Input validation and sanitization**: Validate and sanitize all user inputs on the server side
- **Output encoding**: Properly encode all user-generated content before displaying it (HTML entity encoding, JavaScript encoding, etc.)
- **Content Security Policy (CSP)**: Implement CSP headers to restrict which scripts can be executed
- **Use templating engines**: Use frameworks that automatically escape output by default
- **HTTP-only cookies**: Mark sensitive cookies as HTTP-only to prevent JavaScript access
- **Regular security audits**: Perform regular penetration testing and code reviews to identify XSS vulnerabilities
- **Input length limits**: Enforce proper server-side validation of input length, not just client-side restrictions
