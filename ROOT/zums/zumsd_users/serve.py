import os, argparse

try:
    from cherrypy.wsgiserver import CherryPyWSGIServer
except ImportError:
    from zums.zumsd_users.wsgiserver import CherryPyWSGIServer

def main():
    parser = argparse.ArgumentParser(
        description='zmq based session and user manager for web applications.'
    )
    parser.add_argument(
        "-i", "--ip", default="0.0.0.0", 
        help="listen on this ip (default: 0.0.0.0)"
    )
    parser.add_argument(
        "-p", "--port", default=8088, type=int,
        help="listen on this port (default: 8088)"
    )
    parser.add_argument(
        "-s", "--settings", default="zums.zumsd_users.settings",
        help="settings module to use (default: zums.zumsd_users.settings)"
    )
    parser.add_argument(
        "-t", "--templates", default="./ROOT/templates", 
        help="location of templates (default: ./ROOT/templates)"
    )
    parser.add_argument(
        "-d", "--debug", default=False, action="store_true",
        help="run in debug mode, default is in settings file"
    )
    parser.add_argument(
        "--init", default=False, action="store_true", 
        help="create user database"
    )
    args = parser.parse_args()

    os.environ["DJANGO_SETTINGS_MODULE"] = args.settings

    from django.core.management import call_command
    from django.core.handlers.wsgi import WSGIHandler
    from django.conf import settings

    if args.init:
        call_command('syncdb', interactive=True)
        return

    if args.templates:
        settings.TEMPLATE_DIRS = (args.templates,)
    if args.debug:
        settings.DEBUG = True

    server = CherryPyWSGIServer((args.ip, args.port), WSGIHandler())
    print "Started http server on %s:%s." % (args.ip, args.port)
    print "Hit ^C to exit."

    try:
        server.start()
    except KeyboardInterrupt:
        print "Shutting down gracefully."
        server.stop()

