import json
import automate_reporting
from automate_reporting import get_final_df
import id_goals
from id_goals import get_goals_ids
import automate_piwik
from automate_piwik import get_rp_pages
from automate_piwik import get_goal_results
import pandas as pd
import to_sheets
from to_sheets import updatesheet
from to_sheets import spreadsheet_setup
# from automate_reporting import all_csv_data
from automate_piwik import get_rp_pages_pvs


start_date = input('Enter week start date in the format yyyy-mm-dd: ')
end_date = input('Enter the week end date in the format yyyy-mm-dd: ')

date = '{},{}'.format(start_date,end_date)
print(date)

weekly_new, weekly_returning = get_final_df()

def get_date(date):
    full_timestamp = date[:date.find('T')]
    return full_timestamp

# all_csv_data = all_csv_data()
# all_csv_data['strp_timestamp'] = all_csv_data.apply(lambda row: get_date(row['Timestamp']),axis=1)
# weekly_new = all_csv_data[all_csv_data['Response type']=='NEW']
# weekly_returning = all_csv_data[all_csv_data['Response type']=='RETURNING']

raw_result = get_goals_ids()
# date = '2017-01-23,2017-01-29'
# date = '2017-01-16,2017-01-22'



# if len(dateRange)<1 : dateRange=date_list[-1:]
# period = raw_input('Enter period: ')
# if len(period)<1 : period ='week'
# print str(dateRange) + " " + str(period)

def sum_from_dates(start_date,end_date,df,rp):
    df = df[df['RP name']==rp]
    df = df[(df['strp_timestamp']>=start_date) & (df['strp_timestamp']<=end_date)]

    return df['RP name'].count()

def get_week(date):
	return date[:date.find(',')] + ' to ' + date[date.find(',')+1:]

week = get_week(date)

def d_values(d, depth):
    if depth == 1:
        for i in d.values():
            yield i
    else:
        for v in d.values():
            if isinstance(v, dict):
                for i in d_values(v, depth-1):
                    yield i

goal_names = list(d['name'] for d in d_values(raw_result,1))
goal_ids = list(d['idgoal'] for d in d_values(raw_result,1))

map_goals = {k: v for k, v in zip(goal_names, goal_ids)}

with open('../config_files/services.json') as sf:
	services = json.load(sf)


svc_list = list(d  for d in d_values(services,1))

with open('../config_files/pages.json') as sf:
     pages = json.load(sf)

service_vals = list(services.values())

weekly_cols_list_new = list(weekly_new.columns)

with open('../config_files/sheet_tab_names.json') as sts:
	sheets_tabs_names = json.load(sts)

# def upvs(results,date,page,rp):
	
# 	pgeindx = [i for i,x in enumerate(results) if page in x.get('label')]
# 	return results[pgeindx].get('')
def row_by_date(df,rp):
	print(rp)
	return df[rp][df['Timestamp']==date[:date.find(',')]]

# def sum_from_dates(start_date,end_date,df,rp):
#     df = df[(df['strp_timestamp']>=start_date) & (df['strp_timestamp']<=end_date)]
#     return df.sum()

totaldf = pd.DataFrame()
def master_rp(date,rp): 
	# print('{} verifications returning - {} verifications new {}'.format(rp,row_by_date(weekly_returning,rp),row_by_date(weekly_new,rp)))

	df = pd.DataFrame({"rp":rp,
						'Week': week,
						'(D) Total number of successful matches':get_rp_pages_pvs(date,pages['matching'],services[rp]),
					 	'verifications':row_by_date(weekly_new,rp),
					 	# 'verifications':sum_from_dates(start_date,end_date,weekly_new,rp),
						'Success - REGISTER_WITH_IDP':get_rp_pages(date,pages['success_register'],services[rp]),
						'Failure - REGISTER_WITH_IDP':get_rp_pages(date,pages['register_failure'],services[rp]),
						'Cancel - REGISTER_WITH_IDP':get_rp_pages(date,pages['cancel_register'],services[rp]),
						'Success - SIGN_IN_WITH_IDP':get_rp_pages(date,pages['success_sign'],services[rp]),
						'signin journeys started (goal s2)':get_goal_results(date,map_goals['S2 IDP Was Chosen for Sign In'],services[rp]),
						'sign-ins hub data':row_by_date(weekly_returning,rp),
						# 'sign-ins hub data':sum_from_dates(start_date,end_date,weekly_returning,rp),
						'visits where a verification journey started':get_rp_pages(date,pages['choosing'],services[rp]),
						'IDP visits with a reg request V4':get_goal_results(date,map_goals['V4 IDP Was Chosen for Verification'],services[rp])})

	df['visits where a signin journey started'] = df['signin journeys started (goal s2)']-(df['verifications']-df['Success - REGISTER_WITH_IDP'])
	df['visits where a user signed in'] = df['Success - SIGN_IN_WITH_IDP'] - (df['verifications']-df['Success - REGISTER_WITH_IDP'])
	df['(A) Visits started on the GOV.UK Verify hub'] = df['visits where a verification journey started'] + df['visits where a signin journey started']
	df['(B) Visits with a successful verification or sign-in'] = df['verifications'] + df['visits where a user signed in']
	df['(B/A) Overall completion rate'] = df['(B) Visits with a successful verification or sign-in']/df['(A) Visits started on the GOV.UK Verify hub']
	df['(C) Total verifications and signins'] = df['verifications'] + df['sign-ins hub data']
	df['(D/C) Match rate'] = df['(D) Total number of successful matches']/df['(C) Total verifications and signins']
	df['verification completion rate'] = df['verifications']/df['visits where a verification journey started']
	df['Signin completion rate'] = df['visits where a user signed in']/df['visits where a signin journey started']
	

	# print('all dataframe {}'.format(df.tail()))

	df = df[['Week',
	'(A) Visits started on the GOV.UK Verify hub',
	'(B) Visits with a successful verification or sign-in',
	'(B/A) Overall completion rate',
	'(C) Total verifications and signins',
	'(D) Total number of successful matches',
	'(D/C) Match rate',
	'visits where a verification journey started',
	'verifications',
	'verification completion rate',
	'visits where a signin journey started',
	'visits where a user signed in',
	'Signin completion rate']]

	gc = spreadsheet_setup()
	spreadsheet = gc.open(sheets_tabs_names[rp]['Spreadsheet_name'])
	worksheet = spreadsheet.worksheet(sheets_tabs_names[rp]['tabs'][0])
	pwkdf = pd.DataFrame(worksheet.get_all_values())
	start_cell = len(pwkdf)+1
	

	check_date = pwkdf[pwkdf[0]==week]

	print('Length of check date {}'.format(len(check_date)))
	# # if len(check_date) == 0:

	
	# # print('Length of check date {} and head {} and week {}'.format(len(check_date),check_date.head(1),week))

	if len(pwkdf) < 1:
		updatesheet(sheets_tabs_names[rp]['Spreadsheet_name'], sheets_tabs_names[rp]['tabs'][0],df,2,len(df))
	else:
		updatesheet(sheets_tabs_names[rp]['Spreadsheet_name'], sheets_tabs_names[rp]['tabs'][0],df,start_cell,len(df))
	# else:
	# 	print('You have already run this report for the reporting period {}'.format(week))

	# return df



for k,v in sheets_tabs_names.items():
	# print(k)
	master_rp(date,k)
	# df = master_rp(date,k)
	# totaldf = totaldf.append(df)
