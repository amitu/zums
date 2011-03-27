from django.contrib.sessions.backends.base import SessionBase, CreateError
from zums.zumsd import query
import msgpack

class SessionStore(SessionBase):
    """ Implements ZUMS session store. """

    def __init__(self, session_key=None):
        super(SessionStore, self).__init__(session_key)

    def load(self):
        return msgpack.loads(query("session_get:%s" % self.session_key))

    def create(self):
        self.session_key = query("session_create")
        self.modified = True
        self._session_cache = {}

    def exists(self, session_key):
        return bool(query("session_exists:%s" % session_key))

    def save(self, must_create=False):
        if must_create:
            if query(
                "session_create:%s:%s" % (
                    self.session_key,
                    msgpack.dumps(self._get_session(no_load=must_create))
                )
            ) == "ZUMS.SessionExists":
                raise CreateError
        else:
            query(
                "session_set:%s:%s" % (
                    self.session_key,
                    msgpack.dumps(self._get_session(no_load=must_create))
                )
            )

    def delete(self, session_key=None):
        if session_key is None:
            if self._session_key is None:
                return
            session_key = self._session_key
        query("session_delete:%s" % session_key)
