import webapp2
import auth
import main

# import pdb; pdb.set_trace();

# Handlers
"""
Blog Handlers:
    main.BlogFront - Handler for Homepage
    main.NewPost - Handler for new post
    main.MyPosts - Handler to display posts by the logged in User
    Main.EditPost - Handler for editing an existing post
    auth.Register - Handler for new user registrations
    auth.login - Handler to handle login functionality
    auth.logout - Handler to handle logout functionality
"""
app = webapp2.WSGIApplication([('/', main.BlogFront),
                               ('/newpost', main.NewPost),
                               ('/blog/([0-9]+)', main.PostPage),
                               ('/user/([0-9]+)', main.MyPosts),
                               ('/blog/edit/([0-9]+)', main.EditPost),
                               ('/signup', auth.Register),
                               ('/login', auth.Login),
                               ('/logout', auth.Logout)
                               ],
                              debug=True)


def main():
    app.run()
