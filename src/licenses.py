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


def _license_response(request: Response) -> Result[List[SnipeItLicense], str]:
    if request.status_code == 200:
        if "status" in request.json():
            return Failure(request.text)
        else:
            licenses: List[SnipeItLicense] = []
            for row in request.json()["rows"]:
                licenses.append(SnipeItLicense().from_json(row))
            return Success(licenses)
    else:
        return Failure(f"Status Code: {request.status_code}")
