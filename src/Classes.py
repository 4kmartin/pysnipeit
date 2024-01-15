from __future__ import annotations

from requests import get, Response, delete, put, post
from typing import Any, Self, List
from returns.result import Result, Success, Failure

import json


class SnipeItDate:

    def __init__(self, year: int, month: int, day: int) -> None:
        self.year = year
        self.month = month
        self.day = day

    def __new__(cls, year: int, month: int, day: int) -> Result[None, str]:
        if cls._valid_date(year, month, day):
            cls(year, month, day)
            return Success(super().__new__(cls))
        else:
            return Failure(f"{year}-{month}-{day} is not a valid date")

    @classmethod
    def _valid_date(cls, year: int, month: int, day: int) -> bool:
        return cls._valid_day_number(year, month, day) and month <= 12

    @classmethod
    def _valid_day_number(cls, year: int, month: int, day: int) -> bool:
        if month == 2:
            return cls._leap_year(year, day)
        elif month in (4, 6, 9, 11):
            return day < 31
        else:
            return day <= 31

    @staticmethod
    def _leap_year(year: int, day: int) -> bool:
        if year % 4 > 0:
            return day < 29
        else:
            return day <= 29

    def __str__(self) -> str:
        return f"{self.year}-{self.month}-{self.day}"


class SnipeIt:

    @classmethod
    def from_json(cls, json_data: dict) -> Self:
        return cls(**json.loads(json.dumps(json_data)))

    def into_json(self) -> dict:
        return json.dumps(self.__dict__)


class SnipeItAsset(SnipeIt):

    def __init__(self,
                 asset_id: int,
                 name: str,
                 asset_tag: str,
                 serial: str,
                 model: str,
                 model_number: str,
                 eol: SnipeItDate,
                 status_label: str,
                 category: str,
                 manufacturer: str,
                 supplier: str,
                 notes: str,
                 order_number: str,
                 company: str,
                 location: str,
                 rtd_location: str,
                 image: str,
                 qr: str,
                 alt_barcode: str,
                 assigned_to: str,
                 warranty_months: int,
                 warranty_expires: SnipeItDate,
                 created_at: SnipeItDate,
                 updated_at: SnipeItDate,
                 last_audit_date: SnipeItDate,
                 next_audit_date: SnipeItDate,
                 deleted_at: SnipeItDate,
                 purchase_date: SnipeItDate,
                 age: int,
                 last_checkout: SnipeItDate,
                 expected_checkin: SnipeItDate,
                 purchase_cost: int,
                 checkin_counter: int,
                 checkout_counter: int,
                 requests_counter: int,
                 user_can_checkout: bool,
                 custom_fields: dict[str, Any],
                 available_actions: dict[str, bool],
                 ) -> None:
        self.id: int = asset_id
        self.name = name
        self.asset_tag = asset_tag
        self.serial = serial
        self.model = model
        self.model_number = model_number
        self.eol = eol
        self.status_label = status_label
        self.category = category
        self.manufacturer = manufacturer
        self.supplier = supplier
        self.notes = notes
        self.order_number = order_number
        self.company = company
        self.location = location
        self.rtd_location = rtd_location
        self.image = image
        self.qr = qr
        self.alt_barcode = alt_barcode
        self.assigned_to = assigned_to
        self.warranty_months = warranty_months
        self.warranty_expires = warranty_expires
        self.created_at = created_at
        self.updated_at = updated_at
        self.last_audit_date = last_audit_date
        self.next_audit_date = next_audit_date
        self.deleted_at = deleted_at
        self.purchase_date = purchase_date
        self.age = age
        self.last_checkout = last_checkout
        self.expected_checkin = expected_checkin
        self.purchase_cost = purchase_cost
        self.checkin_counter = checkin_counter
        self.checkout_counter = checkout_counter
        self.requests_counter = requests_counter
        self.user_can_checkout = user_can_checkout
        self.custom_fields = custom_fields
        self.available_actions = available_actions


