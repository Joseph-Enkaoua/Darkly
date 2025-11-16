# Custom curl request with evil headers

## How we found the breach

When clicking on the "BornToSec" text in the footer, we were redirected to `http://localhost:8080/index.php?page=b7e44c7a40c5f80139f0a50f3650fb2bd8d00b0d24667c4c2ca32c88e13b758f`. Inspecting the page source revealed HTML comments indicating we must come from `https://www.nsa.gov/` and use the browser `ft_bornToSec`. We used the `exploit.sh` script (or curl manually) with custom headers: first adding `Referer: https://www.nsa.gov/` (which returned "FIRST STEP DONE"), then adding `User-Agent: ft_bornToSec`, which returned the flag.

## How to exploit the breach / Why is it a problem

The server makes authorization decisions based on HTTP headers, which can be easily spoofed. Trusting client-controlled headers (Referer, User-Agent) for security decisions is fundamentally insecure. HTML comments reveal sensitive information, making exploitation trivial. Attackers can corrupt website statistics with fake referrer headers, bypass security controls, or manipulate business intelligence data.

## How to avoid the breach

Never use headers for authentication or authorization decisions. Always validate security on the server side using secure tokens or sessions. Remove all HTML comments containing sensitive information before deploying. Implement proper session-based authentication, CSRF tokens, and filter known spam referrers. Use security headers like Referrer-Policy and monitor for unusual header patterns.
