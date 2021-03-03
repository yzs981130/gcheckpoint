import signal
import traceback
import torch
import torch.distributed


class GracefulKiller:
    kill_now = False
    callback_function = None

    last_saved_checkpoint = None

    def __init__(self, _callback):
        signal.signal(signal.SIGINT, self.exit_handler)
        signal.signal(signal.SIGTERM, self.exit_handler)
        self.callback_function = _callback

    def exit_handler(self, signum, frame):
        self.kill_now = True
        '''
        if self.callback_function is not None:
            self.callback_function(*self.args)
        traceback.print_stack(frame)
        '''
        if self.last_saved_checkpoint is not None:
            print('saving last checkpoint')
            torch.save(self.last_saved_checkpoint, 'last_checkpoint-autosave.pth.tar')

    def check_exit(self, saved_checkpoint, *args):
        self.last_saved_checkpoint = saved_checkpoint
        is_main = not torch.distributed.is_initialized() or torch.distributed.get_rank() == 0
        if self.kill_now and is_main:
            print('kill now')
            self.callback_function(saved_checkpoint, *args)
