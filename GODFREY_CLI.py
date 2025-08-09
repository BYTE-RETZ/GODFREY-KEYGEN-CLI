import base64
<<<<<<< HEAD
import base58
=======
import base91
>>>>>>> e1ce553 (Replaced base-58 encoding with base-91 encoding for more entropic password)
from argon2.low_level import hash_secret_raw, Type
from cryptography.fernet import Fernet, InvalidToken
import os
import pyperclip
import hashlib

MASTER_KEY_FILE = "master.key"
PASSWORD_STORE_FILE = "passwords.enc"

master_password_cache = []

def derive_key(password):
    hashed = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(hashed[:32])

def encrypt_data(data, key):
    fernet = Fernet(key)
    return fernet.encrypt(data.encode())

def decrypt_data(data, key):
    fernet = Fernet(key)
    return fernet.decrypt(data).decode()

def save_master_password(password):
    key = derive_key(password)
    with open(MASTER_KEY_FILE, "wb") as f:
        f.write(encrypt_data(password, key))

def verify_master_password(password):
    if not os.path.exists(MASTER_KEY_FILE):
        return False
    key = derive_key(password)
    with open(MASTER_KEY_FILE, "rb") as f:
        encrypted = f.read()
    try:
        return decrypt_data(encrypted, key) == password
    except InvalidToken:
        return False

def change_master_password():
    old_pass = input("ENTER CURRENT MASTER KEY: ")
    if not verify_master_password(old_pass):
        print("ERROR: INCORRECT CURRENT MASTER KEY")
        return
    new_pass = input("ENTER A NEW MASTER KEY: ")
    if new_pass:
        save_master_password(new_pass)
        encrypt_existing_passwords(old_pass, new_pass)
        master_password_cache.clear()
        master_password_cache.append(new_pass)
        print("SUCCESS: MASTER KEY UPDATED SUCCESSFULLY")

def encrypt_existing_passwords(old_password, new_password):
    if not os.path.exists(PASSWORD_STORE_FILE):
        return
    old_key = derive_key(old_password)
    new_key = derive_key(new_password)
    with open(PASSWORD_STORE_FILE, "rb") as f:
        try:
            old_data = decrypt_data(f.read(), old_key)
        except:
            old_data = ""
    with open(PASSWORD_STORE_FILE, "wb") as f:
        f.write(encrypt_data(old_data, new_key))

def store_password(word, salt, password, master_password):
    line = f"Word: {word} | Salt: {salt} | Password: {password}\n"
    key = derive_key(master_password)
    if os.path.exists(PASSWORD_STORE_FILE):
        with open(PASSWORD_STORE_FILE, "rb") as f:
            try:
                decrypted = decrypt_data(f.read(), key)
            except:
                decrypted = ""
    else:
        decrypted = ""
    with open(PASSWORD_STORE_FILE, "wb") as f:
        f.write(encrypt_data(decrypted + line, key))

def access_stored_passwords():
    entered = input("ENTER MASTER KEY TO ACCESS PASSWORDS: ")
    if verify_master_password(entered):
        key = derive_key(entered)
        if os.path.exists(PASSWORD_STORE_FILE):
            with open(PASSWORD_STORE_FILE, "rb") as f:
                try:
                    content = decrypt_data(f.read(), key)
                except InvalidToken:
                    print("ERROR: FAILED TO DECRYPT PASSWORD FILE.")
                    return
            print("\nSTORED PASSWORDS:\n" + content)
        else:
            print("INFO: NO PASSWORDS STORED YET.")
    else:
        print("ERROR: INVALID MASTER KEY")

