import webapp2
import auth
import main

# import pdb; pdb.set_trace();

############################### Handlers #########################################

app = webapp2.WSGIApplication([('/',main.BlogFront),
                               ('/signup', auth.Register),
                               ('/welcome', auth.Welcome),
                               ('/login', auth.Login),
                               ('/logout', auth.Logout),
                               ('/newpost', main.NewPost),
                               ('/blog/([0-9]+)', main.PostPage),
                               ('/user/([0-9]+)', main.MyPosts),
                               ('/welcome', auth.Welcome),
                               ('/blog/edit/([0-9]+)', main.EditPost)],
                              debug=True)
def main():
    app.run()