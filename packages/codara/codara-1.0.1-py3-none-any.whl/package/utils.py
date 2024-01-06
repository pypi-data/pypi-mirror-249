import sys
import threading
import time


def format_branch_name(branch_name):
    return branch_name.replace('/', '-')


def rotating_spinner():
    spinner_sequence = ['|', '/', '-', '\\']
    colors_sequence = ['\033[91m', '\033[93m', '\033[92m', '\033[94m', '\033[95m']  # Red, Yellow, Green, Blue, Magenta
    while True:
        for color in colors_sequence:
            for spinner in spinner_sequence:
                yield f"{color}{spinner}\033[0m"


def spinning_loader(task_done: threading.Event):
    spinner = rotating_spinner()
    while not task_done.is_set():
        sys.stdout.write(next(spinner))
        sys.stdout.flush()
        time.sleep(0.1)  # Adjust the speed as needed
        sys.stdout.write('\b')


def print_codara_ascii_message():
    print('\n\n')
    print('*******************************************************')
    print('*                                                     *')
    print('*  ██████╗ ██████╗ ██████╗  █████╗ ██████╗  █████╗    *')
    print('*  ██╔════╝██╔═══██╗██╔══██╗██╔══██╗██╔══██╗██╔══██╗  *')
    print('*  ██║     ██║   ██║██║  ██║███████║██████╔╝███████║  *')
    print('*  ██║     ██║   ██║██║  ██║██╔══██║██╔══██╗██╔══██║  *')
    print('*  ╚██████╗╚██████╔╝██████╔╝██║  ██║██║  ██║██║  ██║  *')
    print('*  ╚═════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   *')
    print('*                                                     *')
    print('*       You\'ve been successfully authenticated.       *')
    print('*                                                     *')
    print('*******************************************************')
    print('\n\n')
