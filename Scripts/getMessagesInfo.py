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

out = open('Messages Info.csv', 'w')
out.write('{:s}, {:s}, {:s}'.format('Class Code', 'Teacher Username', 'Created Date'))
out.write('\n')

def getMessagesInfo(start_date, end_date):
  first_run = True
  skip = 0
  while True:
    if first_run:
      params = urllib.urlencode({
        "where": json.dumps({
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
    endpoint = '/1/classes/GroupDetails?%s' % params
    connection.request('GET', endpoint, '', {
      "X-Parse-Application-Id": "jrumkUT2jzvbFn7czsC5fQmFG5JIYSE4P7GJrlOG",
      "X-Parse-REST-API-Key": "nJKpGXJMp6Y6RCzRAR6VtdI1A8BN1IdI4g7KJILU",
    })
    groupdetails = json.loads(connection.getresponse().read())["results"]
    if len(groupdetails) == 0:
      break
    for groupdetail in groupdetails:
      out.write('{:s}, {:s}, {:s}'.format(groupdetail["code"].encode('utf-8', 'ignore'), groupdetail["senderId"], convertParseDateToDisplayDate(groupdetail["createdAt"])))
      out.write('\n')
    if skip == 10000:
      skip = 0
      first_run = False
      last_date = groupdetails[len(groupdetails)-1]["createdAt"]  
  return

start_date = datetime(2015,9,7,0,0)
end_date = datetime(2015,9,14,0,0)

getMessagesInfo(convertUTCDateToParseDate(start_date), convertUTCDateToParseDate(end_date))