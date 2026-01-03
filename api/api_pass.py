from bcrypt import checkpw



async def check_password(password, api_password='$2b$10$mSXNp6D0PbLp3vCFeWrReuMucVU7DA1k5rYYJ9j7KCNEMehnM.826'):
    print(password, api_password)
    return checkpw(password.encode(), api_password.encode())
