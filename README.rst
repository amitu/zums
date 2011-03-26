ZUMS
====

Django has its way of handling users and sessions. Ruby has its own. Java
servlets has their own. And so on. Not good.

Good: there is a ZeroMQ service that programs written in any language can
interact with, this service maintains users and sessions. The web framework of
your choice passes sessionid from sessionid named cookie, gets session, gets
logged in user etc. Nginx routes www.example.com/accounts to zums service,
which happens to be a web server too, and nginx routes www.example.com/blog to
wordpress based blog, and www.example.com/dashboard/ to a ruby on rails project
and www.example.com/* to django. If a user signs in by going to
www.example.com/accounts/login/, sessionid cookie is set, and if user then goes
to www.example.com/blog, wordpress plugin for zums interacts with zums over
zeromq and fetches user/session data.
