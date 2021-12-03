import requests
import pytest
import random
import string
import uuid

def randStr(chars = string.ascii_lowercase + string.digits, N=10):
	return ''.join(random.choice(chars) for _ in range(N))

@pytest.mark.parametrize("uuid,status", [('d13b0252-9f8f-472e-8700-546a8333d9de', True),
                                         ('3fa85f64-5711-4562-b3fc-2c963f66afa6',False)])
def test_unl_leverage(uuid,status):
    base_uri = 'https://ntapi-core-rke.test.env/api'
    url = f"{base_uri}/users/{uuid}/check_unlim_leverage/"

    response = requests.request("GET", url, verify=False,
                                cert=("/Users/marlonrocha/Documents/cert_key/core-solutions.exness.test.crt",
                                      "/Users/marlonrocha/Documents/cert_key/core-solutions.exness.test.key"))

    assert response.status_code == 200

    response = response.json()

    assert response['unlimited_leverage'] == status

def test_create_new_user():
    base_uri = 'https://ntapi-core-rke.test.env/api'
    url = f"{base_uri}/users/"

    payload={
        "user_uid": uuid.uuid1(),
        "status": "ACTIVE",
        "risk_level": "100",
        "is_swap_free": True,
        "language": "st",
        "location": "AW"
    } 
    

    response = requests.request("POST", url, data=payload, verify=False,
                                cert=("core-solutions.exness.test.crt", "core-solutions.exness.test.key"))

    assert response.status_code == 200

    url = f"{base_uri}/users/{payload['user_uid']}/check_unlim_leverage/"

    response = requests.request("GET", url, verify=False,
                                cert=("core-solutions.exness.test.crt", "core-solutions.exness.test.key"))

    assert response.status_code == 200

    response = response.json()

    assert response['unlimited_leverage'] == False
    