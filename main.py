import base
from google.appengine.ext import db
from database import User, Comment, Post, users_key, blog_key


class BlogFront(base.BlogHandler):
    """
    This handler renders blog's home page.
    """

    def get(self):

        posts = Post.all().order('-created')

        if self.user:
            self.render('front.html', posts=posts, heading_text="")
        else:
            self.redirect('/login')
            return


class NewPost(base.BlogHandler):
    """
    This handler renders the new post page, captures data related to newly created post,
    and stores in the db (Post).
    """

    def get(self):
        if self.user:
            self.render("newpost.html")
        else:
            self.redirect("/login")
            return

    def post(self):
        if not self.user:
            self.redirect('/login')
            return

        postbutton = self.request.get("postbutton")

        if postbutton == "submit":
            subject = self.request.get('subject')
            content = self.request.get('content')

            if subject and content:
                p = Post(
                    parent=blog_key(),
                    subject=subject,
                    content=content,
                    postuser=self.user)
                p.put()
                self.redirect('/blog/%s' % str(p.key().id()))
                return
            else:
                error = "You must enter the subject and the content for the post."
                self.render(
                    "newpost.html",
                    subject=subject,
                    content=content,
                    error=error)
        if postbutton == "cancel":
            self.redirect('/')


class MyPosts(base.BlogHandler):
    """
    This handler renders the page that shows all the posts created by the logged in user.
    """

    def get(self, uid):
        user = User.by_id(int(uid))
        # posts = db.GqlQuery("SELECT * FROM User WHERE postuser = :1 ORDER BY desc", user)
        posts = Post.all().filter('postuser =', user).order('-created')
        # This will display the posts created by the user or a black page if
        # there are no posts
        self.render('front.html', posts=posts)


class EditPost(base.BlogHandler):
    """
    This handler renders the edit post page, captures the contents that have been edited,
    and stores them in the db (Post).
    """

    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)

        if not post:
            self.error(404)
            return

        if self.user:
            self.render(
                "editpost.html",
                subject=post.subject,
                content=post.content,
                error="")
        else:
            self.redirect('/blog/%s' % str(post.key().id()))
            return

    def post(self, post_id):

        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)

        if self.user and self.user == post.postuser:
            post_button = self.request.get("post_button")

            if post_button == "submit":
                subject = self.request.get('subject')
                content = self.request.get('content')

                if subject and content:
                    post.subject = subject
                    post.content = content
                    post.put()
                    self.redirect('/blog/%s' % str(post.key().id()))
                    return
                else:
                    error = "You must enter the subject and the content for the post."
                    self.render(
                        "editpost.html",
                        subject=post.subject,
                        content=post.content,
                        error=error)
            if post_button == "cancel":
                self.redirect('/blog/%s' % str(post.key().id()))
                return
        else:
            self.redirect('/login')

class PostPage(base.BlogHandler):
    """
    This handler renders a single post page and handles all post related functions:
        Like posts, Increase/decrease total number of post likes
        Edit post
        Post comments - add, edit, delete
    """

    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)

        if not post:
            self.error(404)
            return

        # Get all the comments for this particular post
        comments = db.GqlQuery(
            "SELECT * FROM Comment WHERE ANCESTOR IS :1 ", post)

        for c in comments:
            if c.commentuser.key().id() == self.user.key().id():
                # Enable comment edit If the logged in user is also a comment
                # author
                c.editallowed = True
            else:
                c.editallowed = False
            c.put()

        # Render the post page
        if self.user and post.postuser.key().id() == self.user.key().id():
            self.render(
                "permalink.html",
                post=post,
                postuser=True,
                comments=comments)
        elif self.user:
            self.render(
                "permalink.html",
                post=post,
                postuser=False,
                comments=comments)
        else:
            self.redirect('/signup')

    def post(self, post_id):
        post_button = self.request.get("postbutton").split(',')
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)
        user_key = self.user.key()

        # When the user clicks 'like'
        if post_button[0] == "like":
            # If the user already liked the post, decrease likes_total (unlike
            # post)
            if self.user.key().id() != post.postuser.key().id():
                if user_key in post.likedby:
                    post.likedby.remove(user_key)
                    post.likes_total -= 1
                    post.put()
                else:
                    # Increase the likes_total, and append the user to 'likedby'
                    # list
                    post.likes_total += 1
                    post.likedby.append(user_key)
                    post.put()
                self.redirect('/blog/%s' % str(post.key().id()))
                return

        elif post_button[0] == "delete":
            if self.user.key().id() != post.postuser.key().id():
                post.delete()
                self.redirect('/')
                return
            else:
                self.redirect('/login')
                return

        # Add new comment to the post
        elif post_button[0] == "comment":
            if self.user:
                comment_text = self.request.get("comment_text")
                commentuser = self.user
                newcomment = Comment(
                    parent=post,
                    commentuser=commentuser,
                    commenttext=comment_text)
                newcomment.put()
                self.redirect('/blog/%s' % str(post.key().id()))
                return
            else:
                self.redirect('/login')
                return

        # Edit existing post comment
        elif post_button[0] == "editcomment":
            key = db.Key.from_path(
                'Comment', int(
                    post_button[1]), parent=post.key())
            c = db.get(key)
            # If the logged in user is also the comment author, open the
            # comment in edit mode
            if c.commentuser.key().id() == self.user.key().id():
                c.editmode = True
                c.put()
            self.redirect('/blog/%s' % str(post.key().id()))
            return

        # Delete existing comment
        elif post_button[0] == "deletecomment":
            key = db.Key.from_path(
                'Comment', int(
                    post_button[1]), parent=post.key())
            c = db.get(key)
            if c and self.user.key().id() == c.commentuser.key().id():
                c.delete()
                self.redirect('/blog/%s' % str(post.key().id()))
                return
            else:
                self.redirect('/login')
                return

        # Submit the edited comment to the db
        elif post_button[0] == "submitcommentedit":
            key = db.Key.from_path('Comment', int(post_button[1]), parent=post.key())
            c = db.get(key)
            if c and self.user.key().id() == c.commentuser.key().id():
                c.commenttext = self.request.get("comment_edit_text")
                c.editmode = False
                c.put()
                self.redirect('/blog/%s' % str(post.key().id()))
                return

        else:
            comments = db.GqlQuery(
                "SELECT * FROM Comment WHERE ANCESTOR IS :1 ", post)
            for c in comments:
                c.editmode = True
                c.put()
                self.redirect('/blog/%s' % str(post.key().id()))
