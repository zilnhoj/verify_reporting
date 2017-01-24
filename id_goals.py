import requests
import json


def get_goals_ids():

    protocol = 'https'
    domain = 'analytics.ida.digital.cabinet-office.gov.uk'
    path = 'index.php'
    url_template = '{}://{}/{}'
    url = url_template.format(protocol, domain, path)
    with open("../creds/piwik_token.json") as ft:
    	token = json.load(ft)

    token = token['token']

    qs = {
        'module': 'API',
        'method': 'Goals.getGoals',
        'idSite': '1',
        'period': 'range',
        # 'date': '{},{}'.format(start_date,end_date), # TODO: Update this for the required Date Range
        # 'date': date,# TODO: Update this for the required Date Range
        'format': 'json',
        'token_auth': token,
    }
    results = {}

    response = requests.get(url, qs)
    raw_result = response.json()

    return raw_result
