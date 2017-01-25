# verify_reporting

The purpose of this script is to

- Collect data from spreadsheets emailed to the team
- Aggregate the data to show daily and weekly values
- Collect data from PIWIK using the PIWIK api
- Output the collated data in to Google Sheets for each Reliant Party

# Instructions

# Clone the project

We are going to be working on the command line so open up a Terminal session 

Make sure that you have GitHub installed by typing "git --version" into your teminal window

If you don't have Github installed follow these instructions on how to install it and log into your account https://help.github.com/articles/set-up-git/

Once you have github set up, using the Change Directory commnand, cd, change to where you want to put your project folder

You are now ready to clone the project

Type git clone git@github.com:zilnhoj/automate-reporting.git

When you have cloned it you need to set up a creds folder one level down from your automate-reporting folder

In your creds folder you need to make a JSON file which contains your PIWIK token.

The JSON file should be in the format

{
  "token" : "foo"
} 

Replace the 'foo" with your PIWIK token

As well as using the creds folder you also need to clone the verify_config repository https://github.com/zilnhoj/verify_config_files into the same folder as your project folder

You will also need to set up access to the Google Drive api in order to push the data in the script to your spreadsheet

Follow the instructions on how to Authenticate shown in this blog post http://pbpython.com/pandas-google-forms-part1.html.
You will need to:

- set up a project in Google Developer Console
- download a client_secrets.json file - save the file to your creds folder
- share the email address given in your client_secrets.json file with your Google drive spreadsheet

There is a few things you need to be aware of when running this script

You need to copy all the csv files to the relavent folder i.e. all daily verification data needs to go into the data_csvs/verification/daily folder
Do not put dublicate files into the folder as all data in the folder will ba aggregated and you will introduce duplicated data into your reporting
If you make changes to the script and are commiting them back up to GitHub make sure that you do not include the csv files in the data_csv's folder in the push - remove all files and store them locally before you push back to GitHub
There are 4 seperate scripts used to automate the reporting process.

automate_piwik.py - uses the PIWIK API to get data you need for each RP and puts the data into a Pandas dataframe
automate_reporting.py - gathers all the data from your relevant data_csv's folders and aggregates the data into relevant Pandas dataframes
to_sheets.py - passes the data from dataframes into your Google Sheets tabs
get_rp_data.py uses the automate_reporting.py and the automate_piwik.py files to build a dataframe uing criteria supplied in the 'services.json' file.
The data within
to_sheets.py script to pass the data into your Google Sheets tabs

# Running the script

When you are running the script for the first time you need to

- type source bin/activate
- type pip install -r requirements.txt
- this installs all the python libraries you need to run the scripts
- follow the instructions below

Every subsequent times you run the script you need to follow these instructions

- open up the get_rp_data.py file in your favourite text editor
- look for the line - 'date = '2016-11-07,2016-11-13'' - this line sets the date period for the PIWIK API and should be match the time frame for your latest weekly csv data set. If you need to get data for a number of weeks you need to run the script for each separate week changing the date here each time.

- The first date is the start date of the time period and the second date is the end date for the time period

- in the terminal window make sure you are in the automate-reporting folder
- if you are not in your virtual environment type source bin/activate. When you are in your virtual enfironment you will see (automate-reporting) preceeding your commant prompt
- if you want to run the script in iPython type ipython
- then type run data_to_sheets.py
- if you don't want to use ipython type python data_to_scripts.py

