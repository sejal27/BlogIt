from google.appengine.ext import db
import base
import secure

"""
    This module contains the data models - User, Post, and Comment - and related methods.
"""


def users_key(group='default'):
    return db.Key.from_path('users', group)


class User(db.Model):
    name = db.StringProperty(required=True)
    pw_hash = db.StringProperty(required=True)
    email = db.StringProperty()
    displayname = db.StringProperty(required=True)

    # Gets the user by id
    @classmethod
    def by_id(cls, uid):
        return cls.get_by_id(uid, parent=users_key())

    # Gets the user by name
    @classmethod
    def by_name(cls, name):
        u = User.all().filter('name = ', name).get()
        return u

    # This classmethod is also used as a constructor instead of __init__
    @classmethod
    def register(cls, name, pw, displayname, email=None):
        pw_hash = secure.make_pw_hash(name, pw)
        return cls(parent=users_key(),
                   name=name,
                   pw_hash=pw_hash,
                   displayname=displayname,
                   email=email
                   )

    # Check if user name and password combination is valid and return the user
    # object
    @classmethod
    def login(cls, name, pw):
        u = cls.by_name(name)  # Find the user by name
        if u and secure.valid_pw(
                name, pw, u.pw_hash):  # Check for user id and password combination is valid
            return u


def blog_key(name='default'):
    return db.Key.from_path('blogs', name)


class Post(db.Model):
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    # Automatically updated with system date when the post is created
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)
    # Stores the reference to the post author
    postuser = db.ReferenceProperty(User)
    likes_total = db.IntegerProperty(default=0)  # Stores the number of likes
    # Stores the list of users that have liked this post
    likedby = db.ListProperty(db.Key)

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return base.render_str(
            "post.html",
            p=self,
            username=self.postuser.displayname,
            postid=self.key().id())

class Comment(db.Model):
    # Stores the reference to the comment author
    commentuser = db.ReferenceProperty(User)
    commenttext = db.TextProperty(required=True)
    # Set to True if the logged in user is the comment author
    editallowed = db.BooleanProperty(default=False)
    # Set to True if the edit comment button is cliked
    editmode = db.BooleanProperty(default=False)
    created = db.DateTimeProperty(auto_now_add=True)
