# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 01:39:31 2021
@author: amannirala13
"""
from twilio.rest import Client
import requests
import geocoder
import sys

my_ip = requests.get('http://ip.42.pl/raw').text
g = geocoder.ip('me')
location = g.latlng

account_sid = 'your_sid'
account_token = 'your_token'

client = Client(account_sid, account_token)

messageBody = 'Hi! This is your Crack Detection System. We found a crack of '+sys.argv[1]+'cm at https://www.google.com/maps/search/?api=1&query='+str(location[0])+','+str(location[1])

message = client.messages.create(body=messageBody, from_='twilio_number', to='target_number')

print("Location:", location)
print("Body:  ", messageBody)
print("Message SID", message.sid)