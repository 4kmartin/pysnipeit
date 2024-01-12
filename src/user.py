from Classes import Snipeit, SnipeItConnection, SnipeItDate
from typing import Optional, List, Any
from returns.result import Result, Success, Failure


class SnipeItUser (SnipeIt):
    pass


#Start User API Functions
def get_users (connection:SnipeItConnection, 
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
    number_of_users:int = connection._get(f"{url}?limit=1").json()["total"]
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
        request = connection._get(url)
        if request.status_code == 200:
            for row in request.json()["rows"]:
                users.append(SnipeItUser().from_json(row))
            return Success(users)
        else:
            return Failure(request.status_code)

