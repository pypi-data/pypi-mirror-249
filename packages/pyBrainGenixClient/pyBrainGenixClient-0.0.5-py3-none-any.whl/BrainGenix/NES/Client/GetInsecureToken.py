# BrainGenix-NES
# AGPLv3

import requests


def GetInsecureToken(_Username:str, _Password:str):

    RequestURI = f"http://api.braingenix.org/Auth/GetToken?Username={_Username}&Password={_Password}"
    ServerRequst = requests.get(RequestURI)
    ResponseJSON = ServerRequst.json()

    if (ResponseJSON["StatusCode"] != 0):
        raise ValueError("Invalid Credentials Passed. Please Check Your Username/Password!")
    else:
        return ResponseJSON["AuthKey"]
