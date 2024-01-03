# BrainGenix-NES
# AGPLv3

import requests

class RequestHandler:

    def __init__(self, _URIBase:str, _Token:str):
        self.URIBase = _URIBase
        self.Token = _Token

        # Check that API is up
        try:
            Response = requests.get(f"{self.URIBase}/Hello")
        except:
            raise ConnectionError("Unable To Connect To API Endpoint")
        

    
    # Make Query
    def MakeQuery(self, _URIStub:str):
        # try:
        Response = requests.get(f"{self.URIBase}{_URIStub}")
        ResponseJSON = Response.json()
        if (ResponseJSON["StatusCode"] != 0):
            raise ConnectionError(f"Error During API Call To '{self.URIBase}{_URIStub}', API Returned Status Code '{ResponseJSON['StatusCode']}'")
            return None
        return ResponseJSON
        # except :
        #     raise ConnectionError(f"HTTP Error During API Call To '{self.URIBase}{_URIStub}'")
        #     return None
        
    def MakeAuthenticatedQuery(self, _URIStub:str):
        URIStub = f"{_URIStub}&AuthKey={self.Token}"
        return self.MakeQuery(URIStub)