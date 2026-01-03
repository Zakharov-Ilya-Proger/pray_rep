from bcrypt import checkpw



async def check_password(password, api_password):
    print(password, api_password)
    return checkpw(password.encode(), api_password)
