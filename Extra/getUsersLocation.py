import json,httplib,urllib

connection = httplib.HTTPSConnection('api.parse.com', 443)
connection.connect()

from datetime import datetime, timedelta

def convertUTCDateToParseDate(utcdate):
  date = {
    "__type": "Date", 
    "iso": utcdate.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
  }
  return date

def convertParseDateToUTCDate(date):
  utcdate = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')
  return utcdate

def convertParseDateToDisplayDate(date):
  utcdate = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')
  return utcdate.strftime("%Y/%m/%d")

out = open('Users Location.csv', 'w')
out.write('{:s}, {:s}, {:s}'.format('Username', 'Lat', 'Long'))
out.write('\n')

def getUsersLocation():
  first_run = True
  skip = 0
  while True:
    if first_run:
      params = urllib.urlencode({
        "where": json.dumps({
          "lat": {
            "$exists": True
          },
          "long": {
            "$exists": True
          }        
        }),
        "keys": "user,lat,long",
        "limit": 100,
        "skip": skip,
        "order": "createdAt",
        "include": "user"
      })
    else:
      params = urllib.urlencode({
        "where": json.dumps({
          "lat": {
            "$exists": True
          },
          "long": {
            "$exists": True
          },
          "createdAt": {
            "$gt": last_date,
          }
        }),
        "keys": "user,lat,long",
        "limit": 100,
        "skip": skip,
        "order": "createdAt",
        "include": "user"
      })
    skip += 100
    endpoint = '/1/sessions?%s' % params
    connection.request('GET', endpoint, '', {
      "X-Parse-Application-Id": "jrumkUT2jzvbFn7czsC5fQmFG5JIYSE4P7GJrlOG",
      "X-Parse-REST-API-Key": "nJKpGXJMp6Y6RCzRAR6VtdI1A8BN1IdI4g7KJILU",
      "X-Parse-Master-Key": "uh9Vt7UoQUcsUDheZgoOuaBzbPFzUDoxkhSFPEXk"
    })
    sessions = json.loads(connection.getresponse().read())["results"]
    if len(sessions) == 0:
      break
    for session in sessions:
      if session.has_key("user"):
        out.write('{:s}, {:f}, {:f}'.format(session["user"]["username"], session["lat"], session["long"]))
        out.write('\n')
    if skip == 10000:
      skip = 0
      first_run = False
      last_date = sessions[len(sessions)-1]["createdAt"]
  return

getUsersLocation()