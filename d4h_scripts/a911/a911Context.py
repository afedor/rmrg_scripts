#!/usr/bin/env python3
#
# A911Context
# Gets A911 pages
#
import datetime
from . import a911ApiHelper
from .alertModel import AlertModel
from .deviceModel import DeviceModel

class A911Context:

  def __init__(self):
    self.pages = []

  def requestPages(self):
    """ 
    Get the most recent list of pages. Populates
    the pages array with an array of dictionaries containint an 'id'
    """
    response = a911ApiHelper.requestGet('alerts', {})
    if 'message' not in response:
      print("A911 pages failed to find message")
      return
    message = response['message']
    if 'alerts' not in message:
      print("A911 pages failed to find alerts")
      return
    self.pages = message['alerts']

  def requestPage(self, identifier):
    response = a911ApiHelper.requestGet('alerts/'+str(identifier), {})
    if 'message' not in response:
      print("A911 page failed to find message")
      return None
    message = response['message']
    if 'alert' not in message:
      print("A911 pages failed to find alert")
      return None
    page = AlertModel(message['alert'])
    return page

  def requestDevice(self, identifier):
    response = a911ApiHelper.requestGet('devices/'+str(identifier), {})
    if 'message' not in response:
      print("A911 devices failed to find message")
      return None
    message = response['message']
    if 'device' not in message:
      print("A911 device failed to find device")
      return None
    device = DeviceModel(message['device'])
    return device

  def allRespondingDevices(self, page):
    devices = []
    list = page.devices()
    for dict in list:
      print(f"  -- looking for device {dict["identifier"]}")
      device = self.requestDevice(dict["identifier"])
      if device:
        device.setResponse(dict["response"])
        devices.append(device)
    return devices
  
  def pageWithCadCode(self, code):
    for dict in self.pages:
      page = self.requestPage(dict)
      print(f"  -- check page {page.description()} with code {page.cad_code()}")
      if page.cad_code() == code:
        return page
    return None

  def initContext(self):
    a911ApiHelper.requestAccessToken()

