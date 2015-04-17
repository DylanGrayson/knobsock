from google.appengine.ext import ndb


class Group(ndb.Model):
    name = ndb.StringProperty()
    members = ndb.UserProperty(repeated=True)


class Knob(ndb.Model):
    name = ndb.StringProperty()
    parent = ndb.StructuredProperty(Group)
    timeout = ndb.DateTimeProperty()
    sock = ndb.BooleanProperty()


### Knob Functions ###
# get all child knobs of a group
def ListKnobs(parent):
    return Knob.query(parent=parent)


def ListGroups(user):
    return Group.query(Group.members == user).fetch(10)

# update values of a knob with given ID


def UpdateKnob(id, name, timeout, sock):
    knob = Knob(id=id, name=name, timeout=timeout, sock=sock)
    knob.put()
    return knob

# create brand new knob
# defaults to no sock


def CreateKnob(name):
    knob = Knob(name=name, sock=False)
    knob.put()
    return knob

# deletes a knob


def DeleteKnob(id):
    key = ndb.Key(Knob, id)
    key.delete()

### Group Functions ###
# update values of a group with given ID


def UpdateGroup(id, name, members):
    group = Group(id=id, name=name, members=members)
    group.put()
    return group

# create brand new group
# members list consists of the logged-in user


def CreateGroup(name):
    user = users.get_current_user()
    if user:
        group = Group(name=name, members=[user])
        group.put()
    else:
        # there needs to be a logged-in user to own this group
        pass
    return group
