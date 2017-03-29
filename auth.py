import base
import re
import user

#check valid username, password, and email
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

class Signup(base.BlogHandler):

    def get(self):
        self.render("signup-form.html")

    def post(self):
        have_error = False
        self.username = self.request.get('username')
        self.password = self.request.get('password')
        self.verify = self.request.get('verify')
        self.email = self.request.get('email')

        params = dict(username = self.username,
                      email = self.email)

        if not valid_username(self.username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if not valid_password(self.password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif self.password != self.verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not valid_email(self.email):
            params['error_email'] = "That's not a valid email."
            have_error = True

        if have_error:
            self.render('signup-form.html', **params)
        else:
            self.done()

    #each subclass of Signup an override this method. If the override is not implemented, the error occurs.
    def done(self, *a, **kw):
        raise NotImplementedError


class Register(Signup):
    #Register overrides done, and adds user details to db.
    def done(self):
        #Error occurs if the user name already exists.
        u = user.User.by_name(self.username)
        if u:
            msg = 'That user already exists.'
            self.render('signup-form.html', error_username = msg)
        else:
            u = user.User.register(self.username, self.password, self.email)
            u.put()

            self.login(u)
            self.redirect('/')

class Login(base.BlogHandler):
    def get(self):
        self.render('login-form.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        # Check if username and password combination is correct
        # Set the cookie for user_id
        u = user.User.login(username, password)
        if u:
            self.login(u)
            self.redirect('/welcome')
        else:
            msg='Invalid Login'
            self.render('login-form.html', error=msg)

class Logout(base.BlogHandler):
    def get(self):
        self.logout() # Clear cookies on logout
        self.redirect('/login')

class Welcome(base.BlogHandler):
    def get(self):
        if self.user:
            self.render('welcome.html', username=self.user.name, newlogin=True)
        else:
            self.redirect('/signup')