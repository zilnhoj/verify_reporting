import pandas as pd
import requests
import json
import csv

# def get_piwik_data(start_date,end_date):
def get_rp_pages(date,rp):

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
        'method': 'Actions.getPageTitles',
        'idSite': '1', 
        'period': 'range',
        'segment': 'customVariableValue1=={}'.format(rp),
        # 'date': '{},{}'.format(start_date,end_date), # TODO: Update this for the required Date Range
        'date': date,# TODO: Update this for the required Date Range
        'format': 'json',
        'token_auth': token,
    }
    response = requests.get(url,qs)
    print('the pages report rp {} and URL {}'.format(rp,response.url))
    raw_result = response.json()

    # return raw_result['nb_uniq_pageviews']
    return raw_result


date = '2017-01-16,2017-01-22'  

rp = 'DWP UCDS' 

results = get_rp_pages(date,rp)