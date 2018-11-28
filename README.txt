General task will involve:
- use Google Geocoding API to read some user-entered geographic locations of
airport names (later we will call it just "data")
- storing and retrieving (when needed) data using SQLte Database
- placing (visualizing) data on a Google Map (so it can be viewed in a browser)


Notes:
*provided solution was tested only on Ubuntu Linux
** you will need SQLite browser to view and modify the database that will be generated
*** in order to run scripts, you need to register your own project and obtain your own API key grom Google
Details - https://developers.google.com/maps/documentation/geocoding/intro
**** Google Geocoding API have limitations of requests per day/per user.
Details - https://developers.google.com/maps/documentation/geolocation/usage-and-billing
***** This project is inspired by similar project from Python for Everybody Course from University of Michigan,
where Dr. Chuck was visualising list of Universities on Google Map



Solution:

================    First phase (airports.txt, script geo-load.py and geo-coding.sqlite):   ================

    - take our input data in the file (airports.txt) and read it one line at a time
    - before use the geocoding API, check to see if we already have the data for that particular line of input
    in database
    - retrieve the geocoded response and if we don't have the data for the location, call the geocoding API to retrieve
    the data and store it in the database (geo-coding.sqlite).

*To run script again - just remove the file geo-coding.sqlite

** Example of run after there is already some data in the database:

```
Found in database:  Boryspil International Airport

Found in database:  Cherkasy International Airport

Found in database:  Chernivtsi International Airport

Resolving Dnipropetrovsk International Airport
Retrieving https://maps.googleapis.com/maps/api/place/textsearch/json?query=Dnipropetrovsk+International+Airport&key=AIzaSyBrpDDqFMG87-o9kpkx8oCQUUUgIWQmcWE
Retrieved 1731 characters {    "results" : [
{u'status': u'OK', u'results': ... }
.
.
.

```

Explanation:

The first 3 locations are already in the database and so they are skipped.
The program scans to the point where it finds un-retrieved locations and starts retrieving them.

The geo-load.py can be stopped at any time, and there is a counter that you can use to limit the number of calls to
the geocoding API for each run.




================    Second phase (script geo-dump.py and where-geo.js):  ================

    - reads just created database geo-coding.sqlite and writes tile file (where-geo.js) with the location, latitude,
    and longitude in the form of executable JavaScript code.

*Example of written data inside where-geo.js:

```
myData = [
[42.340075,-71.0895367, 'Northeastern, Boston, MA 02115, USA'],
[32.778949,35.019648, 'Technion/ Sports Building, Haifa'],
[33.1561058,131.826132, 'Japan, 〒875-0002 Ōita-ken, Usuki-shi, Shitanoe, 1232−2 ＵＭＤ'],]
];
.
.
.

```

** When you run script geo-dump.py, in case of success, in the console you will see something like that:

```
Northeastern University, 360 Huntington Avenue, Boston, MA 02115, USA 42.3396998 -71.08975
Bradley University, 1501 West Bradley Avenue, Peoria, IL 61625, USA 40.6963857 -89.6160811
.
.
.


2 records written to where.js
Open airports.html to view the data in a browser
```

Explanation:
with each record to the where-geo.js, geo-dump.py will show in the console what exactly is written to the where-geo.js
in a format (where, lat, lng). Then it will sum up how many records was written.




================    Third phase(airports.html)  ================

airports.html consists of HTML and JavaScript to visualize a Google Map.
It reads the most recent data in where.js to get the data to be visualized.

Open where.html in a browser to see the locations.

You can hover over each map pin to find the location that the gecoding API returned for the user-entered input.
If you cannot see any data when you open the where.html file, you might want to check the JavaScript or developer
console for your browser.

