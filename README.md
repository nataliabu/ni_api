# NI API


## About

This project involves the design of an API for a key-value store application.


## Technical stack

The technical stack used is:

* Python (3.8)
* Flask (1.1.2)
* SQLAlchemy (2.4.4) – SQLite
* Flask-testing (0.8.1)


## Installation

In the terminal, run:

```
python3.8 venv venv
source venv/bin/activate
pip install -r requirements.txt
python db_initialisation.py
```

## Usage

In order to run this API, run in the terminal

```
python main.py
```

The functionalities implemented include:

### Get a value (GET /keys/{id})

In the terminal, run (replacing {id} with a valid key):

```
curl http://127.0.0.1:5000/keys/{id}
```

### Get all keys and values (GET /keys)

In the terminal, run:

```
curl http://127.0.0.1:5000/keys
```

### Set a value (PUT /keys)

In the terminal, run:

```
curl --header "Content-Type: application/json" \
	I—request PUT \
	--data '{"my_key": "my_value"}' http://127.0.0.1:5000/keys
```

#### Data type expected
When setting a key-value pair, the data should be put as strings in a dictionary, as in
```
{"my_key":"my_value"}
```
This implementation also admits adding several key-value pairs at once, as in:
```
{
	"key1":"value 1",
	"key2":"value 2"
	"key3":"value 3"
}
```

### Check if a value exists (HEAD /keys/{id})

In the terminal, run (replacing {id} with a valid key):

```
curl --head http://127.0.0.1:5000/keys/mykey
```
### Delete a value (DELETE /keys/{id})

In the terminal, run (replacing {id} with a valid key):
```
curl -X DELETE http://127.0.0.1:5000/keys/{id}
```
### Delete all values (DELETE /keys)

In the terminal, run:
```
curl -X DELETE http://127.0.0.1:5000/keys
```
### Support wildcard keys when getting all values (GET /keys?filter=wo$d)

In the terminal, run (replacing wo$d with the characters you want to filter by):
```
curl http://127.0.0.1:5000/keys?filter=wo$d
```
### Tests

The tests for all implemented functionalities can be run with:
```
python test.py
```
## Implementation decisions: possibilities and limitations

### Deleting

In the assignment it is specified to "delete a value" and "delete all values".
If taken literally, the program would delete only the value(s), not deleting their
corresponding keys.
However, the more common usage in these sort of deletions in APIs and is to remove
completely the whole data entry. This later approach is the one I have taken.

### Checking
Since GET is present, Flask automatically adds support for the HEAD method and handles
HEAD requests according to the HTTP RFC.
This means that an extra implementation of HEAD is not necessary.

### Setting

#### Use cases
This functionality allows the user to:
* set new key-pair values
* update already existent data entries.

If an already existent key is given when setting a key-value pair, the data entry will be
updated and the old value overwritten with the new value.

#### Data type limitations
This implementation only accepts strings as values. If I had more time, I would improve it to accept other
data types. For now if another datatype would be needed in the value, as in:
```
{"some_numbers": [1, 3, 7])}
```
the user would have to *stringify* the value as in:
```
{"some_numbers": "[1, 3, 7]")}
```

#### Character encoding
This implementation accepts setting key-value pairs with special characters (such as ä, ö, ü),
but curl might not display them as expected.


### A note on endpoint implementation

Sometimes one endpoint requires different methods.
In some existing implementations of APIs, these methods are assigned in the same line, and
handled inside one function with conditionals.
In general I tend to prefer having one function per method per endpoint,
as it makes the code more understandable, maintainable and extendable.


## Tests implementation

The automated tests of all functionalities keep a similar structure as their implementation:
one class per method per endpoint. Keeping this structure makes the tests script more clear
and easier to maintain.

## Possible improvements

### Database
SQLite is used in this implementation because it is good enough for this project and
because of ease of use with SQLAlchemy in development. However, in a production context
it would have to be changed to PostgreSQL or similar.

### Personal thoughts on PUT vs. POST

The functionality has been implemented as asked, but I would like to understand
better the decisions behind having PUT /keys for setting a value.
In the context of this API and the endpoints asked, I would have implemented to
* Set a new key:value pair with POST /keys
* Update an existent key with PUT/keys/{id}

I also found this in the [RFC Hypertext Transfer Protocol --
HTTP/1.1 (9.6),](https://www.ietf.org/rfc/rfc2068.txt) I would be curious to
understand your point of view on this (section 9.6).

### Git (spoilers!)
I didn't put (actively) any personal info, but I still appear as author of my
git commits. There might be a way to delete this, but I didn’t have enough time
for solving that.
If you would like to stay unbiased, but want to check my git commits, I
recommend using functionalities where the author is not specified, like for
example:
```
git log --oneline
```

### Security
In a production context I would try to make this API secure and protected by
implementing authentication and authorisation.

### Missing Implementations

I didn't have enough time to implement:

* Set an expiry time when adding a value (PUT /keys?expire_in=60)

I also didn’t have the time to learn how to provide an integration with a monitoring solution,
but I am keen on learning!

