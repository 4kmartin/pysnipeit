from typing import Optional, List, Any

from requests import Response
from returns.result import Result, Success, Failure

from src.Classes import SnipeItAsset, SnipeItConnection, SnipeItDate


# Start Asset API Functions
def get_all_assets(connection: SnipeItConnection) -> List[SnipeItAsset]:
    assets: List[SnipeItAsset] = []
    rows: List[dict[str, Any]] = []
    # get total number of assets:
    number_of_assets: int = connection.get("/hardware?limit=1").json()["total"]
    if number_of_assets > 50:
        offset = 0
        limit = 50
        while offset < number_of_assets:
            response = connection.paginated_request("/hardware", limit, offset)
            rows += response.json()["rows"]
            offset += limit
    else:
        rows += connection.get(f"{connection.url}/hardware").json()["rows"]
    for json_asset in rows:
        assets.append(SnipeItAsset.from_json(json_asset))
    return assets


def get_asset_by_id(connection: SnipeItConnection, asset_id: int) -> Result[SnipeItAsset, str]:
    result = connection.get(f"/hardware/{asset_id}")
    return _asset_result(result)


def _asset_result(result: Response) -> Result[SnipeItAsset, str]:
    if result.status_code == 200:
        if "status" not in result.json():
            return Success(SnipeItAsset.from_json(result.json()))
        else:
            return Failure(result.json()["messages"])
    else:
        return Failure(f"status code: {result.status_code}")


def get_asset_by_tag(connection: SnipeItConnection, asset_tag: str) -> Result[SnipeItAsset, str]:
    result = connection.get(f"/hardware/bytag/{asset_tag}")
    return _asset_result(result)


def get_asset_by_serial(connection: SnipeItConnection, serial: str) -> Result[SnipeItAsset, str]:
    result = connection.get(f"/hardware/byserial/{serial}")
    return _asset_result(result)


def delete_asset(connection: SnipeItConnection, asset_id: int) -> None:
    connection.delete(f"/hardware/{asset_id}")


def update_asset(connection: SnipeItConnection, asset_id: int, asset: SnipeItAsset) -> Result[None, str]:
    url = f"/hardware/{asset_id}"
    payload = asset.into_json()
    # noinspection PyTypeChecker
    response = connection.put(url, payload)
    if response.status_code == 200:
        if "status" in response.json():
            return Failure(str(response.json()["messages"]))
        else:
            return Success(None)
    else:
        return Failure(f"status code: {response.status_code}")


def checkout_asset(
        connection, asset_id: int,
        status_id: int,
        checkout_to_type: str,
        assigned_id: int,
        expected_checkin: Optional[str] = None,
        checkout_at: Optional[str] = None,
        name: Optional[str] = None,
        note: Optional[str] = None
) -> Result[None, str]:
    url = f"/hardware/{asset_id}/checkout"
    payload = {
        "status_id": status_id,
        "checkout_to_type": checkout_to_type,
    }
    match checkout_to_type:
        case "user":
            payload["assigned_user"] = assigned_id
        case "location":
            payload["assigned_location"] = assigned_id
        case "asset":
            payload["assigned_asset"] = assigned_id
        case _:
            return Failure(f"unknown value for checkout_to_type: {checkout_to_type}")
    if expected_checkin:
        payload["expected_checkin"] = expected_checkin
    if checkout_at:
        payload["checkout_at"] = checkout_at
    if name:
        payload["name"] = name
    if note:
        payload["note"] = note

    response = connection.post(url, payload)
    if response.status_code == 200:
        if "status" in response.json():
            return Failure(response.text)
        else:
            return Success(None)
    else:
        return Failure(f"status code: {response.status_code}")


def checkin_asset(
        connection,
        asset_id: int,
        status_id: int,
        name: Optional[str] = None,
        note: Optional[str] = None,
        location_id: Optional[str] = None
) -> Result[None, str]:
    url = f"/hardware/{asset_id}/checkin"
    payload = {
        "status_id": status_id,
    }

    if name:
        payload["name"] = name
    if note:
        payload["note"] = note
    if location_id:
        payload["location_id"] = location_id

    response = connection.post(url, payload)
    if response.status_code == 200:
        if "status" in response.json():
            return Failure(response.text)
        else:
            return Success(None)
    else:
        return Failure(f"status code: {response.status_code}")


def audit_asset(
        connection,
        asset_tag: str,
        location_id: Optional[int] = None,
        next_audit_date: Optional[SnipeItDate] = None
) -> Result[None, str]:
    url = "/hardware/audit"
    payload = {
        "asset_tag": asset_tag
    }
    if location_id:
        payload["location_id"] = location_id
    if next_audit_date:
        payload["next_audit_date"] = str(next_audit_date)
    response = connection.post(url, payload)
    if response.status_code == 200:
        if "status" in response.json():
            return Failure(response.text)
        else:
            return Success(None)
    else:
        return Failure(f"status code:{response.status_code}")


def restore_asset(connection: SnipeItConnection, asset_id: int) -> None:
    url = f"/hardware/{asset_id}/restore"
    payload = {}
    # noinspection PyTypeChecker
    connection.post(url, payload)


def list_audit_due_assets(connection: SnipeItConnection) -> List[SnipeItAsset]:
    url = "/hardware/audit/due"
    audit_due: List[SnipeItAsset] = []
    request = connection.get(url)
    for json_asset in request.json()["rows"]:
        audit_due.append(SnipeItAsset.from_json(json_asset))
    return audit_due


def list_overdue_assets(connection: SnipeItConnection) -> List[SnipeItAsset]:
    url = "/hardware/audit/overdue"
    overdue: List[SnipeItAsset] = []
    request = connection.get(url)
    for json_asset in request.json()["rows"]:
        overdue.append(SnipeItAsset.from_json(json_asset))
    return overdue


def get_user_assets(connection: SnipeItConnection, user_id: int) -> Result[List[SnipeItAsset], str]:
    url = f"/users/{user_id}/assets"
    response = connection.get(url)
    assets = []
    if response.status_code == 200:
        for json in response.json()["rows"]:
            assets.append(SnipeItAsset.from_json(json))
        return Success(assets)
    else:
        return Failure(f"status code: {response.status_code}")