def delete_password():
    entered = input("ENTER MASTER KEY TO DELETE A PASSWORD: ")
    if verify_master_password(entered):
        key = derive_key(entered)
        if os.path.exists(PASSWORD_STORE_FILE):
            with open(PASSWORD_STORE_FILE, "rb") as f:
                try:
                    content = decrypt_data(f.read(), key)
                except InvalidToken:
                    print("ERROR: FAILED TO DECRYPT PASSWORD FILE.")
                    return
            lines = content.split("\n")
            password_list = [line for line in lines if line.strip()]
            if password_list:
                print("\nSTORED PASSWORDS:")
                for idx, password in enumerate(password_list):
                    print(f"{idx + 1}. {password}")
                try:
                    delete_index = int(input("ENTER THE INDEX NUMBER TO DELETE: ")) - 1
                    if delete_index < 0 or delete_index >= len(password_list):
                        raise ValueError("INVALID INDEX")
                    password_list.pop(delete_index)
                    updated_content = "\n".join(password_list)
                    with open(PASSWORD_STORE_FILE, "wb") as f:
                        f.write(encrypt_data(updated_content, key))
                    print("SUCCESS: PASSWORD DELETED SUCCESSFULLY")
                except ValueError as ve:
                    print(f"ERROR: {ve}")
            else:
                print("INFO: NO PASSWORD STORED YET.")
        else:
            print("INFO: NO PASSWORD STORED YET.")
    else:
        print("ERROR: INVALID MASTER KEY")

def generate_password():
    word = input("ENTER THE WORD: ")
    salt = input("ENTER THE SALT: ")
    if not word or not salt:
        print("WARNING: PLEASE ENTER BOTH WORD AND SALT.")
        return
    try:
        word_bytes = word.encode()
        salt_bytes = salt.encode()
        hashed = hash_secret_raw(
            secret=word_bytes,
            salt=salt_bytes,
            time_cost=15,
            memory_cost=2**17,
            parallelism=4,
            hash_len=17,
            type=Type.I
        )
        hex_hash = hashed.hex()
        reversed_hex = hex_hash[::-1]
<<<<<<< HEAD
        b58_encoded = base58.b58encode(reversed_hex.encode()).decode()
        final_password = b58_encoded[::-1]
=======
        b91_encoded = base91.encode(reversed_hex.encode())  # base91.encode returns string
        final_password = b91_encoded[::-1]
>>>>>>> e1ce553 (Replaced base-58 encoding with base-91 encoding for more entropic password)
        print(f"GENERATED PASSWORD: {final_password}")
        store_password(word, salt, final_password, master_password_cache[0])
    except Exception as e:
        print(f"ERROR GENERATING PASSWORD: {str(e)}")

def clear_database():
    master_pass = input("ENTER MASTER KEY TO CLEAR DATABASE (WARNING: THIS WILL DELETE ALL STORED PASSWORDS): ")
    if verify_master_password(master_pass):
        if os.path.exists(PASSWORD_STORE_FILE):
            os.remove(PASSWORD_STORE_FILE)
            print("SUCCESS: ALL THE PASSWORDS ARE WIPED.")
        else:
            print("INFO: DATABASE ALREADY EMPTY.")
    else:
        print("ERROR: INVALID MASTER KEY")

def initialize_master():
    if not os.path.exists(MASTER_KEY_FILE):
        if os.path.exists(PASSWORD_STORE_FILE):
            print("THE MASTERKEY FILE SEEMS TO BE MISPLACED OR DELETED.\nPLEASE RESTORE THE MASTERKEY FILE TO CONTINUE.\n")
            exit()
        pwd = input("SET A MASTER KEY: ")
        if pwd:
            save_master_password(pwd)
            master_password_cache.append(pwd)
            print("SUCCESS: MASTER KEY SET SUCCESSFULLY")
        else:
            exit()
    else:
        pwd = input("ENTER YOUR MASTER KEY: ")
        if pwd and verify_master_password(pwd):
            master_password_cache.append(pwd)
        else:
            print("ACCESS DENIED: INVALID MASTER KEY")
            exit()

def main_menu():
    while True:
        print("\n==== GODFREY KEYGEN CLI ====")
        print("1. Generate Password")
        print("2. Access Stored Passwords")
        print("3. Change Master Key")
        print("4. Delete Stored Password")
        print("5. Clear Database")
        print("6. Exit")
        choice = input("Select an option (1-6): ")
        if choice == "1":
            generate_password()
        elif choice == "2":
            access_stored_passwords()
        elif choice == "3":
            change_master_password()
        elif choice == "4":
            delete_password()
        elif choice == "5":
            clear_database()
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    initialize_master()
<<<<<<< HEAD
    main_menu() 
=======
    main_menu()
>>>>>>> e1ce553 (Replaced base-58 encoding with base-91 encoding for more entropic password)
