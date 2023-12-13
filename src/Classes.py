from requests import get

class SnipeItConnection:

    def __init__(self):
        self.headers = {}
        self.url = ""

    def connect (snipe_it_url:str, personal_access_token:str, validate:bool=False) -> None:
        self.headers = {
            "Accept":"application/json",
            "Content-type":"application/json",
            "Authorization":f"Bearer {personal_access_token}",
        }

        self.url=snipe_it_url

        if validate:
            test = get(f"{self.url}/api/v1/hardware",headers=self.headers).status_code
            if test == 200:
                print("connection successful")
            else:
                print("Connection failed aborting")
                quit()
            

class SnipeItAsset

class SnipeItUser

class SnipeItAccessory

class SnipeItConsumable

class SnipeItComponent

class SnipeItKit

class SnipeItCompany

class SnipeItLocation

class SnipeitStatusLabel

class SnipeItCategory

class SnipeItManufacturer

class SnipeItSupplier

class SnipeItAssetMaintenance

class SnipeItDepartment

class SnipeItGroup

class SnipeItSettings

class SnipeItReports