import json
import webapp2
import time
from google.appengine.api import users
from google.appengine.ext import ndb
import model


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
        new_group = {'name': group.name, 'members': []}
        for i in range(len(group.members)):
            new_group['members'].append(UserAsDict(group.members[i]))
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

    def get(self, parent_hash):
        parent_key = ndb.Key(urlsafe=parent_hash)
        parent = parent_key.get()
        #knobs = model.ListKnobs(parent)
        self.response.write(parent_key)

class GroupCreateHandler(RestHandler):

    def get(self):
      user = users.get_current_user()
      if user != None:
        group1 = model.Group(name="Brandon Sucks", members=[user])
        #UNCOMMENT BELOW to put a test group in under your username
        group1.put()

    def post(self):
        r = json.loads(self.request.body)
        group = model.CreateGroup(r['group_name'])


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
    (r'/api/user/.*', UserHandler),
    (r'/api/groups/create', GroupCreateHandler),
    (r'/api/groups/.*', GroupHandler),
    (r'/api/knobs/(.*)', KnobHandler),
], debug=True)
