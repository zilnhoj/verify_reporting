import pandas as pd
import requests
import json
import csv
from bokeh.charts import Bar, output_file, show
from bokeh.layouts import widgetbox
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn
from bokeh.layouts import layout
from bokeh.charts.attributes import cat

# def get_piwik_data(start_date,end_date):
def get_piwik_data(date):
# print('start date is {}, end date is {}'.format(start_date,end_date))

# start_date = '2016-11-01'
# end_date = '2016-11-30'
    # services = [
    #     'DWP UCDS', 'DEFRA RP', 'BIS RP', 'DVLA VDL',
    #     'DVLA F2D REPORT', 'DVLA F2D RENEW', 'HMRC SA', 'HMRC CC',
    #     'HMRC TE', 'HMRC YSP', 'HMRC PTA', 'HMRC FF',
    # ]

    # Pages for which we need page view data
    with open('../config_files/services.json') as sf:
        pages = json.load(sf)

    

    

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
        # 'date': '{},{}'.format(start_date,end_date), # TODO: Update this for the required Date Range
        'date': date,# TODO: Update this for the required Date Range
        'format': 'json',
        'token_auth': token,
    }
    results = {}

    # for service in services:
    #     print("Processing service: {}".format(service))
    service_results = []
    for segment_name, segment_match in pages.items():
        print('Looking up segment: {}'.format(segment_name))
        qs['segment'] = 'pageTitle=={}'.format(segment_match)
        response = requests.get(url, qs)
        print(response.url)
        raw_result = response.json()
        result = {
            'segment': segment_match,
            'unique_page_views': raw_result['nb_uniq_pageviews'],
            'page_views': raw_result['nb_pageviews']
        }
        service_results.append(result)
        # results[service] = service_results

    # with open('views.json', 'w') as my_file:
    #     json.dump(service_results, my_file, indent=2)

#     # Export as csv
#     # with open('views.csv', 'w') as my_file:
#     #     field_names = ['segment', 'unique_page_views',
#     #                    'page_views']

#     #     gds_writer = csv.DictWriter(my_file, fieldnames=field_names)
#     #     gds_writer.writeheader()
#     #     for service, segments in service_results.items():
#     #         for segment in segments:
#     #             segment['service'] = service
#     #             gds_writer.writerow(segment)



#     piwikdata = pd.read_json('views.json')
#     piwikdata['date'] = date[:date.find(',')]
#     piwikdata = piwikdata[['date', 'segment', 'unique_page_views', 'page_views']]
#     piwikdata = piwikdata.sort_values('page_views', ascending=False)
#     # piwikdata = piwikdata.reset_index
#     return piwikdata

# piwik_data = get_piwik_data('2016-11-01,2016-11-01')
# piwik_data = piwik_data.reset_index()
# piwik_data =piwik_data[['date','segment','unique_page_views','page_views']]

# # p = Bar(piwik_data, values='page_views',label='segment',legend=False)
# p = Bar(piwik_data, values='page_views',label=cat('segment',sort=False),legend=False)
# # output_file('pwk_funnel_all.html') 
# # show(p)

# source = ColumnDataSource(piwik_data)

# columns = [
#         TableColumn(field="segment", title="Page Title"),
#         TableColumn(field="page_views", title="Pageviews"),
#         TableColumn(field="unique_page_views", title="Unique pageviews"),
#     ]

# data_table = DataTable(source=source, columns=columns, width=800, height=280)

# # show(widgetbox(data_table))
# l = layout([
#   [p],
#   [data_table],
# ], sizing_mode='stretch_both')



# output_file('pwk_funnel_all.html') 

# show(l)
# # piwik_data = get_piwik_data()
