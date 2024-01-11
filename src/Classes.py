from requests import get, Response, delete, put
from abc import ABC, abstractmethod
from typing import Optional, List, Any
from returns.result import Result, Success, Failure


class SnipeItDate:
    def __init__ (self, year:int, month:int, day:int) -> Result[None,str]:
        if self.validate_date (year,month,day):
            self.day = day
            self.month = month
            self.year = year
            return Success(None)
        else:
            return Failure(f"{year}-{month}-{day} is not a valid date")
        
    def _valid_date (self, year:int, month:int, day:int ) -> bool:
        return self._valid_day_number(year,month,day) and month <= 12

    def _validate_day_number (self,year: int, month:int, day:int) -> bool:
        if month == 2:
            return self._leap_year(year,day)
        elif month in (4,6,9,11):
            return day < 31
        else:
            return day <= 31
        
    def _leap_year (year:int, day:int) -> bool:
        if year % 4 > 0:
            return day < 29
        else:
            return day <= 29
                
    def __str__ (self) -> str:
        return f"{self.year}-{self.month}-{self.day}"


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


class SnipeItLicense (SnipeIt):
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

    def _put (self, api_endpoint:str, payload:dict[Any]) -> Response:
        url = self._api_url(api_endpoint)
        return put(url, headers=headers, json=payload)

    def _post (self, api_endpoint:str, payload:dict[Any]) -> Response:
        url = self._api_url(api_endpoint)
        return post(url,headers=headers,json=payload)
        
    #Start Asset API Functions
    def get_all_assets (self) -> List[SnipeItAsset]:
        assets:List[SnipeItAsset] = []
        rows:List[dict[str,Any]] = []
        # get total number of assets:
        number_of_assets:int = self._get("/hardware?limit=1").json()["total"]
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
            
    def checkin_asset (
        self,
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

        response = self._post(url,payload)
        if response.status_code == 200:
            if "status" in response.json():
                return Failure(response.text)
            else:
                return Success(None)
        else:
            return Failure(f"status code: {response.status_code}")

    def audit_asset (
        self,
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
        response = self._post(url,payload)
        if response.status_code == 200:
            if "status" in response.json():
                return Failure(response.text)
            else:
                return Success(None)
        else:
            return Failure(f"status code:{response.status_code}")

    def restore_asset (self, id:int) -> None:
        url = f"/hardware/{id}/restore"
        self._post(url,None)

    def list_audit_due_assets (self) -> List[SnipeItAsset]:
        url = "/hardware/audit/due"
        audit_due:List[SnipeItAsset] = []
        request = self._get(url)
        for json_asset in request.json()["rows"]:
            audit_due.append(SnipeItAsset().from_json(json_asset))
        return audit_due

    def list_overdue_assets (self) -> List[SnipeItAsset]:
        url = "/hardware/audit/overdue"
        overdue:List[SnipeItAsset] = []
        request = self._get(url)
        for json_asset in request.json()["rows"]:
            overdue.append(SnipeItAsset().from_json(json_asset))
        return overdue

    def list_asset_licences (self, id:int) -> Result[List[SnipeItLicense],str]:
        url = f"/hardware/{id}/licenses"
        request = self._get(url)
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
    #Start User API Functions
    def get_users (self, 
        fuzzy_search:Optional[str]=None,
        first_name:Optional[str]=None,
        last_name:Optional[str]=None,
        user_name:Optional[str]=None,
        email:Optional[str]=None,
        employee_number:Optional[str]=None,
        state:Optional[str]=None,
        zip:Optional[str]=None,
        country:Optional[str]=None,
        group_id:Optional[int]=None,
        department_id:Optional[int]=None,
        company_id:Optional[int]=None,
        location_id:Optional[int]=None,
        deleted:bool=False, #set to True if you want *ONLY* deleted users
        all:bool=False, #ser to True if you want *BOTH* deleted and active users
        assets_count:Optional[int]=None,
        license_count:Optional[int]=None,
        accessories_count:Optional[int]=None,
        consumables_count:Optional[int]=None,
        remote:Optional[bool]=None, #set to filter against whether user is remote (WFH) or not
        vip:Optional[bool]=None,
        start_date:Optional[SnipeItDate]=None,
        end_date:Optional[SnipeItDate]=None
    ) -> List[SnipeItUser]:
        query = ["?"]
        url = "/users"
        number_of_users:int = self._get(f"{url}?limit=1").json()["total"]
        users:List[SnipeItUser] = []
        if fuzzy_search:
            query.append(f"search={fuzzy_search}")
        if first_name:
            query.append(f"first_name={first_name}")
        if last_name:
            query.append(f"last_name={last_name}")
        if user_name:
            query.append(f"user_name={user_name}")
        if email:
            query.append(f"email={email}")
        if employee_number:
            query.append(f"employee_num={employee_number})
        if state:
            qery.append(f"state={state}")
        if zip:
            query.append(f"zip={zip}")
        if country:
            query.append(f"country={country}")
        if group_id:
            query.append(f"group_id={group_id}")
        if department_id:
            query.append(f"department_id={department_id}")
        if company_id:
            query.append(f"company_id={company_id}")
        if location_id:
            query.append(f"location_id={location_id})
        if deleted:
            query.append("deleted=true")
        if all:
            query.append("all=true")
        if assets_count:
            query.append(f"assets_count={assets_count}")
        if license_count:
            query.append(f"license_count={license_count}")
        if accesories_count:
            query.append(f"accessories_count={accessories_count}")
        if consumables_count:
            query.append(f"consumables_count={consumables_count}")
        if remote != None:
            query.append(f"remote={str(remote).lower()}")
        if vip != None:
            query.append(f"vip={str(vip).lower()}")
        if start_date:
            query.append(f"start_date={str(start_date)}")
        if end_date:
            query.append(f"end_date={str(end_date)}")
        url += '&'.join(query) if len(query) > 1 else ''
        if number_of_users > 50:
            pass
        else:
            request = self._get(url)
            if request.status_code == 200:
                for row in request.json()["rows"]:
                    users.append(SnipeItUser().from_json(row))
                return Success(users)
            else:
                return Failure(request.status_code)
            