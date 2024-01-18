from __future__ import annotations

import random
import string

from subprocess import run
from typing import List, Optional, Callable
from pysnipeit import SnipeItConnection, SnipeItUser, get_users, create_new_user
from pysnipeit.user import get_user_id
from dotenv import dotenv_values
from returns.result import Success, Failure
from re import split


MANAGER_IDS = {}

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
        pattern = '(.+:.+\n[ ]+.+)|(.+:.+)'
        pairs = list(filter(lambda x: x is not None and x != '' and x != '\n',split(pattern,string_values)))
        try:    
            properties = {i.split(':')[0].strip():i.split(':')[1].strip() for i in pairs}
        except IndexError:
            print("Could not parse the following :")
            print(string_values.encode())
            quit(1)
        for (k,v) in properties.items():
            if v == '':
                properties[k] = None
        try:
            properties["enabled"] = bool(properties["enabled"])
        except KeyError:
            print(string_values,"\n\n\n",properties)
            quit(1)
        return cls(**properties)


def get_ad_users(filter_function: Callable[[AdUser], bool] = lambda x: True) -> List[AdUser]:
    """
        Produces a List of AdUsers. The filter function allows you to filter out unwanted users.
        for example if uou only want users where the username is first initial followed by lastname you might define
        this function:

        def filter_user_name (user:AdUser) -> bool:
            return user.user_name == f"{user.first_name[0]}{user.last_name}"
    
    """
    cmd = "get-aduser -filter * -properties * | select name, givenname, surname, samaccountname, enabled, mail, title, department, @{l='manager';e={$_.manager.split(',')[0].split('=')[1]}}, office, streetaddress, city, state, country, postalcode"
    output = run(["powershell", "-command", cmd], capture_output=True).stdout.decode()
    users = []
    for user_properties in output.replace('\r', '').split('\n\n')[1:]:
        if user_properties == '':
            continue
        users.append(AdUser.from_str(user_properties))
    return list(filter(filter_function, users))

def get_users_not_in_snipe_it(ad_users: List[AdUser], snipeit_users: List[SnipeItUser]) -> List[AdUser]:
    snipeit = [user.username.lower() for user in snipeit_users]
    return [user for user in ad_users if user.user_name.lower() not in snipeit]

def add_missing_users_to_snipe_it(missing_users: List[AdUser], connection: SnipeItConnection) -> None:
    manager = None
    arbitrary_password = ''.join(random.choices(string.ascii_uppercase + string.digits, k=19))
    for user in missing_users:
        if user.manager in MANAGER_IDS.keys():
            manager = MANAGER_IDS[user.manager]
        elif user.manager != None:
            match get_user_id(conn, user.manager.split()[0], user.manager.split()[1]):
                case Success(manager_id):
                    MANAGER_IDS[user.manager] = manager_id
                    manager = manager_id
                case _:
                    pass
        match create_new_user(
            connection,
            user.first_name,
            user.user_name,
            arbitrary_password,
            arbitrary_password,
            last_name=user.last_name,
            jobtitle=user.job_title,
            manager_id=manager,
            email=user.email_address,
        ):
            case Failure(why):
                print(f"Failed to create user ({user.user_name})\n{why}")
            case Success(_):
                print(f"created {user.user_name}")


if __name__ == '__main__':
    secrets = dotenv_values(".env")
    url = secrets["SNIPEIT_URL"]
    api = secrets["SNIPEIT_API"]
    
    conn = SnipeItConnection()
    conn.connect(url, api, True)
    
    print("Collecting AD Users")
    ad_users = get_ad_users(filter_script)
    # for user in ad_users:
        # print(f"\t{user.name}")
        
    print('Finding users not in SnipeIT')
    match get_users(conn):
        case Success(snipeit_users):
            delta = get_users_not_in_snipe_it(ad_users,snipeit_users)
            for user in delta:
                print(f"\t{user.user_name}")
            add = 'n'
            if len(delta) > 0:
                add = input("Do you want to add all of these users to Snipe-IT? (Y/n): ")
            if add.lower().strip() in ('', 'y', 'yes'): 
                print("adding users to snipe it")
                add_missing_users_to_snipe_it(delta,conn)
        case Failure(why):
            print(f"Could not get Snipe-It Users\n\nError: {why}")
            # print(conn._api_url("test"))
            # print(conn.url)
            quit(1)
    print("Process Completed")
