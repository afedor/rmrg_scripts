
class MemberModel:

  def __init__(self, model):
    self.member = model

  def identifier(self):
    return self.member['id']

  def name(self):
    return self.member['name']

  def memberLast(self):
    return self.member['name'].split()[-1]
  
  def memberFirst(self):
    return self.member['name'].split()[0]
  
  def memberLastShort(self):
    return self.memberLast() + self.memberFirst()[0]

  def memberEmail(self):
    email = self.member['email']
    return email['value']

