import gcheckpoint
import time


def test_handler(*args):
    for arg in args:
        print(arg)


if __name__ == '__main__':
    state_dict = {'a': 1, 'b': 2}
    state_dict2 = {'c': 1, 'd': 2}
    killer = gcheckpoint.GracefulKiller(test_handler, state_dict, state_dict2)
    while True:
        state_dict['a'] = 2
        if killer.kill_now:
            print("End of the program. I was killed gracefully :)")
            exit()
        time.sleep(1)
        print("doing something in a loop ...")
