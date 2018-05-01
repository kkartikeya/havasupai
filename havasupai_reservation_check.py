#!/usr/bin/python

from datetime import datetime
from datetime import timedelta
import configparser
import json
import requests
import urllib.request, urllib.parse


# https://api.havasupaireservations.com/v1/Reserves/calendar?ec=2018-09-30&np=2&sc=2018-07-01&token=be43a8f7-213a-4339-92d1-327286ab1bd2
NO_OF_PEOPLE=2
CONFIG_FILE_PATH='/Users/kk/work/personal/github.com/configuration/config.properties'

def getfirstdateofthemonth():
	return datetime.today().replace(day=1)
	
def getlastdateofthemonth():
	next_month=datetime.today().replace(day=28) + timedelta(days=4)
	return next_month - timedelta(days=next_month.day)

def getSlackURL():
	config=configparser.RawConfigParser()
	config.read(CONFIG_FILE_PATH)

	return config.get('SLACKURLS', 'RESERVATION_SLACK_URL')

def sendSlackMessage(message):
	slackurl=getSlackURL()
	headers = { 'Content-type': 'application/json' }
	payload = {
		'text': message,
		'username': 'Havasupai Reservation Availability Bot',
		'channel': '#campsite',
		}
	payload=json.dumps(payload).encode('utf-8')

	urllib.request.urlopen(slackurl, payload)

def getSupaiReservationAvailibility(startdate, enddate):
	print(startdate)
	print(enddate)
	sendSlackMessage('this is a test message.')



def main():
	getSupaiReservationAvailibility(getfirstdateofthemonth(), getlastdateofthemonth())

if __name__ == "__main__":
	main()
