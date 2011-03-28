import os, argparse

try:
    from cherrypy.wsgiserver import CherryPyWSGIServer
except ImportError:
    from zums.zumsd_users.wsgiserver import CherryPyWSGIServer

def main():
    parser = argparse.ArgumentParser(
        description='zmq based session and user manager for web applications.'
    )
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", default=8088, type=int)
    parser.add_argument("--settings", default="zums.zumsd_users.settings")
    parser.add_argument("--init", default=False, action="store_true")
    args = parser.parse_args()
    os.environ["DJANGO_SETTINGS_MODULE"] = args.settings

    if args.init:
        from django.core.management import call_command
        call_command('syncdb', interactive=True)
    else:
        from django.core.handlers.wsgi import WSGIHandler
        server = CherryPyWSGIServer((args.host, args.port), WSGIHandler())
        print "Started http server on %s:%s." % (args.host, args.port)
        print "Hit ^C to exit."
        try:
            server.start()
        except KeyboardInterrupt:
            print "Shutting down gracefully."
            server.stop()

