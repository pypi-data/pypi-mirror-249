import sys

from logging import Handler, LogRecord

from kilmlogger.services.scribe.client import ScribeClient


class GRPCEventStreamingHandler(Handler):
    def __init__(self, client: ScribeClient = ScribeClient()):
        """
        Initialize the handler.

        If stream is not specified, sys.stderr is used.
        """
        Handler.__init__(self)
        self._client = client

    def emit(self, record: LogRecord):
        self.acquire()
        try:
            self._client.log(
                msg=record.msg,
            )
        except Exception:
            sys.stdout.write("--- Logging error ---\n")
        finally:
            self.release()
