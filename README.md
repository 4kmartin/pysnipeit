pySnipeIt is a wrapper for [Snipe-It](https://snipeitapp.com/)'s REST API. It aims to have 1:1 compatibility with that api.

# Implementation Progress

- [x] Assets
- [ ] Custom Fields and Fieldsets
- [ ] Companies
- [ ] Locations
- [ ] Accessories
- [ ] Consumables
- [ ] Components
- [x] Users
- [ ] Status Labels
- [ ] Models
- [ ] Licenses
- [ ] Categories
- [ ] Manufacturers
- [ ] Suppliers
- [ ] Asset Maintenances
- [ ] Departments
- [ ] Groups
- [ ] Settings
- [ ] Reports

# Examples 

to get a user by their ID:

```python
from pysnipeit import SnipeItConnection, get_user_by_id
from returns.result import Success,Failure
from dotenv import dotenv_values

secrets = dotenv_values('.env')

conn = SnipeItConnection()
conn.connect(secrets['URL'],secrets['API'])

user = get_user_by_id(conn, 1)
match user:
    case Success(usr):
        print(usr.name)
    case Failure(why):
        print(f"This attempt failed to get a User\n{why}")
```