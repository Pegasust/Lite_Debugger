TRACE = False
DEBUG = False

def log_trace(*args):
    if TRACE:
        # Correctly separate args like print()
        print(' '.join(map(str, args)))

def log_debug(*args):
    if DEBUG:
        print(' '.join(map(str,args)))
