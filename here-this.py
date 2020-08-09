#!/usr/bin/env python3
#
# MIT License
#
# Copyright (c) 2020 Stefaan Lippens
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import logging
import os
import re
import subprocess
import sys
import time


class HereThisException(Exception):
    pass


_log = logging.getLogger("here-this")


def main(argv):
    # logging.basicConfig(level=logging.DEBUG)
    command = " ".join(argv[1:])
    session_name = "here-this-{c}-{w}".format(
        c=re.sub(r'[^a-zA-Z0-9]+', '', command)[:16],
        w=re.sub(r'[^a-zA-Z0-9]+', '', os.getcwd())[-16:]
    )
    here_this(session_name, command)


def run(command: list, *args, **kwargs):
    _log.debug("Running: {c!r}".format(c=command))
    cp = subprocess.run(command, *args, **kwargs)
    _log.debug(repr(cp))
    return cp


def here_this(session_name: str, command: str):
    # Check if session is already running (and check if tmux is available)
    try:
        p_has = run(["tmux", "has-session", "-t", session_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        raise HereThisException("Failed to run 'tmux'. Is it installed?")

    if p_has.returncode != 0:
        print("Starting new tmux session {s!r} in background with command {c!r}".format(s=session_name, c=command))
        p_new = run(["tmux", "new-session", "-s", session_name, "-d", command])
        if p_new.returncode == 0:
            time.sleep(1)
            show_info(session_name, capture_title="Launched new tmux session with initial output:")
        else:
            raise HereThisException("Failed to launch new tmux session.")
    else:
        print("tmux session {s!r} is already running.".format(s=session_name))
        show_info(session_name, capture_title="Current output:")


def show_info(session_name: str, capture_title: str = "Current output:"):
    """Show info about running session"""
    p_capture = run(["tmux", "capture-pane", "-p", "-t", session_name], stdout=subprocess.PIPE)
    if p_capture.returncode == 0:
        print(capture_title)
        print("-" * 70)
        print(re.sub(r"\n+", "\n", p_capture.stdout.decode('ascii')))
        print("-" * 70)
        print("To re-attach:")
        print("    tmux attach -t {s}".format(s=session_name))
        print("To dump latest output/logs:")
        print("    tmux capture-pane -p -t {s}".format(s=session_name))
    else:
        raise HereThisException("tmux session {s!r} not running (anymore).".format(s=session_name))


if __name__ == "__main__":
    main(sys.argv)
