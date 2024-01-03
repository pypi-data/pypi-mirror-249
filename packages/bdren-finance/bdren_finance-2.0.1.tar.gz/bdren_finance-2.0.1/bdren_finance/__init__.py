import json

import requests
from django.conf import settings

BASE_URL = settings.BDREN_FINANCE_URL


def finance_login_session():
    session = requests.Session()
    res = session.get(BASE_URL + 'csrf/')
    csrfToken = res.json()['csrfToken']

    login_data = {
        'email': settings.BDREN_FINANCE_AUTH_EMAIL,
        'password': settings.BDREN_FINANCE_AUTH_PASSWORD,
        'csrfmiddlewaretoken': csrfToken
    }

    headers = {
        'Referer': BASE_URL + 'login/',
        'X-CSRFToken': session.cookies['csrftoken']
    }

    login = session.post(BASE_URL + 'login/', data=login_data, headers=headers)

    if login.status_code != 200:
        raise Exception('Login failed to BdREN Finance')
    return session


def get_accounts(query: str, _type: str = "all", field: str = "no") -> dict:
    """
    Get accounts from BdREN Finance API
    :param query: Query string
    :param _type: all, parent, sub
    :param field: no, name
    :return: Dict
    """

    try:

        session = finance_login_session()

        url = BASE_URL + 'account/search/?q=' + query + '&type=' + _type + '&field=' + field
        res = session.get(url)
        session.close()
        return res.json()

    except Exception as e:
        raise Exception(e)


def create_entry(payload: dict) -> dict:
    """
    Create entry in BdREN Finance API
    :param payload: Dict :return:

    # example payload  = {
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
    """

    try:
        session = finance_login_session()

        headers = {
            'Referer': BASE_URL + 'entry/create/',
            'X-CSRFToken': session.cookies['csrftoken'],
            'Content-Type': 'application/json',
            'Accept': 'application/json, text/plain, */*',
        }

        json_payload = json.dumps(payload)

        response = session.post(BASE_URL + 'entry/create/', data=json_payload, headers=headers)
        session.close()
        return response.json()

    except Exception as e:
        raise Exception(e)
