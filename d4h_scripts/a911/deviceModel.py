
class DeviceModel:

  def __init__(self, model):
    self.device = model
    self.respstr = 'none'

  def memberName(self):
    return self.device['name']

  def memberAgencyName(self):
    if 'memberships' in self.device:
      members = self.device['memberships']
      if len(members):
        member = members[0]
        if 'agency_device_name' in member:
          return member['agency_device_name']
    return self.memberName()

  def response(self):
    return self.respstr

  def setResponse(self, resp):
    self.respstr = resp
