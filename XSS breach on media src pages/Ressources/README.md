# XSS breach on media src pages

## How we found the breach

While examining the homepage, we discovered that clicking on the NSA image redirected to a URL with a `src` parameter: `/?page=media&src=nsa`.

### Testing parameter manipulation

We began investigating whether the `src` parameter could be controlled by modifying its value. Setting it to `nsa2` showed that the page renders an `<object>` element, and the value we provide gets inserted directly into the element's `data` attribute.

Testing with `/` as the parameter value resulted in the root page being embedded inside the object, confirming that the parameter value is used without proper validation.

### Researching Data URLs

The `data` attribute of an `<object>` tag can accept any valid URL according to web standards. Since we knew that images could be embedded using base64 encoding in `<img>` tags, we looked up the formal specification and found MDN's documentation on Data URLs, which explained this technique.

An example from the documentation demonstrated embedding HTML directly in a URL:

```
data:text/html,<script>alert('hi');</script>
```

### Attempting XSS with plain data URL

We tested whether we could inject JavaScript using a data URL by URL-encoding the payload and setting it as the `src` parameter:

```
http://localhost:8080/?page=media&src=data:text/html,%3Cscript%3Ealert(%27hi%27);%3C/script%3E
```

The JavaScript executed successfully, proving the XSS vulnerability exists. However, this method didn't yield the flag.

### Switching to base64 encoding

Next, we attempted base64 encoding the HTML payload, following the same approach used for embedding images. The base64 representation of `<script>alert('hi');</script>` is:

```
PHNjcmlwdD5hbGVydCgnaGknKTs8L3NjcmlwdD4=
```

We constructed a data URL using this base64-encoded payload:

```
http://localhost:8080/?page=media&src=data:text/html;base64,PHNjcmlwdD5hbGVydCgnaGknKTs8L3NjcmlwdD4=
```

This method successfully executed the payload. The `;base64` suffix is required to inform the browser that the data following the comma is base64-encoded and needs to be decoded before use.

## How to exploit the breach / Why is it a problem

**Important distinction**: Simply modifying HTML in your browser's developer tools only affects your own view - it doesn't impact other users. The critical difference with XSS is that the malicious code is **sent to the server** via the URL parameter and then **rendered back** in the response.

In this vulnerability:

1. An attacker crafts a malicious URL with a data URL containing JavaScript in the `src` parameter
2. When the victim visits this URL (or clicks a link), the server processes the parameter
3. The server includes the malicious parameter value directly in the HTML response without sanitization
4. The victim's browser receives and executes the malicious JavaScript

This is called **Reflected XSS** because the malicious payload is reflected back in the server's response. The attack works by tricking victims into visiting the malicious URL, often through phishing emails or malicious links.

Cross-Site Scripting (XSS) vulnerabilities can lead to:

- **Session hijacking**: Stealing user session cookies and authentication tokens
- **Phishing attacks**: Injecting fake login forms to steal credentials
- **Keylogging**: Capturing user keystrokes and sensitive information
- **Defacement**: Modifying page content to display malicious content
- **Malware distribution**: Redirecting users to malicious websites
- **Account takeover**: Using stolen session tokens to impersonate users
- **Data exfiltration**: Sending sensitive data to attacker-controlled servers

In this case, the application directly uses user-controlled input (the `src` query parameter) in the `data` attribute of an `<object>` tag without proper validation or sanitization. This allows attackers to inject arbitrary HTML and JavaScript code that gets executed in the victim's browser.

## How to avoid the breach

- **Input validation**: Validate and whitelist allowed values for the `src` parameter
- **Output encoding**: Properly encode all user-generated content before using it in HTML attributes
- **Content Security Policy (CSP)**: Implement CSP headers to restrict which scripts can be executed
- **URL validation**: Validate that the `src` parameter contains only expected, safe values
- **Sanitization**: Sanitize all user input before using it in HTML attributes or data URLs
- **Use allowlists**: Instead of allowing arbitrary URLs, maintain a list of allowed media sources
- **Regular security audits**: Perform regular penetration testing and code reviews to identify XSS vulnerabilities
