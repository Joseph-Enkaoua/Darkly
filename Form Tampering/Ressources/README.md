# Form Tampering / Client-Side Manipulation

## How we found the breach

During analysis of the survey submission form, we noticed that the dropdown options in the HTML were hardcoded. We used browser developer tools to modify the HTML locally, changing one of the `<option>` elements from a valid value to `1337`. After submitting the form with this modified input, the server responded with a flag, confirming that it did not validate the form input against the list of allowed choices.

## How to exploit the breach / Why is it a problem

By trusting frontend form inputs, the server opens itself up to tampering attacks. Any user with minimal knowledge of browser dev tools can modify form values, trigger unintended behavior, or bypass validations intended to protect business logic. This allows attackers to access restricted resources or manipulate application behavior.

## How to avoid the breach

Never trust values coming from the frontend. Always validate input on the server side by checking submitted values against a server-side whitelist of allowed options. Implement CSRF protection and ensure sensitive logic happens securely on the backend, not in the frontend.
