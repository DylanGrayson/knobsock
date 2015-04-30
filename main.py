import json
import webapp2
import datetime
from google.appengine.api import users
from google.appengine.ext import ndb
import model
import time


def UserAsDict(user):
    return {
        'id': user.user_id(),
        'email': user.email(),
        'admin': users.is_current_user_admin(),
        'nickname': user.nickname()
    }

def AllUsersDict(users):
    users = {'users': []}
    for user in users:
        users['users'].append(UserAsDict(user))
    return users

def GroupsAsDict(groups):
    group_dict = {'groups': []}
    for group in groups:
        new_group = {
            'name': group.name, 
            'members': [],
            'key': group.key.urlsafe(),
            'knob': group.knob}

        for i in range(len(group.members)):
            new_group['members'].append(UserAsDict(group.members[i]))
        new_group['timein'] = group.timein
        new_group['timeout'] = group.timeout
        new_group['servertime'] = time.time()
        group_dict["groups"].append(new_group)
    return group_dict

# parent handler class


class RestHandler(webapp2.RequestHandler):

    def dispatch(self):
        # time.sleep(1)
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

class KnobHandler(RestHandler):

    def get(self):
        user = users.get_current_user()
        if user != None:
            knobs = model.ListKnobs()

class UserInviteHandler(RestHandler):

    def get(self):
      user = users.get_current_user()
      if user != None:
        self.response.headers['content-type'] = 'text/html'
        self.response.write("<html><body><form method='POST' action='/api/user/invite'><input type='text' name='user_name'><input type='submit'></form></body></html>")

    def post(self):
        r = self.request.get('user_name')
        q = users.query().filter()
        self.SendJson()

class GroupCreateHandler(RestHandler):

    def get(self):
      user = users.get_current_user()
      if user != None:
        self.response.headers['content-type'] = 'text/html'
        self.response.write("<html><body><form method='POST' action='/api/groups/create'><input type='text' name='group_name'><input type='submit'></form></body></html>")

    def post(self):
        user = users.get_current_user()
        r = self.request.get('group_name')
        group = model.Group()
        group.name = r
        group.members.append(user)
        group.put()
        self.redirect('/')


class QueryHandler(RestHandler):

    def get(self):
        guests = model.AllGuests()
        r = [AsDict(guest) for guest in guests]
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
    ('/api/user/invite', UserInviteHandler),
    (r'/api/user/.*', UserHandler),
    (r'/api/groups/create', GroupCreateHandler),
    (r'/api/groups/.*', GroupHandler),
    (r'/api/knobs/(.*)', KnobHandler),
], debug=True)
