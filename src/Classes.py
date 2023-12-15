from requests import get, Response, delete, put
from abc import ABC, abstractmethod
from typing import Optional, List, Any
from returns.result import Result, Success, Failure

class SnipeIt (ABC):

    @abstractmethod
    def from_json(self,json_data:dict) -> None:
        pass

    @abstractmethod
    def into_json (self) -> dict[Any]:
        pass


class SnipeItAsset (SnipeIt):
    def from_json (self, json_data:dict) -> None:
        self.id:int = json_data["id"]
        self.name = json_data["name"]
        self.asset_tag = json_data["asset_tag"]
        self.serial = json_data["serial"]
        self.model = json_data["model"]
        self.model_number = json_data["model_number"]
        self.eol = json_data["eol"]
        self.status_label = json_data["status_label"]
        self.category = json_data["category"]
        self.manufacturer = json_data["manufacturer"]
        self.supplier = json_data["supplier"]
        self.notes = json_data["notes"]
        self.order_number = json_data["order_number"]
        self.company = json_data["company"]
        self.location = json_data["location"]
        self.rtd_location = json_data["rtd_location"]
        self.image = json_data["image"]
        self.qr = json_data["qr"]
        self.alt_barcode = json_data["alt_barcode"]
        self.assigned_to = json_data["assigned_to"]
        self.warranty_months = json_data["warranty_months"]
        self.warranty_expires = json_data["warranty_expires"]
        self.created_at = json_data["created_at"]
        self.updated_at = json_data["updated_at"]
        self.last_audit_date = json_data["last_audit_date"]
        self.next_audit_date = json_data["next_audit_date"]
        self.deleted_at = json_data["deleted_at"]
        self.purchase_date = json_data["purchase_date"]
        self.age = json_data["age"]
        self.last_checkout = json_data["last_checkout"]
        self.expected_checkin = json_data["expected_checkin"]
        self.purchase_cost = json_data["purchase_cost"]
        self.checkin_counter = json_data["checkin_counter"]
        self.checkout_counter = json_data["checkout_counter"]
        self.requests_counter = json_data["requests_counter"]
        self.user_can_checkout = json_data["user_can_checkout"]
        self.custom_fields = json_data["custom_fields"]
        self.available_actions = json_data["available_actions"]
    

class SnipeItUser (SnipeIt):
    pass


class SnipeItAccessory (SnipeIt):
    pass


class SnipeItConsumable (SnipeIt):
    pass


class SnipeItComponent (SnipeIt):
    pass


class SnipeItKit (SnipeIt):
    pass


class SnipeItCompany (SnipeIt):
    pass


class SnipeItLocation (SnipeIt):
    pass


class SnipeitStatusLabel (SnipeIt):
    pass


class SnipeItCategory (SnipeIt):
    pass


class SnipeItManufacturer (SnipeIt):
    pass


class SnipeItSupplier (SnipeIt):
    pass


class SnipeItAssetMaintenance (SnipeIt):
    pass


class SnipeItDepartment (SnipeIt):
    pass


class SnipeItGroup (SnipeIt):
    pass


class SnipeItSettings (SnipeIt):
    pass


class SnipeItReportsclass (SnipeIt):
    pass


