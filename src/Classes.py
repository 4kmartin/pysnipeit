from requests import get, Response, delete, put, post
from abc import ABC, abstractmethod
from typing import Any, Self
from returns.result import Result, Success, Failure


class SnipeItDate:
    def __init__ (self, year:int, month:int, day:int) -> Result[None,str]:
        if self._valid_date(year, month, day):
            self.day = day
            self.month = month
            self.year = year
            return Success(None)
        else:
            return Failure(f"{year}-{month}-{day} is not a valid date")

    def _valid_date (self, year:int, month:int, day:int ) -> bool:
        return self._valid_day_number(year,month,day) and month <= 12

    def _valid_day_number (self,year: int, month:int, day:int) -> bool:
        if month == 2:
            return self._leap_year(year,day)
        elif month in (4,6,9,11):
            return day < 31
        else:
            return day <= 31

    def _leap_year (self, year:int, day:int) -> bool:
        if year % 4 > 0:
            return day < 29
        else:
            return day <= 29

    def __str__ (self) -> str:
        return f"{self.year}-{self.month}-{self.day}"


class SnipeIt (ABC):

    @classmethod
    @abstractmethod
    def from_json(cls, json_data: dict) -> Self:
        pass

    @abstractmethod
    def into_json(self) -> dict:
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


class SnipeItStatusLabel (SnipeIt):
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


class SnipeItReports (SnipeIt):
    pass





class SnipeItConnection:
    def __init__(self) -> None:
        self.headers = {}
        self.url = ""

    def connect (self, snipe_it_url:str, personal_access_token:str, validate:bool=False) -> None:
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
                print("An Error has Occurred! Unauthenticated")
                quit()
            else:
                print("Connection failed for unknown reasons.\nAborting.")
                quit()

    def _api_url (self, api_endpoint:str) -> str:
        if api_endpoint[0] != '/':
            api_endpoint = f"/{api_endpoint}"
        return f"{self.url}{api_endpoint}"

    def get (self, api_endpoint:str) -> Response:
        url = self._api_url(api_endpoint)
        return get(url, headers=self.headers)

    def paginated_request (self, api_endpoint:str, limit:int, offset:int) -> Response:
        url = f"{api_endpoint}?limit={limit}&offset={offset}&sort=id&order=asc"
        return self.get(url)

    def delete (self, api_endpoint:str) -> Response:
        url = self._api_url(api_endpoint)
        return delete(url,headers=self.headers)

    def put (self, api_endpoint:str, payload:dict[Any]) -> Response:
        url = self._api_url(api_endpoint)
        return put(url, headers=self.headers, json=payload)

    def post (self, api_endpoint:str, payload:dict[Any]) -> Response:
        url = self._api_url(api_endpoint)
        return post(url,headers=self.headers,json=payload)


def return_none_from_response(response:Response) -> Result[None,str]:
    if response.status_code == 200:
        if "status" in response.json():
            return Failure(response.text)
        else:
            return Success(None)
    else:
        return Failure(f"status code: {response.status_code}")
