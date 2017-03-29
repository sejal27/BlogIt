import webapp2
import jinja2
import os
import user
import secure

# Create the Jinja environment
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)


# Global render_str function that gets the template from the jinja environment and returns the rendered string from the template.
def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)


class BlogHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        params['user'] = self.user
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))
        
    #Makes cookie value secure and sets the secure cookie
    def set_secure_cookie(self,name,val):
        cookie_val = secure.make_secure_val(val)
        self.response.headers.add_header('Set-Cookie', '%s=%s; Path=/' % (name, cookie_val))

    #Reads the cookie for name, and returns the secure value, if the cookie exists and passes the security check
    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and secure.check_secure_val(cookie_val)

    # check if the user is logged in and set the current user to that
    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and user.User.by_id(int(uid))

    # Set the secure cookie for user login
    def login(self,user):
        self.set_secure_cookie('user_id', str(user.key().id()))

    # Clear the user_id cookie
    def logout(self):
        self.response.headers.add_header('Set-Cookie','user_id=; Path=/')