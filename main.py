import json
import webapp2

import datetime

from google.appengine.api import users
from google.appengine.ext import ndb
import model
import time


def UserAsDict(user):
    return {
        'id': user.userid,
        'nickname': user.username
    }

def GroupsAsDict(groups):
    group_dict = {'groups': []}
    for group in groups:
        new_group = {
            'name': group.name, 
            'members': [],
            'key': group.key.urlsafe(),
            'knob': group.knob
            }
        for i in range(len(group.members)):
            new_group['members'].append(UserAsDict(group.members[i]))
        new_group['timein'] = str(group.timein)
        new_group['timeout'] = str(group.timeout)
        new_group['servertime'] = str(datetime.datetime.now())
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
            self.redirect(users.create_login_url('/dashboard'))
        elif "logout" in self.request.path:
            self.redirect(users.create_logout_url('/'))
        else:
            user = users.get_current_user()
            usr = model.UserProfile.query(model.UserProfile.userid == user.user_id()).get()
            if user != None:
                self.SendJson(UserAsDict(usr))
            else:
                self.SendJson({'user': None})

class GroupHandler(RestHandler):

    def get(self):
        user = users.get_current_user()
        if user != None:
            usr = model.UserProfile.query(model.UserProfile.userid == user.user_id()).get()
            if usr == None:
                u = model.UserProfile()
                u.username = user.nickname()
                u.userid = user.user_id()
                u.put()
            groups = model.ListGroups(usr)
            self.SendJson(GroupsAsDict(groups))

class KnobHandler(RestHandler):

    def get(self):
        pass

    # expects:
    #   {
    #       'group': ndb.key,
    #       'new_time': datetime,
    #       'message': string
    #   }
    def post(self):
        key = ndb.Key(urlsafe=self.request.get('group'))
        group = key.get()

        group.timein = datetime.datetime.now()
        group.timeout = datetime.datetime.now() + datetime.timedelta(hours = -7, minutes = int(self.request.get('delta_minutes')))
        group.knob = True
        group.sock_owner = model.UserProfile.query(model.UserProfile.userid == self.request.get('userid')).get()
        group.sock_msg = self.request.get('message')
        group.put()

class UserInviteHandler(RestHandler):

    def get(self):
      user = users.get_current_user()
      if user != None:
        self.response.headers['content-type'] = 'text/html'
        self.response.write(self.request.get(''))
        self.response.write("<html><body><form method='POST' action='/api/user/invite'><input type='text' name='user_name'><input type='submit'></form></body></html>")

    def post(self):
        r = self.request.get('user_name_search')
        group_key = ndb.Key(urlsafe=self.request.get('group_key'))
        query = model.UserProfile.query(model.UserProfile.username == r)
        usr = query.get()
        if usr != None:
            group = group_key.get()
            group.members.append(usr)
            group.put()
        self.redirect('/dashboard')



class GroupCreateHandler(RestHandler):

    def get(self):
      user = users.get_current_user()
      if user != None:
        self.response.headers['content-type'] = 'text/html'
        self.response.write("<html><body><form method='POST' action='/api/groups/create'><input type='text' name='group_name'><input type='submit'></form></body></html>")

    # expects:
    #   {
    #       'group_name': string,
    #   }
    def post(self):
        user = users.get_current_user()
        usr = model.UserProfile.query(model.UserProfile.userid == user.user_id()).get()
        r = self.request.get('group_name')
        group = model.Group()
        group.name = r
        group.members.append(usr)
        group.knob = False
        group.put()
        self.redirect('/dashboard')


class SockHandler(RestHandler):

    def post(self):
        group = ndb.Key(urlsafe=str(self.request.get('group_key'))).get()
        user = get_current_user()
        minutes = int(self.request.get('minutes'))
        group.knob = True
        query = model.UserProfile.query(model.UserProfile.userid == user.user_id())
        group.sock_owner = query.get()
        group.timein = datetime.datetime.today()
        group.timeout = group.timein + datetime.timedelta(0, 0, 0, 0, minutes)
        group.put()
        self.redirect('/dashboard')

APP = webapp2.WSGIApplication([
    ('/api/sock/remove', SockHandler),
    ('/api/user/invite', UserInviteHandler),
    ('/user/login', UserHandler),
    ('/user/logout', UserHandler),
    (r'/api/user/.*', UserHandler),
    (r'/api/groups/create', GroupCreateHandler),
    (r'/api/groups/.*', GroupHandler),
    (r'/api/knobs/update', KnobHandler),
], debug=True)
