import pandas as pd

append_df = pd.DataFrame()

csvs = ['verifications_by_rp_report.2016-01-23.csv',
		'verifications_by_rp_report.20170124.csv',
		'verifications_by_rp_report.20170125.csv',
		'verifications_by_rp_2017-01-27_2017-01-27.csv',
		'verifications_by_rp_2017-01-28_2017-01-28.csv',
		'verifications_by_rp_2017-01-29_2017-01-29.csv']

for csv in csvs:
	df = pd.read_csv('../not_to_github/verification/daily/{}'.format(csv))
	append_df = append_df.append(df)


append_df.to_csv('../not_to_github/verification/weekly/verifications_by_rp_report.2016-01-23_2017-01-29.csv')