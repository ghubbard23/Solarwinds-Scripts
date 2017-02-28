from __future__ import print_function
import re
import requests
from orionsdk import SwisClient
import time
import csv

#Login Prompt. Asks for necessary info to hit the API. I haven't tried using the hostname of Solarwinds, only the IP. 
#Also, domain accounts don't seem to work. Only local accounts. Not sure why.
print('Login to Solarwinds')
npm_server = '10.2.2.66'
print('Use a local Solarwinds service account for login...')
username = input('Username: ')
password = input('Password: ')

#Creates connection to Solarwinds API    
swis = SwisClient(npm_server, username, password)

#Asks for user input on filename. Input is a raw string so the \\ shouldn't be needed
csvFile = csv.reader(open(input('File Path of CSV of data that needs to be imported: ')))

print("Add a group:")

def main():
  #iterate through the rows in the csv file
    for row in csvFile:
        #col1 - Name of the group... col2 - containerID that the new group is nested into
        #col3 - Environment (SND,DEV,TST,PRD) col4 - Name of application. This should correlate to the NameOfApp custom property 
        col1, col2, col3, col4 = row
        group_name = ("%s" % (col4))
        #owner will always be "core"
        group_owner = 'core'
        #frequency is always 60
        refresh_frequency = 60
        #rollup is always 0
        status_rollup = 0
        #Reusing the group name as the group description
        group_description = ("%s" % (col1))
        #polling_enabled should always be true
        polling_enabled = True
        #Name is being called from col1, Environment is from col3, NameofApp from col4
        group_members = [
          {'Name': 'NodeQuery',  'Definition': "filter:/Orion.Nodes[CustomProperties.Environment='{0}' AND CustomProperties.NameOfApp='{1}']" .format(col3, col1)},
          {'Name': 'AppQuery',   'Definition': "filter:/Orion.APM.GenericApplication[Contains(Template.DisplayName,'{0}')]" .format(col4)},
          {'Name': 'WPMQuery',   'Definition': "filter:/Orion.SEUM.Transactions[Contains(Recording.DisplayName,'{0}')]" .format(col4)},
        ]
        print("Adding group {}... ".format(group_name), end="")
        #swis.create did not work for this, not sure why. Using swis.invoke with the "CreateContainer" verb called out in the Schema
        groupID = swis.invoke('Orion.Container', 'CreateContainer',
                              group_name,
                              group_owner,
                              refresh_frequency,
                              status_rollup,
                              group_description,
                              polling_enabled,
                              group_members,
                             )
        print("Done Adding Group")
        print("Here is your new groups ContainerID.")
        print(groupID)
        print("Adding new group to parent...")
        #Starting to nest new group into parent group.
        #defining variable to grab the new container id and format appropriately to use as property for parent group
        group_members2 = {'Name': 'Test', 'Definition': 'swis://solarwinds.wwt.com/Orion/Orion.Groups/ContainerID=%s' % (groupID)}
        #Using invoke again with "AddDefinition" verb  to nest newly created group into parent group. Parent Group is defined in col2 of the CSV.
        results2 = swis.invoke('Orion.Container', 'AddDefinition',
                              #pulling in col2 as a string then converting to integer
                              int(('%s' % (col2))),
                              group_members2,
                              )
        print("Done adding group to parent.")
        print("Script Complete.")
        print("")
        print("")

requests.packages.urllib3.disable_warnings()


if __name__ == '__main__':
    main()
