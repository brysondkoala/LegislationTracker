import requests
import xml.etree.ElementTree as ET
import pandas as pd

# Find the LegislatoreCode of a Legislator using FirstName, LastName, SessionKey
# FirstName, LastName, SessionKey
FirstName = "Wlnsvey"
LastName = "Campos"
SessionKey = "2025R1"

# Base URL for the OLIS API
base_url = "https://api.oregonlegislature.gov/odata/odataservice.svc/Legislators"

#Construct the filter query
filter_query = f"FirstName eq '{FirstName}' and LastName eq '{LastName}' and SessionKey eq '{SessionKey}'"

# Parameters for the query
params = {
    "$filter": filter_query,
    "$select": "LegislatorCode"
}

# Make the GET request to the API
response = requests.get(base_url, params=params)

#Parse the XML Response
root = ET.fromstring(response.content)

#Define the namespaces
namespaces = {
    "atom": "http://www.w3.org/2005/Atom",
    "d": "http://schemas.microsoft.com/ado/2007/08/dataservices",
    "m": "http://schemas.microsoft.com/ado/2007/08/dataservices/metadata"
}

#Find all entries in the XML response
entries = root.findall(".//atom:entry", namespaces)

if entries:
    # Extract the LegislatorCode from the first entry
    LegislatoreCode = entries[0].find(".//d:LegislatorCode", namespaces).text
    print(f"LegislatorCode: {LegislatoreCode}")
else:
    print("No matching legislator found.")

#Find Measures sponsored by the legislator based on LegislatorCode, SessionKey
#Base URL for the OLIS API
base_url = "https://api.oregonlegislature.gov/odata/odataservice.svc/MeasureSponsors"

#Construct the filter query
filter_query = f"SessionKey eq '{SessionKey}' and LegislatoreCode eq '{LegislatoreCode}'"

#Paramaters for the query
params = {
    "$filter": filter_query,
    #"$select": "MeasurePrefix, MeasureNumber"
}

#Make the GET request
response = requests.get(base_url, params=params)
print(response.url)

#Parse the XML Response
root = ET.fromstring(response.content)

#Create lists to append output to:
measure_list = []
sponsor_level_list = []

# Find all entries in the XML response
entries = root.findall(".//atom:entry", namespaces)
if entries:
    print(f"Bills introduced by {LegislatoreCode} in session {SessionKey}:")
    for entry in entries:
        # Get Measure #
        MeasurePrefix = entry.find(".//d:MeasurePrefix", namespaces).text
        MeasureNumber = entry.find(".//d:MeasureNumber", namespaces).text
        measure = f"{MeasurePrefix}{MeasureNumber}"
        measure_list.append(measure)

        #Get Chief?
        SponsorLevel = entry.find(".//d:SponsorLevel", namespaces).text
        sponsor_level_list.append(SponsorLevel)
        #print(f"- Measure Number: {MeasurePrefix}{MeasureNumber}")
    else:
        print(f"No bills found for {LegislatoreCode} in session {SessionKey}.")

data = pd.DataFrame({'Measure': measure_list, 'Chief?': sponsor_level_list})
print(data)
data.to_csv('out.csv', index = False)


