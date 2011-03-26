# imports and config # {{{
from zreplier import ZReplier, query_maker
import bsddb, time, msgpack, logging

ZUMS_BIND = "tcp://127.0.0.1:7979"
logger = logging.getLogger("zumsd")
# }}}

# BDBSessionStore # {{{
class BDBSessionStore:
    def __init__(self, db_file="./sessions.bdb"):
        self.db_file = db_file
        self.db = bsddb.hashopen(db_file)
        print "BDBSessionStore initialized with %s, containing %s sessions." % (
            db_file, len(self.db)
        )

    def create(self):
        session = {}
        sid = ""
        session["sessionid"] = sid
        session["created_on"] = time.time()
        self.db[sid] = msgpack.dumps(session)
        return sid

    def get(self, sid):
        return self.db[sid]

    def set(self, sid, **kw):
        kw.pop("sessionid", None) # ignore sessionid, it can not be changed
        session = msgpack.loads(self.db[sid])
        session.update(kw)
        session = msgpack.dumps(session)
        self.db[sid] = session
        return session

    def exists(self, sid):
        return sid in self.db # and checks TODO

    def delete(self, sid):
        if sid in self.db: del self.db[sid]
# }}}

sessions = BDBSessionStore()

# ZUMSServer # {{{
class ZUMSServer(ZReplier):
    def reply(self, line):
        if line == "session_create":
            return sessions.create()
        if line.startswith("session_get:"):
            parts = line.split(":")
            return sessions.get(parts[1])
        if line.startswith("session_set:"):
            parts = line.split(":")
            return sessions.set(parts[1], parts[2])
        if line.startswith("session_create:"):
            parts = line.split(":")
            if sessions.exists(parts[1]): return "ZUMS.SessionExists"
            return sessions.set(parts[1], parts[2])
        if line.startswith("session_delete:"):
            parts = line.split(":")
            sessions.delete(parts[1])
            return "OK"
        return super(ZUMSServer, self).reply(line)
# }}}

query = query_maker(bind=ZUMS_BIND)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    ZUMSServer(ZUMS_BIND).loop()
