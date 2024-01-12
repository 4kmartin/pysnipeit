from Classes import SnipeItConnection, SnipeIt
from typing import List, Self
from returns.result import Result, Failure, Success
from requests import Response


class SnipeItLicense(SnipeIt):

    def into_json(self) -> dict:
        pass

    @classmethod
    def from_json(cls, json_data: dict) -> Self:
        pass

    def __init__(self) -> None:
        pass


def list_asset_licences(connection: SnipeItConnection, asset_id: int) -> Result[List[SnipeItLicense], str]:
    url = f"/hardware/{asset_id}/licenses"
    request = connection.get(url)
    return _license_response(request)


def _license_response(response: Response) -> Result[List[SnipeItLicense], str]:
    if response.status_code == 200:
        if "status" in response.json():
            return Failure(response.text)
        else:
            licenses: List[SnipeItLicense] = []
            for row in response.json()["rows"]:
                licenses.append(SnipeItLicense().from_json(row))
            return Success(licenses)
    else:
        return Failure(f"Status Code: {response.status_code}")

def get_user_licenses (connection:SnipeItConnection, user_id:int) -> Result[List[SnipeItLicense], str]:
    url = f"/users/{user_id}/licenses"
    request = connection.get(url)
    return _license_response(request)
