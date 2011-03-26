# imports and config # {{{
from zutils import ZReplier, query_maker, process_command
import bsddb, time
import json as msgpack

ZUMS_BIND = "tcp://127.0.0.1:7979"
# }}}

# BDBSessionStore # {{{
class BDBSessionStore:
    def __init__(self, db_file="./sessions.bdb"):
        self.db_file = db_file
        self.db = bsddb.hashopen(db_file)
        print "BDBSessionStore initialized with %s, containing %s sessions." % (
            db_file, len(self.db)
        )

    def start_session(self):
        session = {}
        sid = zid_query("get")
        session["sessionid"] = sid
        session["created_on"] = time.time()
        self.db[sid] = msgpack.dumps(session)
        return sid

    def get_session(self, sid):
        return self.db[sid]

    def save_session(self, sid, **kw):
        kw.pop("sessionid", None) # ignore sessionid, it can not be changed
        session = msgpack.loads(self.db[sid])
        session.update(kw)
        session = msgpack.dumps(session)
        self.db[sid] = session
        return session
# }}}

sessions = BDBSessionStore()

# ZUMSServer # {{{
class ZUMSServer(ZReplier):
    def reply(self, line):
        arguments = process_command(line)
        print arguments
        if arguments == "start_session":
            return self.session_store.start_session()
        if len(arguments) == 2 and arguments[0] == "get_session":
            return self.session_store.get_session(arguments[1])
        if len(arguments) == 3 and arguments[0] == "save_session":
            return self.session_store.save_session(arguments[1], **arguments[2])
        return super(ZUMSServer, self).reply(line)
# }}}

query = query_maker(bind=ZUMS_BIND)

if __name__ == "__main__":
    ZUMSServer(ZUMS_BIND).loop()
