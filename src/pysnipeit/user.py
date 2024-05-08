from .Classes import SnipeItUser, SnipeItConnection, SnipeItDate, return_none_from_response
from typing import Optional, List
from returns.result import Result, Success, Failure


# Start User API Functions
def get_users(connection: SnipeItConnection,
              fuzzy_search: Optional[str] = None,
              first_name: Optional[str] = None,
              last_name: Optional[str] = None,
              user_name: Optional[str] = None,
              email: Optional[str] = None,
              employee_number: Optional[str] = None,
              state: Optional[str] = None,
              zip_code: Optional[str] = None,
              country: Optional[str] = None,
              group_id: Optional[int] = None,
              department_id: Optional[int] = None,
              company_id: Optional[int] = None,
              location_id: Optional[int] = None,
              deleted: bool = False,  # set to True if you want *ONLY* deleted users
              all_users: bool = False,  # ser to True if you want *BOTH* deleted and active users
              assets_count: Optional[int] = None,
              license_count: Optional[int] = None,
              accessories_count: Optional[int] = None,
              consumables_count: Optional[int] = None,
              remote: Optional[bool] = None,  # set to filter against whether user is remote (WFH) or not
              vip: Optional[bool] = None,
              start_date: Optional[SnipeItDate] = None,
              end_date: Optional[SnipeItDate] = None
              ) -> Result[List[SnipeItUser], str]:
    query = ["?"]
    url = "/users"
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
        query.append(f"employee_num={employee_number}")
    if state:
        query.append(f"state={state}")
    if zip_code:
        query.append(f"zip={zip_code}")
    if country:
        query.append(f"country={country}")
    if group_id:
        query.append(f"group_id={group_id}")
    if department_id:
        query.append(f"department_id={department_id}")
    if company_id:
        query.append(f"company_id={company_id}")
    if location_id:
        query.append(f"location_id={location_id}")
    if deleted:
        query.append("deleted=true")
    if all_users:
        query.append("all=true")
    if assets_count:
        query.append(f"assets_count={assets_count}")
    if license_count:
        query.append(f"license_count={license_count}")
    if accessories_count:
        query.append(f"accessories_count={accessories_count}")
    if consumables_count:
        query.append(f"consumables_count={consumables_count}")
    if remote is not None:
        query.append(f"remote={str(remote).lower()}")
    if vip is not None:
        query.append(f"vip={str(vip).lower()}")
    if start_date:
        query.append(f"start_date={str(start_date)}")
    if end_date:
        query.append(f"end_date={str(end_date)}")
    url += '&'.join(query) if len(query) > 1 else ''
    test = connection.get(f"{url}?limit=1")
    if test.status_code != 200:
        return Failure(test.json())
    number_of_users: int = test.json()["total"]
    users: List[SnipeItUser] = []
    if number_of_users > 50:
        offset = 0
        limit = 50
        rows = []
        while offset < number_of_users:
            rows += connection.paginated_request(url, limit, offset).json()["rows"]
            offset += limit
    else:
        rows = connection.get(url).json()["rows"]
    for row in rows:
        users.append(SnipeItUser.from_json(row))
    return Success(users)


def create_new_user(
        connection: SnipeItConnection,
        first_name: str,
        username: str,
        password: str,
        confirm_password: str,
        last_name: Optional[str] = None,
        email: Optional[str] = None,
        permissions: Optional[str] = None,
        activated: bool = False,
        phone: Optional[str] = None,
        jobtitle: Optional[str] = None,
        manager_id: Optional[int] = None,
        employee_number: Optional[str] = None,
        notes: Optional[str] = None,
        company_id: Optional[int] = None,
        two_factor_enrolled: bool = False,
        two_factor_optin: bool = False,
        department_id: Optional[int] = None,
        location_id: Optional[int] = None,
        remote: bool = False,
        groups: Optional[List[int]] = None,
        vip: bool = False,
        start_date: Optional[SnipeItDate] = None,
        end_date: Optional[SnipeItDate] = None
) -> Result[SnipeItUser, str]:
    url = "/users"
    payload = {
        "first_name": first_name,
        "username": username,
        "password": password,
        "password_confirmation": confirm_password,
    }

    if last_name:
        payload["last_name"] = last_name
    if email:
        payload["email"] = email
    if permissions:
        payload["permissions"] = permissions
    if activated:
        payload["activated"] = "true"
    if phone:
        payload["phone"] = phone
    if jobtitle:
        payload["jobtitle"] = jobtitle
    if manager_id:
        payload["manager_id"] = manager_id
    if employee_number:
        payload["employee_num"] = employee_number
    if notes:
        payload["notes"] = notes
    if company_id:
        payload["company_id"] = company_id
    if two_factor_enrolled:
        payload["two_factor_enrolled"] = two_factor_enrolled
    if two_factor_optin:
        payload["two_factor_optin"] = two_factor_optin
    if department_id:
        payload["department_id"] = department_id
    if location_id:
        payload["location_id"] = location_id
    if remote:
        payload["remote"] = "true"
    if groups:
        payload["groups"] = groups
    if vip:
        payload["vip"] = "true"
    if start_date:
        payload["start_date"] = str(start_date)
    if end_date:
        payload["end_date"] = str(end_date)

    response = connection.post(url, payload)
    if response.status_code == 200:
        if response.json()["status"] == "error":
            return Failure(response.json())
        return Success(SnipeItUser.from_json(response.json()["payload"]))
    else:
        return Failure({"user_name":username, "response": response.json()})


def get_user_by_id(connection: SnipeItConnection, user_id: int) -> Result[SnipeItUser, str]:
    url = f"/users/{user_id}"
    response = connection.get(url)
    if response.status_code == 200:
        return Success(SnipeItUser.from_json(response.json()))
    else:
        return Failure(f"status code: {response.status_code}")


def update_user_details(
        connection: SnipeItConnection,
        user: SnipeItUser
) -> Result[None, str]:
    url = f"/users/{user.id}"
    response = connection.put(url, user.into_json())
    return return_none_from_response(response)


def delete_user(connection: SnipeItConnection, user_id: int) -> Result[None, str]:
    url = f"/users/{user_id}"
    response = connection.delete(url)
    return return_none_from_response(response)


def restore_user(connection: SnipeItConnection, user_id: int) -> Result[None, str]:
    url = f"/users/{user_id}/restore"
    response = connection.post(url, {})
    return return_none_from_response(response)


def whoami(connection: SnipeItConnection) -> SnipeItUser:
    url = "/users/me"
    response = connection.get(url)
    return SnipeItUser.from_json(response.json())

def get_user_id(connection: SnipeItConnection, first_name: str, last_name: str) -> Result[int,str]:
    match get_users(connection, first_name=first_name,last_name=last_name):
        case Failure(why):
            return Failure(why)
        case Success(user_list):
            if len(user_list) == 0:
                return Failure(f"could not find a user named: {first_name} {last_name}")
            if len(user_list) > 1:
                return Failure(f"Not enough information to identify a specific user: {first_name} {last_name}")
            return Success(user_list[0].id)
            