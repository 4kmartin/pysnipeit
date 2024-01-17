from __future__ import annotations

import random
import string
from subprocess import run
from typing import List, Optional, Callable
from pysnipeit import SnipeItConnection, SnipeItUser, get_users, create_new_user


class AdUser:
    def __init__(self,
                 name: str,
                 givenname: Optional[str],
                 surname: Optional[str],
                 samaccountname: str,
                 enabled: bool,
                 mail: Optional[str],
                 title: Optional[str],
                 department: Optional[str],
                 manager: Optional[str],
                 office: Optional[str],
                 streetaddress: Optional[str],
                 city: Optional[str],
                 state: Optional[str],
                 country: Optional[str],
                 postalcode: Optional[str]
                 ) -> None:
        self.name = name
        self.first_name = givenname
        self.last_name = surname
        self.user_name = samaccountname
        self.enabled = enabled
        self.email_address = mail
        self.job_title = title
        self.department = department
        self.manager = manager
        self.office = office
        self.street_address = streetaddress
        self.city = city
        self.state = state
        self.country = country
        self.zip_code = postalcode

    @classmethod
    def from_str(cls, string_values: str) -> AdUser:
        splits = list(map(lambda x: x.strip(), map(lambda x: x.split(":"), string_values.split("\n"))))
        keys = splits[::2]
        values = splits[1::2]
        properties = {keys[i]: values[i] for i in range(len(keys))}
        return cls(**properties)


def get_ad_users(filter_function: Callable[[AdUser], bool] = lambda x: True) -> List[AdUser]:
    """
        Produces a List of AdUsers. The filter function allows you to filter out unwanted users.
        for example if uou only want users where the username is first initial followed by lastname you might define
        this function:

        def filter_user_name (user:AdUser) -> bool:
            return user.user_name == f"{user.first_name[0]}{user.last_name}"
    
    """
    cmd = "get-aduser -filter * -properties * | select name, givenname, surname, samaccountname, enabled, mail, title, department, @{l=\"manager\";e={$_.manager.split(',')[0].split('=')[1]}}, office, streetaddress, city, state, country, postalcode"
    output = run(["powershell", "-command", cmd], capture_output=True).stdout.decode()
    users = []
    for user_properties in output.replace('\r', '').split('\n\n'):
        users.append(AdUser.from_str(user_properties))
    return list(filter(filter_function, users))


def get_users_not_in_snipe_it(ad_users: List[AdUser], snipeit_users: List[SnipeItUser]) -> List[AdUser]:
    snipeit = [user.user_name for user in snipeit_users]
    return [user for user in ad_users if user.name not in snipeit]


def add_missing_users_to_snipe_it(missing_users: List[AdUser], connection: SnipeItConnection) -> None:
    arbitrary_password = ''.join(random.choices(string.ascii_uppercase + string.digits, k=14))
    for user in missing_users:
        manager = get_users(connection, fuzzy_search=user.manager).id
        create_new_user(
            connection,
            user.first_name,
            user.user_name,
            arbitrary_password,
            arbitrary_password,
            last_name=user.last_name,
            jobtitle=user.job_title,
            manager_id=manager,
            email=user.email_address,
            department=user.department
        )


if __name__ == '__main__':
    url = "<URL HERE>"
    api = "<API TOKEN HERE>"
    conn = SnipeItConnection()
    conn.connect(url, api, True)
    add_missing_users_to_snipe_it(
        get_users_not_in_snipe_it(
            get_ad_users(),
            get_users(conn)
        ),
        conn
    )
