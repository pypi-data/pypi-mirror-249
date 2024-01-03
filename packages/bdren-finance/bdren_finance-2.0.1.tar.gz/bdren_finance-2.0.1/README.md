### Setup

you need to add 3 variables in your settings.py file:

```python
# settings.py

BDREN_FINANCE_URL = 'https://finance.bdren.net.bd'
BDREN_FINANCE_AUTH_EMAIL = 'your_username'
BDREN_FINANCE_AUTH_PASSWORD = 'your_password'
```

### Usage

```python
from bdren_finance import get_accounts, create_entry

print(get_accounts(query='your_query'))

payload = {
    "transNo": "",
    "transDate": "2024-01-01",
    "entryDate": "2024-01-01",
    "generalParticular": "This is general Particular",
    "vouchers": [
        {
            "accountNo": 15600005,
            "accountName": "FDR with Jananta Bank -UGC Bhaban Branch",
            "drAmount": 100,
            "crAmount": 0,
            "particular": "Bank will be debited",
            "type": "dr"
        },
        {
            "accountNo": 55500700,
            "accountName": "Sub-Project Revenue - DUET",
            "drAmount": 0,
            "crAmount": 100,
            "particular": "The university will be credited ",
            "type": "cr"
        }
    ]
}

print(create_entry(payload))

```