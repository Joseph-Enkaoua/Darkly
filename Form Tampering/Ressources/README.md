#  Form Tampering / Client-Side Manipulation


## How we found the breach

During analysis of the survey submission form, we noticed that the dropdown options in the HTML were hardcoded in the following way:
```
<select name="score">
  <option value="1">1</option>
  <option value="2">2</option>
  <option value="3">3</option>
</select>
```

While inspecting the form, we used browser developer tools (e.g., right-click → “Inspect”) to modify the HTML locally before submitting the form.


## What We Changed

We manually changed one of the <option> elements to:

```
<option value="1337">A</option>
```

Then we submitted the form with this modified input.


## What Happened

The server responded with a flag, indicating that it accepted the tampered value. This confirmed that the server did not validate the form input against the list of allowed choices.


## Why This Is a Problem

By trusting the frontend form inputs, the server opens itself up to tampering attacks. Any user with minimal knowledge of browser dev tools can:

* Modify form values or add new ones.

* Trigger unintended behavior (like receiving secret content or accessing restricted resources).

* Bypass validations intended to protect business logic.

This specific case could hint at a flag reward system, hidden input testing, or an insecure internal scoring logic based on value.


## How to Fix It

1. Validate Input on the Server Side:

* Never trust values coming from the frontend.

* Check submitted value against a server-side list of allowed options.

2. Use a whitelist:

```
$allowed_values = [10, 20, 30];
if (!in_array($_POST['score'], $allowed_values)) {
    die("Invalid score.");
}
```

3. Avoid sensitive logic in frontend:

* If rewards or privileges are given based on form values, ensure the logic happens securely on the backend.

4. Consider CSRF protection:

* If forms can be abused easily, CSRF tokens help reduce automated attacks.