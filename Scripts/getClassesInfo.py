import json,httplib,urllib,time

connection = httplib.HTTPSConnection('api.parse.com', 443)
connection.connect()

from datetime import datetime, timedelta

def convertUTCDateToParseDate(utcdate):
  date = {
    "__type": "Date", 
    "iso": utcdate.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
  }
  return date

def convertParseDateToDisplayDate(date):
  utcdate = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')
  return utcdate.strftime("%Y/%m/%d")

out = open('Classes Info.csv', 'w')
out.write('{:s}, {:s}, {:s}'.format('Class Code', 'Teacher Username', 'Created Date'))
out.write('\n')

def getClassesInfo(start_date, end_date):
  first_run = True
  skip = 0
  while True:
    if first_run:
      params = urllib.urlencode({
        "where": json.dumps({
          "classExist": True,
          "createdAt": {
            "$gt": start_date,
            "$lte": end_date
          }
        }),
        "keys": "senderId,code",
        "limit": 100,
        "skip": skip,
        "order": "createdAt"
      })
    else:
      params = urllib.urlencode({
        "where": json.dumps({
          "classExist": True,
          "createdAt": {
            "$gt": last_date,
            "$lte": end_date
          }
        }),
        "keys": "senderId,code",
        "limit": 100,
        "skip": skip,
        "order": "createdAt"
      })
    skip += 100
    endpoint = '/1/classes/Codegroup?%s' % params
    connection.request('GET', endpoint, '', {
      "X-Parse-Application-Id": "jrumkUT2jzvbFn7czsC5fQmFG5JIYSE4P7GJrlOG",
      "X-Parse-REST-API-Key": "nJKpGXJMp6Y6RCzRAR6VtdI1A8BN1IdI4g7KJILU",
    })
    codegroups = json.loads(connection.getresponse().read())["results"]
    if len(codegroups) == 0:
      break
    for codegroup in codegroups:
      out.write('{:s}, {:s}, {:s}'.format(codegroup["code"].encode('utf-8', 'ignore'), codegroup["senderId"], convertParseDateToDisplayDate(codegroup["createdAt"])))
      out.write('\n')
    if skip == 10000:
      skip = 0
      first_run = False
      last_date = codegroups[len(codegroups)-1]["createdAt"]  
  return

start_date = datetime(2015,9,7,0,0)
end_date = datetime(2015,9,14,0,0)

getClassesInfo(convertUTCDateToParseDate(start_date), convertUTCDateToParseDate(end_date))