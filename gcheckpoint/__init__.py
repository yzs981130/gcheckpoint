import signal
import traceback
import torch.distributed


class GracefulKiller:
    kill_now = False
    callback_function = None
    args = None

    def __init__(self, _callback, *args):
        signal.signal(signal.SIGINT, self.exit_handler)
        signal.signal(signal.SIGTERM, self.exit_handler)
        self.callback_function = _callback
        self.args = args

    def exit_handler(self, signum, frame):
        self.kill_now = True
        '''
        if self.callback_function is not None:
            self.callback_function(*self.args)
        traceback.print_stack(frame)
        '''
    def check_exit(self, *args):
        is_main = not torch.distributed.is_initialized() or torch.distributed.get_rank() == 0
        if self.kill_now and is_main:
            print('kill now')
            self.callback_function(*args)
