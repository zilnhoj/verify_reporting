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

weekly_new, weekly_returning = get_final_df()

raw_result = get_goals_ids()
date = '2017-01-23,2017-01-29'

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
def row_by_date(df):
	return df[df['Timestamp']==date[:date.find(',')]]


def master_rp(date,rp): 
	print(rp)

	df = pd.DataFrame({'Week': week,
						'[F] Total_number_of_successful_matches':get_rp_pages(date,pages['matching'],services[rp]),
					 	'[I] verifications verifications csv [Weekly - verifications]':row_by_date(weekly_returning)[rp],
						'[P] Success - REGISTER_WITH_IDP':get_rp_pages(date,pages['success_register'],services[rp]),
						'[Q] Failure - REGISTER_WITH_IDP':get_rp_pages(date,pages['register_failure'],services[rp]),
						'[R] Cancel - REGISTER_WITH_IDP':get_rp_pages(date,pages['cancel_register'],services[rp]),
						'[S] Success - SIGN_IN_WITH_IDP':get_rp_pages(date,pages['success_register'],services[rp]),
						'[T] signin journeys started (goal s2)':get_goal_results(date,map_goals['S2 IDP Was Chosen for Sign In'],services[rp]),
						'[U] sign-ins hub data verifications csv - service':row_by_date(weekly_new)[rp],
						'[H] visits where a verification journey startedPiwik - UPV':get_rp_pages(date,pages['choosing'],services[rp]),
						'[V] IDP visits with a reg requestV4':get_goal_results(date,map_goals['V4 IDP Was Chosen for Verification'],services[rp])})

	df['[k] visits where a signin journey started'] = df['[T] signin journeys started (goal s2)']-(df['[I] verifications verifications csv [Weekly - verifications]']-df['[P] Success - REGISTER_WITH_IDP'])
	df['[L] visits where a user signed in'] = df['[S] Success - SIGN_IN_WITH_IDP']- (df['[I] verifications verifications csv [Weekly - verifications]']-df['[P] Success - REGISTER_WITH_IDP'])
	df['[B] Visits started on GOV.UK Verify hub'] = df['[H] visits where a verification journey startedPiwik - UPV'] + df['[k] visits where a signin journey started']
	df['[C] Visits with a successful verification or signin'] = df['[I] verifications verifications csv [Weekly - verifications]'] + df['[L] visits where a user signed in']
	df['[D] (B/A) Overall completion rate'] = df['[C] Visits with a successful verification or signin']/df['[B] Visits started on GOV.UK Verify hub']
	df['[E] Total verifications and signins'] = df['[I] verifications verifications csv [Weekly - verifications]'] + df['[U] sign-ins hub data verifications csv - service']
	df['[G] (D/C) Match rate'] = df['[F] Total_number_of_successful_matches']/df['[E] Total verifications and signins']
	df['[J] verification completion rate'] = df['[I] verifications verifications csv [Weekly - verifications]']/df['[H] visits where a verification journey startedPiwik - UPV']
	df['[M] Signin completion rate'] = df['[L] visits where a user signed in']/df['[k] visits where a signin journey started']
	df['[W] percentage of verifications from 1st time users'] = (df['[H] visits where a verification journey startedPiwik - UPV']+df['[S] Success - SIGN_IN_WITH_IDP'])/((df['[H] visits where a verification journey startedPiwik - UPV']+0.12)+df['[H] visits where a verification journey startedPiwik - UPV']) #really need to check this data point 
	df['[N] success rate'] = df['[I] verifications verifications csv [Weekly - verifications]']/(df['[I] verifications verifications csv [Weekly - verifications]']+df['[Q] Failure - REGISTER_WITH_IDP']+(df['[R] Cancel - REGISTER_WITH_IDP']/2))
	df['[X] People visiting an IDP to register'] = df['[V] IDP visits with a reg requestV4']+df['[W] percentage of verifications from 1st time users']
	df['[O] IPD Conversion rate'] = (df['[I] verifications verifications csv [Weekly - verifications]']+df['[L] visits where a user signed in'])/(df['[k] visits where a signin journey started']+df['[X] People visiting an IDP to register'])

	df = df[['Week',
	'[B] Visits started on GOV.UK Verify hub',
	'[C] Visits with a successful verification or signin',
	'[D] (B/A) Overall completion rate',
	'[E] Total verifications and signins',
	'[F] Total_number_of_successful_matches',
	'[G] (D/C) Match rate',
	'[H] visits where a verification journey startedPiwik - UPV',
	'[I] verifications verifications csv [Weekly - verifications]',
	'[J] verification completion rate',
	'[k] visits where a signin journey started',
	'[L] visits where a user signed in',
	'[M] Signin completion rate']]

	gc = spreadsheet_setup()
	spreadsheet = gc.open(sheets_tabs_names[rp]['Spreadsheet_name'])
	worksheet = spreadsheet.worksheet(sheets_tabs_names[rp]['tabs'][0])
	pwkdf = pd.DataFrame(worksheet.get_all_values())
	start_cell = len(pwkdf)+1
	
	if len(pwkdf[pwkdf[0]==date])>0:

		if len(pwkdf) < 1:
			updatesheet(sheets_tabs_names[rp]['Spreadsheet_name'], sheets_tabs_names[rp]['tabs'][0],df,2,len(df))
		else:
			updatesheet(sheets_tabs_names[rp]['Spreadsheet_name'], sheets_tabs_names[rp]['tabs'][0],df,start_cell,len(df))
	else:
		print('You have already run this report for the reporting period {}'.format(date))



for k,v in sheets_tabs_names.items():
	print(k)
	master_rp(date,k)
	
