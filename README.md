# NI API


## About

This project involves the design of an API for a key-value store application.


## Technical stack

The technical stack used is:

* Python (3.8)
* Flask (1.1.2)
* SQLAlchemy (2.4.4) – SQLite
* (unittest?)
* Flask-testing (0.8.1)


## Installation

In the terminal, run:

```
python3.8 venv venv  
source venv/bin/activate  
pip install -r requirements.txt  
python app.py  
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
curl --header "Content-Type: application/json"   --request PUT   --data '{"my_key": "my_value"}' http://127.0.0.1:5000/keys
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


## Implementation decisions: possibilities and limitations

### Deleting

In the assingment it is specified to "delete a value" and "delete all values".  
If taken literally, the program would delete only the value(s), not deleting their   corresponding keys.  
However, the more common usage in these sort of deletions in APIs and is to remove  
completely the whole data entry. This later approach has been the one taken.  

### Checking
Since GET is present, Flask automatically adds support for the HEAD method and handles   
HEAD requests according to the HTTP RFC.  
This means that an extra implementation of HEAD is not necessary  

### Setting

#### Use cases
This programs accepts to set new key-pair values and to update already existent  
data entries.
If an already existent key is given when setting a key-value pair, the data entry will be   
updated and the old value overwritten with the new value.

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
#### Data type limitations
This implementation only accepts strings as values and could be improved to accept other   
data types. For now if another datatype would be needed in value, as in:    
```
{"some_numbers": [1, 3, 7])}
```   
the user would have to *stringy* the value as in   
```
{"some_numbers": "[1, 3, 7]")}
```

#### Character encoding
This implementation accepts setting key-value pairs with special characters (such as ä, ö, ü),   
but curl might not display them as expected(***TRUE? HOW CAN I CHECK THIS?***). 


### A note on endoint implementation

Sometimes one endpoint requires different methods.  
In some existing implementations of APIs, these methods are assigned in the same line, and   
handled inside the function with conditionals.  
In this implementation it was prefered to have one function per method per endpoint   
whenever possible, as it makes the code more understandable, maintainable and extendable.   
Additionally, the implementation of the testing of each functionality can keep the same   
structure as their implementation, making it also more clear and easier to maintain.  


## Tests

The tests for all implemented functionalities can be found in
```
test.py
```

## Possible improvements

### Database
SQLite is used in this implementation because it is good enough for this project and   
because of ease of use in development. However, in a production context it would have   
to be changed to PostgreSQL or similar.

#### Personal thoughts on PUT vs. POST

The functionality has been implemented as asked, but I would like to understand  
better the decissions behind having the endpoint /keys for setting a value with  
PUT.  
In the context of this API and the endpoints asked, I would have implemented to   
* Set a new key:value pair (POST /keys)
* Update an existent key (PUT/keys/{id})

(I also found this in the [RFC Hypertext Transfer Protocol --
HTTP/1.1 (9.6),](https://www.ietf.org/rfc/rfc2068.txt) I would be curious to  
understand better your point of view on this).  

## Git (spoilers!)
I didn't put (actively) any personal info, but I still appear as author of my  
git commits.  
If you would like to stay unbiased, but want to check my git commits, I  
recommend using functionalities where the author is not specified, like for 
example
```
git log --oneline
```

### Security
In a production context I would try to make this API secure and protected by  
implementing authentication and authorisation.

## Missing Implementations

I didn't have enough time to implement:

* Set an expiry time when adding a value (PUT /keys?expire_in=60)
* Support wildcard keys when getting all values (GET /keys?filter=wo$d)

