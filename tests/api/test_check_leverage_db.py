from clickhouse_driver import Client
import requests
import pytest

def test_unl_leverage_in_db(secret):
    client = Client('clickhouse-datahub.test.env',
            user='marlon_rocha',
            password=secret,
            compression=True)

    result = client.execute("""SELECT login
    FROM xdata.`.inner.view_order_mt4_stat` WHERE volume_lots >= 5 AND  orders_count >=10
    AND server_name == 'Real' LIMIT 10;""")

    result = [r[0] for r in result]
    accounts_list = ""
    for r in result:
        accounts_list += f"{r},"

    base_uri = 'https://ntapi-core-rke.test.env/api'
    url = f"{base_uri}/accounts/list/?accounts={accounts_list[:-1]}"

    response = requests.request("GET", url, verify=False,
                                    cert=("/Users/marlonrocha/Documents/cert_key/core-solutions.exness.test.crt", 
                                          "/Users/marlonrocha/Documents/cert_key/core-solutions.exness.test.key"))

    response = response.json()
    uuids = []
    for r in response['data']:
        uuids.append(r['user_uid'])


    for uuid in uuids:
        response = requests.request("GET", f"{base_uri}/users/{uuid}/check_unlim_leverage/",  verify=False,
                                    cert=("/Users/marlonrocha/Documents/cert_key/core-solutions.exness.test.crt", 
                                          "/Users/marlonrocha/Documents/cert_key/core-solutions.exness.test.key"))
        response = response.json()

        assert response['unlimited_leverage']
