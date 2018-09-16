import pyrebase

def create_firebase_user(auth):
    #prompt user to provide credentials
    print('Register your Knocknock account.')
    email = input('Enter your email: ')
    password = input('Enter your password: ')
    #return firebase user
    return auth.create_user_with_email_and_password(email, password)

def login_to_firebase(auth):
    #prompt user to login on frontend
    print('Login to your Knocknock account.')
    email = input('Enter your email: ')
    password = input('Enter your password: ')
    #return firebase user
    return auth.sign_in_with_email_and_password(email, password)

def authenticate_user(auth):
    choice = input('Enter \"r\" to register new user or enter \"l\" to login: ')
    if choice == 'r':
        return create_firebase_user(auth)
    else:
        return login_to_firebase(auth)
