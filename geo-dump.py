import sqlite3
import json
import codecs

conn = sqlite3.connect('geo-coding.sqlite')
cursor = conn.cursor()

cursor.execute('SELECT * FROM Locations')
fhandler = codecs.open('where-geo.js', 'w', "utf-8")
fhandler.write("myData = [\n")

count = 0
for row in cursor:
    data = str(row[1].decode())
    try:
        datajs = json.loads(str(data))
    except:
        continue

    if not('status' in datajs and datajs['status'] == 'OK'):
        continue

    lat = datajs["results"][0]["geometry"]["location"]["lat"]
    lng = datajs["results"][0]["geometry"]["location"]["lng"]

    if lat == 0 or lng == 0:
        continue

    where = datajs['results'][0]['formatted_address']
    where = where.replace("'", "")

    try:
        print(where, lat, lng)

        count = count + 1
        if count > 1:
            datajs.write(",\n")

        output = "["+str(lat)+","+str(lng)+", '"+where+"']"
        datajs.write(output)
    except:
        continue

fhandler.write("\n];\n")
cursor.close()
datajs.close()

print(count, "records written to where-geo.js")
print("Now you can open airports.html to view the data in a browser on the map")
