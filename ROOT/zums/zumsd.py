# imports and config # {{{
from zreplier import ZReplier, query_maker
import bsddb, time, logging, os, random, hashlib, msgpack, argparse

if hasattr(random, 'SystemRandom'):
    randrange = random.SystemRandom().randrange
else:
    randrange = random.randrange

ZUMS_BIND = "tcp://127.0.0.1:7979"
logger = logging.getLogger("zumsd")
MAX_SESSION_KEY = 18446744073709551616L     # 2 << 63
# }}}

# BDBSessionStore # {{{
class BDBSessionStore:
    def __init__(self, db_file="./sessions.bdb"):
        self.db_file = db_file
        self.db = bsddb.hashopen(db_file)
        print "BDBSessionStore initialized with %s, containing %s sessions." % (
            db_file, len(self.db)
        )

    def get_next_key(self):
        try:
            pid = os.getpid()
        except AttributeError:
            # No getpid() in Jython, for example
            pid = 1
        while 1:
            session_key = hashlib.md5(
                "%s%s%s" % (randrange(0, MAX_SESSION_KEY), pid, time.time())
            ).hexdigest()
            if not self.exists(session_key):
                break
        return session_key

    def create(self):
        session = {}
        sid = self.get_next_key()
        session["sessionid"] = sid
        session["created_on"] = time.time()
        self.db[sid] = msgpack.dumps(session)
        return sid

    def get(self, sid):
        return self.db[sid]

    def set(self, sid, value):
        data = msgpack.loads(value)
        data.pop("sessionid", None) # ignore sessionid, it can not be changed
        self.db[sid] = msgpack.dumps(data)
        return "OK"

    def exists(self, sid):
        return sid in self.db # and checks TODO

    def delete(self, sid):
        if sid in self.db: del self.db[sid]
# }}}

# ZUMSServer # {{{
class ZUMSServer(ZReplier):
    def __init__(self, bind, sessionfile):
        super(ZUMSServer, self).__init__(bind)
        self.sessionfile = sessionfile

    def thread_init(self):
        super(ZUMSServer, self).thread_init()
        self.sessions = BDBSessionStore(self.sessionfile)

    def reply(self, line):
        if line == "session_create":
            return self.sessions.create()
        if line.startswith("session_get:"):
            parts = line.split(":")
            return self.sessions.get(parts[1])
        if line.startswith("session_exists:"):
            parts = line.split(":")
            return "yes" if self.sessions.exists(parts[1]) else ""
        if line.startswith("session_set:"):
            parts = line.split(":", 2)
            return self.sessions.set(parts[1], parts[2])
        if line.startswith("session_create:"):
            parts = line.split(":", 2)
            if self.sessions.exists(parts[1]): return "ZUMS.SessionExists"
            return self.sessions.set(parts[1], parts[2])
        if line.startswith("session_delete:"):
            parts = line.split(":")
            self.sessions.delete(parts[1])
            return "OK"
        return super(ZUMSServer, self).reply(line)
# }}}

query = query_maker(bind=ZUMS_BIND)

def main():
    parser = argparse.ArgumentParser(
        description='zmq based session and user manager for web applications.'
    )
    parser.add_argument("--bind", default=ZUMS_BIND)
    parser.add_argument("--sessionfile", default="./sessions.bdb")
    arguments = parser.parse_args()
    ZUMSServer(arguments.bind, arguments.sessionfile).loop()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    try:
        main()
    except Exception:
        logger.exception("Exception in main")
        raise
