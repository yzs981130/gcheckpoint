import signal


class GracefulKiller:
    kill_now = False
    callback_function = None
    args = None

    def __init__(self, _callback, *args):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)
        self.callback_function = _callback
        self.args = args

    def exit_gracefully(self, signum, frame):
        self.kill_now = True
        if self.callback_function is not None:
            self.callback_function(self.args)