class SnipeItUser(SnipeIt):

    def __init__(self,
                 id: int,
                 avatar: str,
                 name: str,
                 first_name: str,
                 last_name: str,
                 username: str,
                 remote: bool,
                 locale: str,
                 employee_num: str,
                 manager: SnipeItUser,
                 jobtitle: str,
                 vip: bool,
                 phone: str,
                 website: str,
                 address: str,
                 city: str,
                 state: str,
                 country: str,
                 zip: str,
                 email: str,
                 department: SnipeItDepartment,
                 location: SnipeItLocation,
                 notes: str,
                 permissions: dict[str, bool],
                 activated: bool,
                 autoassign_licenses: bool,
                 ldap_import: bool,
                 two_factor_enrolled: bool,
                 two_factor_optin: bool,
                 assets_count: int,
                 licenses_count: int,
                 accessories_count: int,
                 consumables_count: int,
                 company: SnipeItCompany,
                 created_by: SnipeItUser,
                 created_at: SnipeItDate,
                 updated_at: SnipeItDate,
                 start_date: SnipeItDate,
                 end_date: SnipeItDate,
                 last_login: SnipeItDate,
                 deleted_at: SnipeItDate,
                 available_actions: dict[str, bool],
                 groups: List[SnipeItGroup]
                 ) -> None:
        self.id = id
        self.name = name
        self.avatar = avatar
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.remote = remote
        self.locale = locale
        self.employee_num = employee_num
        self.manager = manager
        self.jobtitle = jobtitle
        self.vip = vip
        self.phone = phone
        self.website = website
        self.address = address
        self.city = city
        self.state = state
        self.country = country
        self.zip = zip
        self.email = email
        self.department = department
        self.location = location
        self.notes = notes
        self.permissions = permissions
        self.activated = activated
        self.auto_assign_licenses = autoassign_licenses
        self.ldap_import = ldap_import
        self.two_factor_enrolled = two_factor_enrolled
        self.two_factor_optin = two_factor_optin
        self.asset_count = assets_count
        self.license_count = licenses_count
        self.accessories_count = accessories_count
        self.consumables_count = consumables_count
        self.company = company
        self.created_by = created_by
        self.created_at = created_at
        self.updated_at = updated_at
        self.start_date = start_date
        self.end_date = end_date
        self.last_login = last_login
        self.deleted_at = deleted_at
        self.available_actions = available_actions
        self.groups = groups


class SnipeItAccessory(SnipeIt):
    pass


class SnipeItConsumable(SnipeIt):
    pass


class SnipeItComponent(SnipeIt):
    pass


class SnipeItKit(SnipeIt):
    pass


class SnipeItCompany(SnipeIt):
    pass


class SnipeItLocation(SnipeIt):
    pass


class SnipeItStatusLabel(SnipeIt):
    pass


class SnipeItCategory(SnipeIt):
    pass


class SnipeItManufacturer(SnipeIt):
    pass


class SnipeItSupplier(SnipeIt):
    pass


class SnipeItAssetMaintenance(SnipeIt):
    pass


class SnipeItDepartment(SnipeIt):
    pass


class SnipeItGroup(SnipeIt):
    pass


class SnipeItSettings(SnipeIt):
    pass


class SnipeItReports(SnipeIt):
    pass


class SnipeItConnection:
    def __init__(self) -> None:
        self.headers = {}
        self.url = ""

    def connect(self, snipe_it_url: str, personal_access_token: str, validate: bool = False) -> None:
        self.headers = {
            "Accept": "application/json",
            "Content-type": "application/json",
            "Authorization": f"Bearer {personal_access_token}",
        }

        self.url = f"{snipe_it_url}/api/v1"

        if validate:
            test = get(f"{self.url}/hardware?limit=1,", headers=self.headers).status_code
            if test == 200:
                print("connection successful")
            elif test == 401:
                print("An Error has Occurred! Unauthenticated")
                # quit()
            else:
                print(f"Connection failed for unknown reasons.\nstatus code: {test}\nAborting.")
                # quit()

    def _api_url(self, api_endpoint: str) -> str:
        if api_endpoint[0] != '/':
            api_endpoint = f"/{api_endpoint}"
        return f"{self.url}{api_endpoint}"

    def get(self, api_endpoint: str) -> Response:
        url = self._api_url(api_endpoint)
        print(url)
        return get(url, headers=self.headers)

    def paginated_request(self, api_endpoint: str, limit: int, offset: int) -> Response:
        url = f"{api_endpoint}?limit={limit}&offset={offset}&sort=id&order=asc"
        return self.get(url)

    def delete(self, api_endpoint: str) -> Response:
        url = self._api_url(api_endpoint)
        return delete(url, headers=self.headers)

    def put(self, api_endpoint: str, payload: dict[Any]) -> Response:
        url = self._api_url(api_endpoint)
        return put(url, headers=self.headers, json=payload)

    def post(self, api_endpoint: str, payload: dict[Any]) -> Response:
        url = self._api_url(api_endpoint)
        return post(url, headers=self.headers, json=payload)


def return_none_from_response(response: Response) -> Result[None, str]:
    if response.status_code == 200:
        if "status" in response.json():
            return Failure(response.text)
        else:
            return Success(None)
    else:
        return Failure(f"status code: {response.status_code}")
