# Project 5: Phonebook Lookups with RPC
### Task
**Design a remote phonebook service using RPC where clients can query and manage
contact information. The backend can be memory-based or use a database for
persistence.**  
**Variant A: A modifiable phonebook where users can add/edit/delete entries (all
in-memory)**

### How to launch the server and clients?
One can easily run the server by typing in the shell this command:  
```sh
python3 server.py
```
A client can be launched in a similar way:
```sh
python3 client.py
```
### Client commands
Here is the list of client's commands: *Add*, *Get*, *Edit*, *Delete*, and *List*. In general all of them are self-explanatory and all of the arguments are asked interactively.  
The *Add* command requires 1) contact's name; 2) its phone number; 3) its TTL in seconds.  
The *Get* command requires the contact's name and returns its phone number.  
The *Edit* command requires the contact's name and optionally its new phone number and TTL. If you provide just empty lines, nothing will be changed.  
The *Delete* command requires the contact's name and deletes it from the phonebook.
And the *List* command prints out all of the entries in the phonebook.
To exit just enter the empty line instead of any command.
## Tests
The tests are in the "tests" directory and can be ran by this command (from the project's working directory):
```sh
for i in tests/test*.sh; do $i; done
```
It's important that before the start of the tests the server should not be already started.
The test no. 1 checks the correctness of the sequential access to the server. The client 1 adds a contact and the client 2 checks that the new data are correct.  
The test no. 2 first runs two clients in parallel, both of them add a contact. Then the clinet 3 checks the contact list's correctness.
