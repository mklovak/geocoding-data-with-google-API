import ssl
import urllib.request
import urllib.parse
import urllib.error
import sqlite3
import json

# Google Places API key and URL
# key is personal, do not publish it
api_key = YOUR OWN API KEY
url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"

# Connect to database and create table if not exist
connect = sqlite3.connect('geo-coding.sqlite')
cursor = connect.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS Locations (address TEXT, geodata TEXT)''')

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


fhandler = open("airports.txt")

# 100 requests per second (QPS), per user are usage limits that are currently in place for the Google Geolocation API
# The following code limitation is created for that purpose
# Details - https://developers.google.com/maps/documentation/geolocation/usage-and-billing
count = 0
for line in fhandler:
    if count > 100:
        print('Retrieved 100 locations, be careful because of usage limitations,'
              'check https://developers.google.com/maps/documentation/geolocation/usage-and-billing.'
              'Restart to retrieve more')
        break

    airport_name = line.strip()
    print('')
    cursor.execute("SELECT geodata FROM Locations WHERE address= ?", (memoryview(airport_name.encode()), ))

    try:
        data = cursor.fetchone()[0]     # method to retrieve a single matching row
        print("Found in database: ", airport_name)
        continue
    except:
        print('# no results')
        pass

    params = dict()

    params["query"] = airport_name
    params['key'] = api_key

    url = url + urllib.parse.urlencode(params)
    print('Retrieving', url)
    uh = urllib.request.urlopen(url, context=ctx)
    data = uh.read().decode()
    print('Retrieved', len(data), 'characters', data[:20].replace('\n', ' '))
    count = count + 1

    try:
        datajs = json.loads(data)
    except:
        print(data)  # We print in case unicode causes an error
        continue

    if 'status' not in datajs or (datajs['status'] != 'OK' and datajs['status'] != 'ZERO_RESULTS'):
        print('# failure to retrieve ')
        print(data)
        break

    cursor.execute('''INSERT INTO Locations (address, geodata)
            VALUES ( ?, ? )''', (memoryview(airport_name.encode()), memoryview(data.encode()) ) )
    connect.commit()


print("Run geo-dump.py to read the data from the SQLite database 'geo-coding.sqlite', "
      "so you can vizualize it on a map later.")
