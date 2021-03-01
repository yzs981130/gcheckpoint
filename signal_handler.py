import signal
import time


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


def test_handler(*args):
    for arg in args:
        print(arg)


if __name__ == '__main__':
    state_dict = {'a': 1, 'b': 2}
    state_dict2 = {'c': 1, 'd': 2}
    killer = GracefulKiller(test_handler, state_dict, state_dict2)
    while True:
        state_dict['a'] = 2
        if killer.kill_now:
            print("End of the program. I was killed gracefully :)")
            exit()
        time.sleep(1)
        print("doing something in a loop ...")
