import requests
import xml.etree.ElementTree as ET

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

#TODO: Add the select function to the query
#Paramaters for the query
params = {
    "$filter": filter_query,
    "$expand": "Measure"
}

#Make the GET request
response = requests.get(base_url, params=params)
print(response.url)

#Parse the XML Response
root = ET.fromstring(response.content)

# Find all entries in the XML response
entries = root.findall(".//atom:entry", namespaces)

#TODO: Find a way to make this stop double printing measures
if entries:
    print(f"Bills introduced by {LegislatoreCode} in session {SessionKey}:")
    for entry in entries:
        # Extract Measure details
        MeasurePrefix = entry.find(".//d:MeasurePrefix", namespaces).text
        MeasureNumber = entry.find(".//d:MeasureNumber", namespaces).text
        print(f"- Measure Number: {MeasurePrefix}{MeasureNumber}")
    else:
        print(f"No bills found for {LegislatoreCode} in session {SessionKey}.")


#Todo: Take the measures and start turning it into an actual product


