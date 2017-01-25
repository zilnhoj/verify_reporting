import pandas as pd
import requests
import json
import csv

# def get_piwik_data(start_date,end_date):
def get_rp_pages(date,pageTitle,rp):

    # Build the URL
    protocol = 'https'
    domain = 'analytics.ida.digital.cabinet-office.gov.uk'
    path = 'index.php'
    url_template = '{}://{}/{}'
    url = url_template.format(protocol, domain, path)
    with open("../creds/piwik_token.json") as ft:
        token = json.load(ft)

    token = token['token']

    # Build the query string
    qs = {
        'module': 'API',
        'method': 'Actions.get',
        'idSite': '1',
        'period': 'range',
        'segment': 'pageTitle=@{},customVariableValue1=={}'.format(pageTitle, rp),
        # 'date': '{},{}'.format(start_date,end_date), # TODO: Update this for the required Date Range
        'date': date,# TODO: Update this for the required Date Range
        'format': 'json',
        'token_auth': token,
    }
    response = requests.get(url,qs)
    raw_result = response.json()

    return raw_result['nb_uniq_pageviews']

# piwik_data = get_rp_pages('2017-01-01,2017-01-01','Success - REGISTER_WITH_IDP','DWP UCDS')
# piwik_data = get_piwik_data()

def get_goal_results(date,goalid,rp):
    protocol = 'https'
    domain = 'analytics.ida.digital.cabinet-office.gov.uk'
    path = 'index.php'
    url_template = '{}://{}/{}'
    url = url_template.format(protocol, domain, path)
    with open("../creds/piwik_token.json") as ft:
        token = json.load(ft)

    token = token['token']

    # Build the query string
    qs = {
        'module': 'API',
        'method': 'Goals.get',
        'idSite': '1',
        'period': 'range',
        'segment': 'customVariableValue1=={}'.format(rp),
        'idGoal':goalid,
        # 'date': '{},{}'.format(start_date,end_date), # TODO: Update this for the required Date Range
        'date': date,# TODO: Update this for the required Date Range
        'format': 'json',
        'token_auth': token,
    }
    response = requests.get(url,qs)
    print(response.url)
    raw_goal = response.json()

    return raw_goal['nb_conversions']
# piwik_goal = get_goal_results('2017-01-01,2017-01-01','DWP UCDS',16)


