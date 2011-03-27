import zmq, threading, time, logging, msgpack

CONTEXT = zmq.Context()
ZNull = zmq.Message(None)

# multi helpers # {{{
def recv_multi(sock):
    parts = []
    while True:
        parts.append(sock.recv())
        if not sock.getsockopt(zmq.RCVMORE): break
    return parts

def send_multi(sock, parts, reply=None):
    if reply is not None:
        parts[-1] = reply
    for part in parts[:-1]:
        sock.send(part, zmq.SNDMORE)
    sock.send(parts[-1], 0)
# }}}

logger = logging.getLogger("zums.ZReplier")
class NoReply(Exception): pass

# ZReplier # {{{
class ZReplier(threading.Thread):

        def __init__(self, bind):
            super(ZReplier, self).__init__()
            self.shutdown_event = threading.Event()
            self.daemon = True
            self.bind = bind
            self.stats = {}
            self.stats["started_on"] = time.asctime()

        def thread_init(self):
            self.socket = CONTEXT.socket(zmq.XREP)
            try:
                self.socket.bind(self.bind)
            except zmq.ZMQError, e:
                print e, "while binding on", self.bind
                self.shutdown_event.set()
                raise

        def thread_quit(self):
            self.socket.close()

        def reply(self, message):
            if message == "shutdown":
                self.shutdown_event.set()
                logger.warn("shutdown")
                self.increment_stats_counter("shutdown")
                return "shutting down"
            if message == "stats":
                logger.info("stats")
                self.increment_stats_counter("stats")
                return msgpack.dumps(self.stats)
            self.increment_stats_counter("no_reply")
            raise NoReply

        def increment_stats_counter(self, counter_name):
            if counter_name not in self.stats:
                self.stats[counter_name] = 0
            self.stats[counter_name] += 1

        def run(self):
            self.thread_init()

            print self.__class__.__name__, "listening on %s." % self.bind


            while not self.shutdown_event.isSet():
                parts = recv_multi(self.socket)

                self.increment_stats_counter("requests")

                if len(parts) != 3:
                    logger.warn(
                        "Expected 3 parts, got %s: %s" % (len(parts), parts)
                    )
                    send_multi(self.socket, parts, "BAD MESSAGE")
                    continue

                message = parts[2]

                try:
                    send_multi(self.socket, parts, self.reply(message))
                except NoReply:
                    logger.info("NoReply for: %s" % message)
                    send_multi(self.socket, parts, "Unknown command.")
                except Exception, e:
                    logger.exception("Exception %s for: %s" % (e, message))
                    send_multi(self.socket, parts, "exception: %s" % e)

            self.thread_quit()

        def shutdown(self):
            socket = CONTEXT.socket(zmq.REQ)
            socket.connect(self.bind)

            socket.send("shutdown")
            recv_multi(socket)
            socket.close()

        def loop(self):
            self.start()
            try:
                while True:
                    self.shutdown_event.wait(1)
                    if self.shutdown_event.isSet():
                        print "Terminating after remote signal."
                        break
            except KeyboardInterrupt:
                print "Terminating gracefully... "
                self.shutdown()
                self.join()
                print "Terminated."
# }}}

def query_maker(bind):
    socket = CONTEXT.socket(zmq.REQ)
    socket.connect(bind)

    def query(*args, **kw):
        if args and kw:
            cmd = "%s:%s" % ( ":".join(args), msgpack.dumps(kw))
        elif args:
            cmd = ":".join(args)
        elif kw:
            cmd = msgpack.dumps(kw)
        else:
            cmd = ""
        socket.send(cmd)
        return socket.recv()

    return query

