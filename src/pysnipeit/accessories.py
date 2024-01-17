from .Classes import SnipeItConnection, SnipeItAccessory
from returns.result import Result, Success, Failure
from typing import List
from requests import Response


def get_user_accessories(connection: SnipeItConnection, user_id: int) -> Result[List[SnipeItAccessory], str]:
    url = f"/users/{user_id}/accessories"
    response = connection.get(url)
    return _accessories_result(response)


def _accessories_result(response: Response) -> Result[List[SnipeItAccessory], str]:
    if response.status_code == 200:
        if "status" in response.json():
            return Failure(response.text)
        else:
            licenses: List[SnipeItAccessory] = []
            for row in response.json()["rows"]:
                licenses.append(SnipeItAccessory.from_json(row))
            return Success(licenses)
    else:
        return Failure(f"Status Code: {response.status_code}")
