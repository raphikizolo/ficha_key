# ficha_key
A library that encrypts the data in a file e.g. A properties file for sensitive data like api token strings and passwords.

# Quickstart
1. Install using pip as follows:
    ```python
    pip install ficha-key

    ```
2. Import to your project:
    ```python
    from ficha_key import api
    ```
3. Generate the secret key for the first time:
    ```python
    api.add_key()
    ```
More about secret key generation is in the key generation section. 
At this point ficha-key is ready to encrypt data. 
ficha-key expects a data file where it will save the encrypted data. 
The idea is this library will expect you to create a file that will hold the encrypted data. 
This file can be public if you want. It can be seen by anybody. 
You can have it in your project repository. 
Ficha-key always encrypts data then saves it there.
So long as ficha-key has been configured in the client's 
computer the app should be able to fetch and store the encrypted properties using the ficha-key library.
# Encryption and decryption
1. To add a token to the encrypted file:

    ```python
    ficha = api.get_ficha()
    ficha.encrypt(property_name, property_value, encrypted_data_file)
    ```
2. To get a token from the encrypted data file:
    ```python
    ficha = api.get_ficha()
    property_value = ficha.get_stored_token(property_name, encrypted_data_file)
    ```
3. To get all properties stored in the encrypted data file:
    ```python
    ficha = api.get_ficha()
    properties: dict = ficha.decryptd(encrypted_data_file)
    ```
4. To delete a stored property from the encrypted file:
    ```python
    ficha = api.get_ficha()
    property_value = ficha.remove_stored_token(property_name, encrypted_data_file)
    ```

# Key generation
1. Generate the secret key for the first time. Please note that this will ask the user to confirm (y/n) from a console:
    ```python
    api.add_key()
    ```
2. Generate key without asking for confirmation from user:
    ```python
    api.add_key(False)
    ```
    ***
    ***
    This is suitable if you have imported ficha-key as a module into some other project. Option 1. above is suitable if your project is a console application and you want the user to confirm the generation of a new key.
    ***
    ***

3. Check if a secret key exists and generate a new one if there's no existing secret key:
    ```python
    api.try_add_key()
    ```
4. Check if a secret key exists and generate a new one if there's no existing secret key, without asking the user for confirmation:
    ```python
    api.try_add_key(False)
    ```