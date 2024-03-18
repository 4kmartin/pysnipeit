from typing import Optional, List, Any

from requests import Response
from returns.result import Result, Success, Failure

from .Classes import SnipeItAsset, SnipeItConnection, SnipeItDate


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
            if result.json()["total"] == 1:
                return Success(SnipeItAsset.from_json(result.json()["rows"][0]))
            else:
                return Failure(f"Query returns {result.json()['total']} assets. Expected 1")
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


def get_audit_due_assets(connection: SnipeItConnection) -> List[SnipeItAsset]:
    url = "/hardware/audit/due"
    audit_due: List[SnipeItAsset] = []
    request = connection.get(url)
    for json_asset in request.json()["rows"]:
        audit_due.append(SnipeItAsset.from_json(json_asset))
    return audit_due


def get_overdue_assets(connection: SnipeItConnection) -> List[SnipeItAsset]:
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


def update_custom_field(connection: SnipeItConnection,
                        asset_id: int, db_field_name: str,
                        value: Any) -> Result[None, str]:
    url = f"/hardware/{asset_id}"
    payload = {
        db_field_name: value
    }

    response = connection.patch(url, payload)
    if response.status_code == 200 and response.json()["status"] == "success":
        return Success(None)
    else:
        return Failure(f"status code: {response.status_code}\n{response.text}")


def create_new_asset( 
                    connection: SnipeItConnection, 
                    asset_tag: Optional[str], # if auto_incement is on then this can be set to None otherwise it *must* have a value
                    status_id: int, 
                    model_id: int, 
                    name: Optional[str] = None, 
                    image: Optional[str] = None, 
                    serial: Optional[str] = None, 
                    purchase_date: Optional[SnipeItDate] = None,
                    purchase_cost: Optional[float] = None,
                    order_number: Optional[str] = None,
                    notes: Optional[str] = None,
                    archived: Optional[str] = None,
                    warranty_months: Optional[int] = None,
                    depreciate: bool = False,
                    supplier_id: Optional[int] = None,
                    requestable: bool = False,
                    rtd_location_id: Optional[int] = None, # The corresponding location_id from a location in the locations table that should indicate where the item is when it's *NOT* checked out to someone
                    last_audit_date: Optional[SnipeItDate] = None,
                    location_id: Optional[int] = None,
                    byod: bool = False
                    ) -> Result[SnipeItAsset,str]:
    payload = {
        "status_id": status_id,
        "model_id": model_id,
    }
    if asset_tag:
        payload["asset_tag"] = asset_tag
    if name:
        payload["name"] = name
    if image:
        payload["image"] = image
    if serial:
        payload["serial"] = serial
    if purchase_date:
        payload["purchase_date"] = purchase_date
    if purchase_cost:
        payload["purchase_cost"] = purchase_cost
    if order_number:
        payload["order_number"] = order_number
    if notes:
        payload["notes"] = notes
    if archived:
        payload["archived"] = archived
    if warranty_months:
        payload["warranty_months"] = warranty_months
    if depreciate:
        payload["depreciate"] = depreciate
    if supplier_id:
        payload["supplier_id"] = supplier_id
    if requestable:
        payload["requestable"] = requestable
    if rtd_location_id:
        payload["rtd_location_id"] = rtd_location_id
    if last_audit_date:
        payload["last_audit_date"] = last_audit_date
    if location_id:
        payload["location_id"] = location_id
    if byod:
        payload["byod"]
    resposnse = connection.post("/hardware", payload)
    if resposnse.json()["status"] == "success":
        return Success(SnipeItAsset.from_json(resposnse.json["payload"]))
    else:
        return Failure(f"response: {resposnse.status_code}\nreason: {resposnse.json()['status']}")