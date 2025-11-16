# Image Search Engine SQL injection

## How we found the breach

The image search functionality on the website is vulnerable to SQL injection. Similar to the members SQL injection breach, we discovered that the search parameter could be manipulated to execute arbitrary SQL queries.

### Discovering the database structure

The `list_images` table structure was discovered using the same SQL injection technique applied to the members page, where we queried `information_schema.columns` to enumerate all database tables and columns:

```
1 AND 1=2 UNION SELECT table_name, column_name FROM information_schema.columns
```

This revealed the `list_images` table exists with its column structure. Alternatively, on the image search page itself, we can discover the table structure through trial and error by testing different column names in the CONCAT function until we find valid columns:

```
-1 UNION SELECT 1, CONCAT(id, url, title, comment) FROM list_images
```

Through these methods, we discovered the `list_images` table contains the following columns:

- `id`
- `url`
- `title`
- `comment`

### Extracting data from list_images

Using UNION SELECT with CONCAT, we retrieved all entries from the `list_images` table:

**Input:**

```
-1 UNION SELECT 1, CONCAT(id, url, title, comment) FROM list_images
```

**Output:**

- Image 1: NSA program image
- Image 2: Number 4242
- Image 3: Google logo
- Image 4: Earth image
- Image 5: Contains the hash `1928e8083cf461a51303633093573c46` in the comment field

### Retrieving the flag

The comment column of the last image contained an MD5 hash: `1928e8083cf461a51303633093573c46`

1. **MD5 decryption**: Decrypting the hash gives us the plain text: `albatroz`
2. **SHA256 hashing**: Hashing `albatroz` with SHA256 algorithm produces the flag: `f2a29020ef3132e01dd61df97fd33ec8d7fcd1388cc9601e7db691d17d4d6188`

## How to exploit the breach / Why is it a problem

SQL injection vulnerabilities can lead to:

- **Data theft**: Leaking entire database contents, including users' personal information, emails, passwords, and other sensitive data
- **Data manipulation**: Inserting entries into tables (e.g., adding credits to an account, creating admin users)
- **Data destruction**: Deleting all entries from tables, potentially causing complete data loss if backups are not available
- **Privilege escalation**: Accessing or modifying data beyond the intended permissions

## How to avoid the breach

- **Use parameterized queries (prepared statements)**: Never concatenate user input directly into SQL queries
- **Input validation**: Validate and sanitize all user inputs before using them in database queries
- **Least privilege**: Database users should have minimal necessary permissions
- **Error handling**: Don't expose database errors to users; use generic error messages
- **Web Application Firewall (WAF)**: Implement a WAF to detect and block SQL injection attempts
- **Regular security audits**: Perform regular penetration testing and code reviews to identify vulnerabilities
