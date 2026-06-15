#!/usr/bin/env python3
#
# apiHelper
# Uses requests to make A911 API requests
#
import requests
import urllib
from a911.config import *

access_token=""

def requestGet(path, params) -> dict:
  """
  Make a get request
  """
  url = api_url + '/' + path
  headers = {'Authorization': 'Bearer ' + access_token}
  r = requests.get(url, headers=headers, params=params)
  if r.status_code >= 300:
    print("A911 Fail: ", r.status_code, ': ', r.text)
    raise ValueError('A911 api fail')
  json = responseToJson(r)
  if 'result' in json and json['result'] != 'success':
    print(f"A911 get request failed {path}")
  return json

def requestAccessToken():
  global access_token
  if access_token:
    return;

  url="https://console.active911.com/interface/dev/api_access.php"
  auth = {"refresh_token": refresh_token}
  form = urllib.parse.urlencode(auth)
  headers = {"Content-Type": "application/x-www-form-urlencoded"}
  r = requests.post(url, data=form, headers=headers)
  if r.status_code >= 300:
    print("A911 Get Access Token Fail: ", r.status_code, ': ', r.text)
    raise ValueError('A911 api get access token fail')
  json = responseToJson(r)
  if 'access_token' in json:
    access_token = json['access_token']
    print("got access token")
  else:
    print("Could not get access token")
    raise ValueError('A911 api get access token fail')

def responseToJson(response):
  try:
    json = response.json()
    return json
  except Exception:
    print("Could not convert to json")
  return {}
  


