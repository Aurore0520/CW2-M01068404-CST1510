import bcrypt
import os
USER_DATA_FILE = "users.txt"

def hash_password(plain_text_password):
   
    # TODO: Encode the password to bytes (bcrypt requires byte strings)
    password_bytes = plain_text_password.encode('utf-8')
    
    # TODO: Generate a salt using bcrypt.gensalt()
    salt = bcrypt.gensalt()
    
    # TODO: Hash the password using bcrypt.hashpw()
    hashed = bcrypt.hashpw(password_bytes, salt)
    
    # TODO: Decode the hash back to a string to store in a text file
    
    return hashed.decode('utf-8')

def verify_password(plain_text_password,hashed_password):
    
    # TODO: Encode both the plaintext password and the stored hash to byte
    password_bytes = plain_text_password.encode('utf-8')
    hash_bytes = hashed_password.encode('utf-8')
    
    # TODO: Use bcrypt.checkpw() to verify the password
    # This function extracts the salt from the hash and compares
    return bcrypt.checkpw(password_bytes, hash_bytes)
    

def register_user(username, password):
    # TODO: Check if the username already exists
    if user_exists(username):
        print(f"Error: Username '{username}' is already registered.")
        return False
    # TODO: Hash the password
    hashed = hash_password(password)  
    # TODO: Append the new user to the file
    # Format: username,hashed_password
    with open(USER_DATA_FILE, "a") as f:
        f.write(f"{username},{hashed}\n")
    
    print(f"User '{username}' registered successfully.")
    return True

    
def user_exists(username):
 # TODO: Handle the case where the file doesn't exist yet
 if not os.path.exists(USER_DATA_FILE):
     return False
 # TODO: Read the file and check each line for the username
 with open(USER_DATA_FILE, "r")as f:
     for line in f.readlines():
         user, hash = line.strip().split(',',1)
         if user == username:
             return True
 return False

def login_user(username, password):
    # Handle the case where no users are registered yet
    if not os.path.exists(USER_DATA_FILE):
        print("Error: No users registered yet.")
        return False

    # Search for the username in the file
    with open(USER_DATA_FILE, "r") as f:
        for line in f.readlines():
            user, hash = line.strip().split(',', 1)
            user = user.strip()
            hash = hash.strip()

            # If username matches, verify the password
            if user == username:
                if verify_password(password, hash):
                    print(f"Welcome back {user}!")
                    input("\nPress Enter to log out and return to the main menu...")
                    return True
                else:
                  print("Incorrect password.")
                  return False

    # Username not found
    print("Error: Username not found.")
    return False


def validate_username(username):
    return True, ""
def validate_password(password):
    return True, ""

def display_menu():
    """Displays the main menu options."""
    print("\n" + "="*50)
    print("  MULTI-DOMAIN INTELLIGENCE PLATFORM")
    print("  Secure Authentication System")
    print("="*50)
    print("\n[1] Register a new user")
    print("[2] Login")
    print("[3] Exit")
    print("-"*50)
def main():
    """Main program loop."""
    print("\nWelcome to the Week 7 Authentication System!")
    
    while True:
        display_menu()
        choice = input("\nPlease select an option (1-3): ").strip()
        
        if choice == '1':
            # Registration flow
            print("\n--- USER REGISTRATION ---")
            username = input("Enter a username: ").strip()
            
            # Validate username
            is_valid, error_msg = validate_username(username)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue
            
            password = input("Enter a password: ").strip()
            # Validate password
            is_valid, error_msg = validate_password(password)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue
            
            # Confirm password
            password_confirm = input("Confirm password: ").strip()
            if password != password_confirm:
                print("Error: Passwords do not match.")
                continue
            
            # Register the user
            register_user(username, password)
        
        elif choice == '2':
            # Login flow
            print("\n--- USER LOGIN ---")
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()
            
            # Attempt login
            if login_user(username, password):
                print("\nYou are now logged in.")
                print("\nPress Enter to return to main menu...")
                input()
            else:
                print("\n Login failed. Please check your username or password.")

        
        elif choice == '3':
            # Exit
            print("\nThank you for using the authentication system.")
            print("Exiting...")
            break
        
        else:
            print("\nError: Invalid option. Please select 1, 2, or 3.")
if __name__ == "__main__":
    main()
 
