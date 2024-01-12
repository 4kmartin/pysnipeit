from Classes import SnipeIt, SnipeItConnection, SnipeItDate
from typing import Optional, List, Any
from returns.result import Result, Success, Failure
	
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

        
#Start Asset API Functions
def get_all_assets (connection:SnipeItConnection) -> List[SnipeItAsset]:
    assets:List[SnipeItAsset] = []
    rows:List[dict[str,Any]] = []
    # get total number of assets:
    number_of_assets:int = connection._get("/hardware?limit=1").json()["total"]
    if number_of_assets > 50:
        offset = 0
        limit = 50
        while offset < number_of_assets:
            response = connection._paginated_request("/hardware",limit,offset)
            rows += response.json()["rows"]
            offset += limit
    else:
        rows += connection._get(f"{connection.url}/hardware").json()["rows"]
    for json_asset in rows:
        assets.append(SnipeItAsset().from_json(json_asset))
    return assets

def get_asset_by_id (connection:SnipeItConnection, id:int) -> Result[SnipeItAsset, str]:
    result = connection._get(f"/hardware/{id}")
    return connection._asset_result(result) 

def _asset_result (connection:SnipeItConnection, result:Response) -> Result[SnipeItAsset, str]:
    if result.status_code == 200:
        if "status" not in result.json():
            return Success(SnipeItAsset().from_json(result.json()))
        else:
            return Failure(result.json()["messages"])
    else:
        return Failure(f"status code: {result.status_code}")

def get_asset_by_tag (connection:SnipeItConnection, asset_tag:str) -> Result[SnipeItAsset, str]:
    result = connection._get(f"/hardware/bytag/{asset_tag}")
    return connection._asset_result(result)

def get_asset_by_serial (connection:SnipeItConnection, serial:str) -> Result[SnipeItAsset, str]:
    result = connection._get(f"/hardware/byserial/{serial}")
    return connection._asset_result(result)

def delete_asset (connection:SnipeItConnection, id:int) -> None:
    connection._delete(f"/hardware/{id}")
    
def update_asset (connection:SnipeItConnection, id:int, asset:SnipeItAsset) -> Result[None,str]:
    url = f"/hardware/{id}"
    payload = asset.into_json()
    response = connection._put(url,payload)
    if response.status_code == 200:
        if "status" in result.json():
            return Failure(str(result.json()["messages"]))
        else:
            return Success(None)
    else:
        return Failure(f"status code: {response.status_code}")
    
def checkout_asset (
    connection, id:int, 
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

    response = connection._post(url,payload)
    if response.status_code == 200:
        if "status" in response.json():
            return Failure(response.text)
        else:
            return Success(None)
    else:
        return Failure(f"status code: {response.status_code}")
        
def checkin_asset (
    connection,
    id:int,
    status_id:int,
    name:Optional[str]=None,
    note:Optional[str]=None,
    location_id:Optional[str]=None
) -> Result[None,str]:
    url = f"/hardware/{id}/checkin"
    payload = {
        "status_id":status_id,
    }

    if name:
        payload["name"] = name
    if note:
        payload["note"] = note
    if location_id:
        payload["location_id"] = location_id

    response = connection._post(url,payload)
    if response.status_code == 200:
        if "status" in response.json():
            return Failure(response.text)
        else:
            return Success(None)
    else:
        return Failure(f"status code: {response.status_code}")

def audit_asset (
    connection,
    asset_tag:str,
    location_id:Optional[int]=None,
    next_audit_date: Optional[SnipeItDate]=None
) -> Result[None, str]:
    url = "/hardware/audit"
    payload = {
        "asset_tag":asset_tag
    }
    if location_id:
        payload["location_id"] = location_id
    if next_audit_date:
        payload["next_audit_date"] = str(next_audit_date)
    response = connection._post(url,payload)
    if response.status_code == 200:
        if "status" in response.json():
            return Failure(response.text)
        else:
            return Success(None)
    else:
        return Failure(f"status code:{response.status_code}")

def restore_asset (connection:SnipeItConnection, id:int) -> None:
    url = f"/hardware/{id}/restore"
    connection._post(url,None)

def list_audit_due_assets (connection:SnipeItConnection) -> List[SnipeItAsset]:
    url = "/hardware/audit/due"
    audit_due:List[SnipeItAsset] = []
    request = connection._get(url)
    for json_asset in request.json()["rows"]:
        audit_due.append(SnipeItAsset().from_json(json_asset))
    return audit_due

def list_overdue_assets (connection:SnipeItConnection) -> List[SnipeItAsset]:
    url = "/hardware/audit/overdue"
    overdue:List[SnipeItAsset] = []
    request = connection._get(url)
    for json_asset in request.json()["rows"]:
        overdue.append(SnipeItAsset().from_json(json_asset))
    return overdue

def list_asset_licences (connection:SnipeItConnection, id:int) -> Result[List[SnipeItLicense],str]:
    url = f"/hardware/{id}/licenses"
    request = connection._get(url)
    if requst.status_code == 200:
        if "status" in request.json():
            return Failure(request.text)
        else:
            licenses:List[SnipeItAssets] =[]
            for row in request.json()["rows"]:
                licenses.append(SnipItLicense().from_json(row))
            return Success(licences)
    else:
        return Failure(f"Status Code: {request.status_code}")

#End Asset API Functions
