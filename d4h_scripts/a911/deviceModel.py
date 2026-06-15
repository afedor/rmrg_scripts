
class DeviceModel:

  def __init__(self, model):
    self.device = model
    self.respstr = 'none'

  def memberName(self):
    return self.device['name']

  def response(self):
    return self.respstr

  def setResponse(self, resp):
    self.respstr = resp