class SnipeItConnection:
    def __init__(self) -> None:
        self.headers = {}
        self.url = ""

    def connect (snipe_it_url:str, personal_access_token:str, validate:bool=False) -> None:
        self.headers = {
            "Accept":"application/json",
            "Content-type":"application/json",
            "Authorization":f"Bearer {personal_access_token}",
        }

        self.url=f"{snipe_it_url}/api/v1/"

        if validate:
            test = get(f"{self.url}/hardware?limit=1,",headers=self.headers).status_code
            if test == 200:
                print("connection successful")
            elif test == 401:
                print("An Error has Occured! Unauthenticated")
                quit()
            else:
                print("Connection failed for unknown reasons.\nAborting.")
                quit()

    def _api_url (self, api_endpoint:str) -> str:
        if api_endpoint[0] != '/':
            api_endpoint = f"/{api_endpoint}"
        return f"{self.url}{api_endpoint}"
    
    def _get (self, api_endpoint:str) -> Response:
        url = self._api_url(api_endpoint)
        return get(url, headers=self.headers)

    def _paginated_request (self, api_endpoit:str, limit:int, offset:int) -> Response:
        url = f"{api_endpoint}?limit={limit}&offset={offset}&sort=id&order=asc"
        return self._get(url)

    def _delete (self, api_enpoint:str) -> Response:
        url= self._api_url(api_endpoint)
        return delete(url,headers=self.headers)

    def _put (self, api_endpoint, payload:dict[Any]) -> Response:
        url = self._api_url(api_endpoint)
        return put(url, headers=headers, json=payload)
        

    def get_all_assets (self) -> List[SnipeItAsset]:
        assets:List[SnipeItAsset] = []
        rows:List[dict[str,any]] = []
        # get total number of assets:
        number_of_assets:int = get(f"{self.url}/hardware?limit=1").json()["total"]
        if number_of_assets > 50:
            offset = 0
            limit = 50
            while offset < number_of_assets:
                response = self._paginated_request("/hardware",limit,offset)
                rows += response.json()["rows"]
                offset += limit
        else:
            rows += self._get(f"{self.url}/hardware").json()["rows"]
        for json_asset in rows:
            assets.append(SnipeItAsset().from_json(json_asset))
        return assets

    def get_asset_by_id (self, id:int) -> Result[SnipeItAsset, str]:
        result = self._get(f"/hardware/{id}")
        return self._asset_result(result) 

    def _asset_result (self, result:Response) -> Result[SnipeItAsset, str]:
        if result.status_code == 200:
            if "status" not in result.json():
                return Success(SnipeItAsset().from_json(result.json()))
            else:
                return Failure(result.json()["messages"])
        else:
            return Failure(f"status code: {result.status_code}")

    def get_asset_by_tag (self, asset_tag:str) -> Result[SnipeItAsset, str]:
        result = self._get(f"/hardware/bytag/{asset_tag}")
        return self._asset_result(result)

    def get_asset_by_serial (self, serial:str) -> Result[SnipeItAsset, str]:
        result = self._get(f"/hardware/byserial/{serial}")
        return self._asset_result(result)

    def delete_asset (self, id:int) -> None:
        self._delete(f"/hardware/{id}")
        
    def update_asset (self, id:int, asset:SnipeItAsset) -> Result[None,str]:
        url = f"/hardware/{id}"
        payload = asset.into_json()
        response = self._put(url,payload)
        if response.status_code == 200:
            if "status" in result.json():
                return Failure(str(result.json()["messages"]))
            else:
                return Success(None)
        else:
            return Failure(f"status code: {response.status_code}")
        
    def checkout_asset (
        self, id:int, 
        status_id:int, 
        checkout_to_type:str, 
        assigned_id:int,
        expected_checkin:Optional[str]=None,
        checkout_at:Optional[str]=None,
        name:Optional[str]=None,
        note:Optional[str]=None
    ) -> Result[None,str]:
        url = f"/hardware/{id}/checkout"
        payload = {
            "status_id":status_id,
            "checkout_to_type":checkout_to_type,
        }
        match checkout_to_type:
            case "user":
                payload ["assigned_user"] = assigned_id
            case "location":
                payload ["assigned_location"] = assigned_id
            case "asset":
                payload ["assigned_asset"] = assigned_id
            case _:
                return Failure(f"unknown value for checkout_to_type: {checkout_to_type}")
        if expected_checkin:
            payload ["expected_checkin"] = expected_checkin
        if checkout_at:
            payload ["checkout_at"] = checkout_at
        if name:
            payload ["name"] = name
        if note:
            payload ["note"] = note

        response = self._post(url,payload)
        if response.status_code == 200:
            if "status" in response.json():
                return Failure(response.text)
            else:
                return Success(None)
        else:
            return Failure(f"status code: {response.status_code}")
            