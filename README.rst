ZUMS
====

One auth to rule them all.

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

So I wrote this service. This is actually a collection of services and plugins.

First install this service::

    $ easy_install zums

You will have to run the zumsd daemon too.::

    $ zumsd --help

And create a database for users.::

    $ zumsd --init

This will ask for a database engine, location, hostname, username etc and
create the tables for you. [TODO: not done yet].

The point to note is that your users are stored in this data base, and are
accessible over a zeromq api too all languages and frameworks, not just django.

Using zums with Django Projects
-------------------------------

Using it is trivial in a django project, look at the settings.py file in
zums_dj_example_project::

    SESSION_ENGINE = "zums.django_backends.session"
    AUTHENTICATION_BACKENDS = ["zums.django_backends.auth.ZUMSBackend"]

These two settings is all you need to do, and your django project is getting
all the benefits of zums, which is, it can co exist with subprojects writter in
other languages.

Note: the auth backend creates a local copy of User in your django database, so
foreign key to user etc still work without any changes.

The only thing you need to know when using this service/backend vs normal
django project is that not all users may not be there in your database, nor are
they gauranteed to be in sync with actual master database.

It is trivial to solve the above two by writing some zumsd extensions described
elsewhere. [TODO: this is not done yet]


Using zums with non Django Projects
-----------------------------------

You will have to do a little more work, and hopefully someone will write
session backends and auth backends for the programming language and web
framework of your choice. If not, you can implement the simple zeromq api for
zumsd daemon, and write your own session and auth handling code.

Zumsd ZeroMQ API
----------------

TBD

Zumsd Extensions
----------------

Zumsd can be extended by writing plugins. Zumsd talks to plugins, over zeromq,
so plugins can be written in any language one wishes too.

Plugins are quite simple, they just subscribe (zmq.SUB) to messages that zumsd
sends over, they then user zumsd ZeroMQ api mentioned above to update data
managed by zumsd or do whatever they want.

For simplicty zumsd supports python plugins, they live within the zumsd
process, and need not be managed as separate service.

TBD
