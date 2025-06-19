# GODFREY-KEYGEN-CLI

        Version 1.0 | Built by RETZ

**Godfrey Keygen** is a secure, offline password generation and management tool built with Python. 
It combines cryptographic strength with a user-friendly GUI for everyday use — especially for those who want local control over their passwords.
This version is built of tool is built for **TERMUX**.

## Philosophy

This tool was developed with the mindset:
"Own your passwords without relying on any other tool or software, just a few things to remember; you have all your passwords safe in you hands."



## Features

- Password Generation using layered hashing and encoding:
- Argon2i hashing
- Hex conversion
- Base58, encoding 
- Secure Password Storage with encrypted local file
- Master Password Authentication
- Password Deletion & Full Database Wipe**
- Offline Use** — No data ever leaves your machine.

## Getting Started
**Firstly we will clone the repository into our termux machine.**
```bash
git clone https://github.com/BYTE-RETZ/GODFREY-KEYGEN-CLI.git
```
### Requirements

1.**Install dependencies:**

On your terminal:

```bash
pip install -r requirements.txt
```
The cryptography module for Termux
```bash
apt install python-cryptography
```
**Run the program**
```bash
python GODFREY_CLI.py
```


Next it will ask to set a **Master-Key**
Set any simple yet secure passsword.
This **Master-Key** will be used to further authenticate.
The **Master-Key** is stored in an encrypted file.
The **Master-Key** also be changed in the menu options.

## USAGE
1) Input a word that has to be hashed by argon2i.
2) Then enter a unique salt to generate hash.
3) The generated password is stored in an AES-256 encrypted file.
4) Passwords can be accessed and deleted by using in menu options.



