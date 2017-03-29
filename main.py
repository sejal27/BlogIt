import base
from google.appengine.ext import db
from database import User, Comment, Post, users_key, blog_key

class BlogFront(base.BlogHandler):
    def get(self):

        posts = Post.all().order('-created')

        if self.user:
            self.render('front.html', posts = posts)
        else:
            self.redirect('/login')

class NewPost(base.BlogHandler):
    def get(self):
        if self.user:
            self.render("newpost.html")
        else:
            self.redirect("/login")

    def post(self):
        if not self.user:
            self.redirect('/login')

        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            p = Post(parent = blog_key(), subject = subject, content = content, postuser=self.user)
            p.put()
            self.redirect('/blog/%s' % str(p.key().id()))
        else:
            error = "You must enter the subject and the content for the post."
            self.render("newpost.html", subject=subject, content=content, error=error)

class MyPosts(base.BlogHandler):
    def get(self, uid):
        ukey = User.by_id(int(uid)).key()
        posts = Post.all().filter('postuser =',ukey).order('-created').fetch(limit=100)
        if not posts:
            self.error(404)
            return
        self.render('front.html', posts = posts)

class EditPost(base.BlogHandler):
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)

        if not post:
            self.error(404)
            return

        if self.user:
            self.render("editpost.html", subject=post.subject, content=post.content, error="")
        else: 
            self.redirect('/blog/%s' % str(post.key().id()))

    def post(self, post_id):
        if not self.user:
            self.redirect('/')

        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)
        post_button = self.request.get("post_button")

        if post_button == "submit":
            subject = self.request.get('subject')
            content = self.request.get('content')

            if subject and content:
                post.subject = subject
                post.content = content
                post.put()
            else:
                error = "You must enter the subject and the content for the post."
                self.render("editpost.html", subject=post.subject, content=post.content, error=error)  

        self.redirect('/blog/%s' % str(post.key().id()))

class PostPage(base.BlogHandler):
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)

        if not post:
            self.error(404)
            return

        comments = db.GqlQuery("SELECT * FROM Comment WHERE ANCESTOR IS :1 ", post)

        for c in comments:
            if c.commentuser == self.user:
                c.editallowed = True
                c.put()

        if self.user and post.postuser.key().id() == self.user.key().id():
            self.render("permalink.html", post=post, postuser=True, comments=comments)
        elif self.user:
            self.render("permalink.html", post = post, postuser=False, comments=comments)
        else:
            self.redirect('/signup')

    def post(self, post_id):
        post_button = self.request.get("postbutton").split(',')
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)
        user_key = self.user.key()
        
        if post_button[0] == "like":
            if user_key in post.likedby:
                post.likedby.remove(user_key)
                post.likes_total -= 1
                post.put()
            else:
                post.likes_total += 1
                post.likedby.append(user_key)
                post.put()
            self.redirect('/blog/%s' % str(post.key().id()))
            return

        if post_button[0] == "delete":
            post.delete()
            self.redirect('/')
            return

        if post_button[0] == "comment":
            comment_text = self.request.get("comment_text")
            commentuser = self.user
            newcomment = Comment(parent=post, commentuser=commentuser, commenttext = comment_text, editallowed = True)
            newcomment.put();
            self.redirect('/blog/%s' % str(post.key().id()))
            return

        # if post_button[0] == "editcomment":
