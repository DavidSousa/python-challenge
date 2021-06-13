# Python challenge

## API's

<br/>

### Receives 1 email as input and returns a list of data leaks where the email appeared

<br/>

- API path: */dataLeaks/?email=\<email\>*

<br/>

### Receives 1 domain as input and returns a list of emails that were leaked from that domain

<br/>

- API path */emails/?domain=\<domain\>*

<br/>

## Data load and storage

<br/>

1. All data is initially loaded from both URL's in parallel 
2. Emails are validated against the provided regular expression
3. Each email is then mapped to a *namedtuple* composed of fields: email, domain and company. The *namedtuple* was used because values can be accessed by field name and because it's more memory efficient than dictionaries.
4. The list of emails is used to start our *database*, which then initializes a lookup table for each field
5. The *database* has a function *get* which allows a consumer to filter the leaked emails by a field name and its value (e.g. db.get(company='Linkedin'))
