#!/usr/bin/env python3
#
# apiHelper
# Uses requests to make D4H API requests
#
import json
import requests

from config import *

# Global properties
context="team"

def requestGet(path, params, use_context=True) -> dict:
  """
  Make a get request
  """
  url = d4h_url + '/' + d4h_api
  if use_context:
    url += '/' + context
  url += '/' + path
  headers = {'Authorization': 'Bearer '+d4h_token}
  r = requests.get(url, headers=headers, params=params)
  if r.status_code >= 300:
    print("D4H Fail: ", r.status_code, ': ', r.json())
    raise ValueError('D4H api fail')
  return r.json()

def requestContext():
  """
  Get the context info for API requests
  """
  global context
  response = requestGet('whoami', {}, use_context=False)
  teamid = response['members'][0]['owner']['id']
  context = 'team/' + str(teamid)
  
