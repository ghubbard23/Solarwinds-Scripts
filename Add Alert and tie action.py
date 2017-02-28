from __future__ import print_function
import re
import requests
from orionsdk import SwisClient
import time
import csv

#Asks for user input on filename. Input is a raw string so the \\ shouldn't be needed
csvFile = csv.reader(open(input('File Path of CSV of data that needs to be imported: ')))

#Login Prompt. Asks for necessary info to hit the API. I haven't tried using the hostname of Solarwinds, only the IP. 
#Also, domain accounts don't seem to work. Only local accounts. Not sure why.
print("Login to Solarwinds")
npm_server = input('Solarwinds Server IP: ')
username = input('Solarwinds Username: ')
password = input('Solarwinds Password: ')

#Sets up connection to Solarwinds API
swis = SwisClient(npm_server, username, password)
print("Add an Alert:")

#define the main function
def main():
    for row in csvFile:
        #When creating the alert, 4 variables are needed in the CSV and last_edit is NOT in the CSV
        #3 more variables are needed to tie the alerts
        col1, col2, col3, col4, col5, col6, col7 = row
        #Future reference. Don't have a filename as csv.py. That doesn't work with other files trying to import CSV modules :)
        alert_name = ("%s" % (col1))
        ObjectType = ("%s" % (col2))
        alert_trigger = ("%s" % (col3))
        severity = (col4)
        last_edit = (time.strftime("%m/%d/%Y %I:%M %p"))
        # set up property bag for the new alert
        alert_variables = {
                'Name': alert_name,
                'ObjectType': ObjectType,
                'Trigger': alert_trigger,
                'Severity': severity,
                'LastEdit': last_edit
                }
        #Let me know what's happening
        print("Adding alert {}... ".format(alert_variables['Name']), end="")
        results = swis.create('Orion.AlertConfigurations', **alert_variables)
        print("DONE!")
        #Confirm the AlertID
        print(results)
        print("Adding action to alert")
        #setup alert actions
        #grab the last 3 characters of the results with the slice below
        parent_id = results[-3:]
        action_id = ("%s" % (col5))
        environment_type = ("%s" % (col6))
        category_type = ("%s" % (col7))
        #setup alert action variables
        action_variables = {
                'ParentID': parent_id,
                'ActionID': action_id,
                'EnvironmentType': environment_type,
                'CategoryType': category_type
                }
        results2 = swis.create('Orion.ActionsAssignments', **action_variables)
        print(results2)
            


#not really sure what this does. It was in the initial ORION API samples I was working with from GitHub
requests.packages.urllib3.disable_warnings()


if __name__ == '__main__':
    main()
