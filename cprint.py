import sys

def cprint(color, *args, **kwargs):
    colors = {
        'red': "\033[1;31m",
        'blue': "\033[1;34m",
        'cyan': "\033[1;36m",
        'yellow': "\033[33m",
        'green': "\033[0;32m",
        'reset': "\033[0;0m",
        'bold': "\033[;1m",
        'reverse': "\033[;7m",
    }
    if color in colors:
        sys.stdout.write(colors[color])
        print(*args, **kwargs)
        sys.stdout.write(colors['reset'])