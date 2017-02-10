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

If you don't have Github installed follow [these instructions](https://help.github.com/articles/set-up-git/) on how to install it and log into your account 

Once you have github set up, using the Change Directory commnand, cd, change to where you want to put your project folder

You are now ready to clone the project

Type git clone git@github.com:zilnhoj/verify_reporting.git

When you have cloned it you need to set up a creds folder one level up from your automate-reporting folder

In your creds folder create a JSON file which contains your PIWIK token.

The JSON file should be in the format
```JSON
{
  "token" : "foo"
} 
```
Replace the 'foo" with your PIWIK token

As well as using the creds folder you also need to clone the [verify_config repository](https://github.com/zilnhoj/verify_config_files) one level up from this project 

You will need to set up access to the Google Drive api in order to push the data in the script to your spreadsheet

Follow the instructions on how to Authenticate shown in this [blog post](http://pbpython.com/pandas-google-forms-part1.html).
You will need to:

- set up a project in Google Developer Console
- download a client_secrets.json file - save the file to your creds folder
- share the email address given in your client_secrets.json file with your Google drive spreadsheet


#Data location
There is a few things you need to be aware of when running this script

You will need to create a folder set up like 
```
|-- raw_files
	|-- verification
		|-- daily
		|-- weekly
```

You need to copy all the csv files to the relavent folder i.e. all weekly verification data needs to go into the raw_files/verification/weekly folder
Do not put dublicate files into the folder as all data in the folder will ba aggregated and you will introduce duplicated data into your reporting

There are 4 seperate scripts used to automate the reporting process.

- automate_piwik.py - uses the PIWIK API to get data you need for each RP and puts the data into a Pandas dataframe
- automate_reporting.py - gathers all the data from the csv's in the weekly folder and aggregates the data into relevant Pandas dataframes
- to_sheets.py - passes the data from dataframes into your Google Sheets tabs
- get_rp_data.py uses the automate_reporting.py and the automate_piwik.py files to build a dataframe uing criteria supplied in the 'services.json' file.  It passes the data to_sheets.py script which inserts the datainto your Google Sheets tabs

# Setting up to run the script for the first time

When you are running the script for the first time you need to

- type source bin/activate
- type pip install -r requirements.txt
- this installs all the python libraries you need to run the scripts
- follow the instructions below

# Running the script

Once you are set up you need to 

- check in the terminal window and make sure you are in the automate_performance_reporting folder
- if you are not in your virtual environment type source bin/activate. When you are in your virtual enfironment you will see (automate-reporting) preceeding your commant prompt
- if you want to run the script in iPython type ipython
- then type run get_rp_data.py
- enter the start date for the week you are running the report for in the format yyyy-mm-dd
- enter the end date for the week you are running the report for in the format yyyy-mm-dd
- if you don't want to use ipython type python data_to_scripts.py
- enter the start date for the week you are running the report for in the format yyyy-mm-dd
- enter the end date for the week you are running the report for in the format yyyy-mm-dd

# Adding serivces 

When new services are added to Verify you need to update some files in the [config folder](https://github.com/zilnhoj/verify_config_files) in order to include these new new servcies in your reporting.  

Instructions on what you need to do is available at the repository 

