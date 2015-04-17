import json
import webapp2
import time
import google.appengine.api.users as users

import model


def UserAsDict(user):
  return {
    'id': user.user_id(), 
    'email': user.email(), 
    'admin': users.is_current_user_admin(),
    'nickname': user.nickname()
  }

def GroupsAsDict(groups):
  group_dict = {'groups': []}
  for group in groups:
    group_dict.groups.append({'name': group.name()})
  return group_dict

# parent handler class 
class RestHandler(webapp2.RequestHandler):

  def dispatch(self):
    #time.sleep(1)
    super(RestHandler, self).dispatch()


  def SendJson(self, r):
    self.response.headers['content-type'] = 'text/plain'
    self.response.write(json.dumps(r))
    

class UserHandler(RestHandler):

  def get(self):
    if "login" in self.request.path:
      self.redirect(users.create_login_url())
    elif "logout" in self.request.path:
      self.redirect(users.create_logout_url('/'))
    else:
        user = users.get_current_user()
        if user != None:
          self.SendJson(UserAsDict(user))
        else:
          self.SendJson({'user': None})

class GroupHandler(RestHandler):

  def get(self):
    user = users.get_current_user()
    if user != None:
      groups = model.ListGroups(user)
      self.SendJson(GroupsAsDict(groups))

class QueryHandler(RestHandler):

  def get(self):
    guests = model.AllGuests()
    r = [ AsDict(guest) for guest in guests ]
    self.SendJson(r)


class UpdateHandler(RestHandler):

  def post(self):
    r = json.loads(self.request.body)
    guest = model.UpdateGuest(r['id'], r['first'], r['last'])
    r = AsDict(guest)
    self.SendJson(r)


class InsertHandler(RestHandler):

  def post(self):
    r = json.loads(self.request.body)
    guest = model.InsertGuest(r['first'], r['last'])
    r = AsDict(guest)
    self.SendJson(r)


class DeleteHandler(RestHandler):

  def post(self):
    r = json.loads(self.request.body)
    model.DeleteGuest(r['id'])


APP = webapp2.WSGIApplication([
    ('/api/query', QueryHandler),
    ('/api/insert', InsertHandler),
    ('/api/delete', DeleteHandler),
    ('/api/update', UpdateHandler),
    (r'/api/user/.*', UserHandler),
    (r'/api/groups/.*', GroupHandler),
], debug=True)


