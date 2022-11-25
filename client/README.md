# Client

The client is responisble for encrypting and decrypting messages and other sensitive data that needs to be passed through the server. 

It consists of multiple classes that interact to create a fully functional chat. 

## User class

### Cryptography

The User class uses the ```cryptography``` library to implement RSA key-pairs for private and public keys. These keys are created when a ```User``` object is initialized. 

The User class provides methods for storing and reading the keys from storage, ```save_keys()``` and ```read_keys(password)```, such that they are still available after restarting the application. 
