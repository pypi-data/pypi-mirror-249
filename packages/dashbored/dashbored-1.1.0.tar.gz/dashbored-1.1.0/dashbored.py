import argparse
from contextlib import contextmanager
import curses
from functools import partial
import importlib
import importlib.metadata
import inspect
import logging
import os
import re
import signal
import sys
import time
from typing import Callable
from typing import Dict
from typing import IO
from typing import Optional
from typing import List
from typing import Mapping
from typing import Any
from typing import Union

logger = logging.getLogger("dashbored")

class DataSource:

    def __init__(self, fetch: Callable[[], List[Mapping[str, str]]], freq: float):
        self._fetch: Callable[[], List[Mapping[str, str]]] = fetch
        self.freq: float = freq
        self.last_result: List[Mapping[str, str]] = self._fetch()
        self.last_update: float = time.time()

    def fetch(self):
        if self.last_update is not None:
            now = time.time()
            if now - self.last_update < self.freq:
                return self.last_result
        self.last_result = self._fetch()
        self.last_update = time.time()
        return self.last_result

class View:
    """ Draws the view """

    def __init__(self, fmt: str, data_source: DataSource):
        self.fmt = fmt
        self.data_source = data_source
        self.sort_by: Optional[str] = None

    def draw(self, window):
        (height, width) = window.getmaxyx()
        rows = self.data_source.fetch()
        if len(rows) == 0:
            return
        headers = {key:key for key in rows[0].keys() }
        window.chgat(curses.A_REVERSE)
        window.addstr(self.fmt.format(**headers), curses.A_REVERSE)
        window.move(1, 0)
        y = 1
        if self.sort_by is not None:
            rows = sorted(rows, key=lambda row: str(row.get(self.sort_by, "")).lower())
        for index, row in zip(range(height - 2), rows):
            window.addstr(self.fmt.format(**row))
            y += 1
            window.move(y, 0)
        window.move(height - 1, 0)
        window.addstr(" [s]ort")

def setup_redraw(screen, view: View):
    """ Setups up a signal handler for SIGWINCH to redraw """
    def redraw(signal, frame):
        screen.clear()
        view.draw(screen)
        screen.refresh()
    signal.signal(signal.SIGWINCH, redraw)
    view.draw(screen)
    screen.refresh()

@contextmanager
def init_screen(view: View):
    """ Initializes a screen and setups a draw if the
    window is resized.
    """
    try:
        screen = curses.initscr()
        curses.noecho()
        screen.keypad(True)
        curses.cbreak()
        setup_redraw(screen, view)
        yield screen
    except KeyboardInterrupt:
        pass
    finally:
        curses.nocbreak()
        screen.keypad(False)
        curses.echo()
        curses.endwin()

def sort_by(window, view: View):
    curses.nocbreak()
    curses.echo()
    (height, width) = window.getmaxyx()
    window.move(height - 1, 0)
    window.addstr("Sort by: ")
    view.sort_by = window.getstr().decode("utf-8")
    curses.cbreak()
    curses.noecho()
    signal.raise_signal(signal.SIGWINCH)

INDEX_COMMANDS: Dict[int, Callable[..., None]] = {}
INDEX_COMMANDS[ord('q')] = partial(sys.exit, 0)
INDEX_COMMANDS[ord('s')] = sort_by

def create(fmt: str, fetch: Callable[[], List[Mapping[str, str]]], fetch_freq: float):
    data_source = DataSource(fetch, fetch_freq)
    view = View(fmt, data_source)
    with init_screen(view) as window:
        while True:
            key = window.getch()
            if key in INDEX_COMMANDS:
                func = INDEX_COMMANDS[key]
                spec = inspect.getfullargspec(func)
                posargs = spec[0]
                kwargs = {}
                if "window" in posargs:
                    kwargs["window"] = window
                if "view" in posargs:
                    kwargs["view"] = view
                func(**kwargs)

            if (time.time() - data_source.last_update) >= fetch_freq:
                signal.raise_signal(signal.SIGWINCH)

SYSEXITS_DATAERR = 65
SYSEXITS_NOINPUT = 66
SYSEXITS_UNAVAILABLE = 69

def log_and_exit(message, code):
    logger.error(message)
    sys.exit(code)

def main():
    
    argparser = argparse.ArgumentParser()
    argparser.add_argument("data_source", metavar="data-source",
                           help="Data source")
    argparser.add_argument("--format", help="Row output format")
    argparser.add_argument("--freq", type=float, help="Frequency of fetch")
    argparser.add_argument("--verbose", "-v", help="Log verbosely to file")
    
    args = argparser.parse_args()
    if args.verbose:
        logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler(args.verbose)
        formatter = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    eps = importlib.metadata.entry_points(
            group='dashbored',
            name=args.data_source)

    if len(eps) == 1:
        module = eps[0].load()
    else:
        module = importlib.import_module(args.data_source) 

    fmt = args.format if args.format is not None \
            else getattr(module, "FORMAT", None)
    if fmt is None:
        log_and_exit("No format provided.", SYSEXITS_DATAERR)

    freq = args.freq if args.freq is not None\
            else getattr(module, "FREQUENCY", None)
    if freq is None:
        log_and_exit("No frequency provided.", SYSEXITS_DATAERR)

    fetch = getattr(module, "fetch", None)
    if fetch is None:
        log_and_exit("Defined 'fetch' does not exist.", SYSEXITS_UNAVAILABLE)
    if not callable(fetch):
        log_and_exit("Defined 'fetch' is not callable.", SYSEXITS_DATAERR)
    create(fmt, fetch, freq)
   
if __name__ == '__main__':
    main()
