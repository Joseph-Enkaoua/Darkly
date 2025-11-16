# File upload breach - send script as image with fake content-type

## How we found the breach

On the page `http://localhost:8080/?page=upload`, we discovered an image upload form that appeared to only accept JPG files. After analyzing the multipart form request, we discovered that the server only validated the `Content-Type` header in the form-data. By manually crafting a request with `Content-Type: image/jpeg` while sending a PHP script, we bypassed the validation and successfully uploaded the file, receiving the flag in the response.

## How to exploit the breach / Why is it a problem

Upload the provided `script.php` file using curl with the `Content-Type` header set to `image/jpeg`:

```bash
curl -X POST \
  -F "uploaded=@Ressources/script.php;type=image/jpeg" \
  -F "MAX_FILE_SIZE=100000" \
  -F "Upload=Upload" \
  -H "Cookie: I_am_admin=68934a3e9455fa72420237eb05902327" \
  "http://localhost:8080/?page=upload"
```

The server only checks the client-controlled `Content-Type` header without verifying actual file content (magic bytes). This allows attackers to upload executable scripts (PHP, Python, etc.) to web-accessible directories, enabling remote code execution. This can lead to complete server compromise, data theft, lateral movement, or backdoor installation. Uploaded SVG files with JavaScript can cause XSS attacks, and large file uploads can cause denial of service.

## How to avoid the breach

Always verify file content using magic bytes (file signatures), not just headers. Use server-side libraries to verify file types. Implement a strict whitelist of allowed file extensions and rename uploaded files. Store files outside the web root directory and serve them through secure scripts. Disable script execution in upload directories via server configuration. Enforce server-side file size limits, sanitize filenames, scan uploaded files, and implement access controls with rate limiting.
