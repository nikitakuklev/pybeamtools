import os
import threading


class RayMixin:
    def getattr(self, attr):
        return getattr(self, attr)

    def getattrs(self, attrs):
        return {x: getattr(self, x) for x in attrs}

    def get_pid(self):
        return os.getpid()

    def get_thread_id(self):
        return threading.get_ident()