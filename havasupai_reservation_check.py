#!/usr/bin/python

from datetime import datetime
from datetime import timedelta
import configparser
import uuid
import json
import requests
import urllib.request, urllib.error


# https://api.havasupaireservations.com/v1/Reserves/calendar?ec=2018-09-30&np=2&sc=2018-07-01&token=be43a8f7-213a-4339-92d1-327286ab1bd2
NO_OF_PEOPLE=2
CONFIG_FILE_PATH='/Users/kk/work/personal/github.com/configuration/config.properties'
BASE_URL='https://api.havasupaireservations.com/v1/Reserves/calendar?'

def getfirstdateofthemonth():
	return datetime.today().replace(day=1)

def getlastdateofthemonth(first_date):
	next_month=first_date.replace(day=28) + timedelta(days=4)
	return next_month - timedelta(days=next_month.day)

def getSlackURL():
	config=configparser.RawConfigParser()
	config.read(CONFIG_FILE_PATH)

	return config.get('SlackURLS', 'RESERVATION_SLACK_URL')

def sendSlackMessage(message):
	slackurl=getSlackURL()
	headers = { 'Content-type': 'application/json' }
	payload = {
		'text': message,
		'username': 'Havasupai Reservation Availability Bot',
		'channel': '#campsite',
		}
	payload=json.dumps(payload).encode('utf-8')

	try:
		urllib.request.urlopen(slackurl, payload)
	except (urllib.error.URLError, urllib.error.HTTPError) as err:
		print(err.reason)

def getSupaiReservationAvailibility(startdate, enddate, token):
	fullURL=BASE_URL+'ec=%s&np=%s&sc=%s&token=%s' %(enddate, NO_OF_PEOPLE, startdate, token)
	httprequest=urllib.request.Request(fullURL)

	try:
		response=urllib.request.urlopen(httprequest)
		availabilityJson=response.read().decode('utf-8')
		parseAvailabilityJson(availabilityJson)
	except (urllib.error.URLError, urllib.error.HTTPError) as err:
		sendSlackMessage('Error Code: %s, Error Msg: %s' % (err.code, err.reason) )

def parseAvailabilityJson(availabilityJson):
	availabilityDict=json.loads(availabilityJson)
	for epochTime in availabilityDict.keys():
		available=availabilityDict.get(epochTime)
		availabilityDate=datetime.utcfromtimestamp(int(epochTime)).strftime("%Y-%m-%d")

		if available=='true':
			sendSlackMessage('%s - %s' % (availabilityDate, available))

def main():
	token=str(uuid.uuid4())
	first_date=getfirstdateofthemonth()
	last_date=getlastdateofthemonth(first_date)
	month=first_date.month

	while month <= 12:
		getSupaiReservationAvailibility(first_date.strftime("%Y-%m-%d"), last_date.strftime("%Y-%m-%d"), token)

		if month==12:
			break

		month+=1
		first_date=first_date.replace(month=month)
		last_date=getlastdateofthemonth(first_date)

if __name__ == "__main__":
	main()
