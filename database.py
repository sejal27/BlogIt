from google.appengine.ext import db
import base
import secure

# TODO: figure this out
def users_key(group = 'default'):
    return db.Key.from_path('users', group)

class User(db.Model):
    name = db.StringProperty(required=True)
    pw_hash = db.StringProperty(required=True)
    email = db.StringProperty()

    @classmethod
    def by_id(cls,uid):
        return cls.get_by_id(uid, parent=users_key())

    @classmethod
    def by_name(cls, name):
        # q = db.GqlQuery("SELECT * FROM User WHERE name= :uname", uname=name)
        # return q.get()
        u = User.all().filter('name = ', name).get()
        return u

    @classmethod # This classmethod is also used as a constructor instead of __init__
    def register(cls, name, pw, email=None):
        pw_hash = secure.make_pw_hash(name, pw)
        return cls(parent = users_key(),
                    name=name,
                    pw_hash=pw_hash,
                    email=email)

    # Check if user name and password combination is valid and return the user object
    @classmethod
    def login(cls, name, pw):
        u = cls.by_name(name) # Find the user by name
        if u and secure.valid_pw(name, pw, u.pw_hash): # Check for user id and password combination is valid
            return u

def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name)

class Post(db.Model):
  subject = db.StringProperty(required=True)
  content = db.TextProperty(required=True)
  created = db.DateTimeProperty(auto_now_add=True)
  last_modified=db.DateTimeProperty(auto_now=True)
  postuser = db.ReferenceProperty(User)
  likes_total = db.IntegerProperty(default=0)
  likedby = db.ListProperty(db.Key)

  def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return base.render_str("post.html", p = self, username=self.postuser.name, postid=self.key().id())

class Comment(db.Model):
    commentuser = db.ReferenceProperty(User)
    commenttext = db.TextProperty(required=True)
    editallowed = db.BooleanProperty(default=False)
    editmode = db.BooleanProperty(default=False)
    created = db.DateTimeProperty(auto_now_add=True)