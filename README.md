
# Here this!


`here-this` is a simple wrapper script around `tmux` 
to easily launch a (long running) command
in a background tmux session.


For example, Python has a built-in simple HTTP server 
to statically serve your current working directory
and can be invoked with just `python -m http.server`.
However, because this server runs in an infinite loop,
it will hijack your current shell session until you kill it.

`here-this` allows to launch it 
in a background tmux session instead, 
offering these features:

- your interactive shell **isn't hijacked**
- while it feels like launching something in the background,
  you can still **re-attach** to the tmux session
  and interact with the process interactively,
  e.g. scroll through the stdout/stderr logs, enter a password,
  kill the process, ...


Of course, any operating system worth its salt provides
"big boy" tools for running background services 
and daemons (init, systemd, launchd, ...)
but sometimes you just want a quick and ~~dirty~~ easy
solution to run something ad-hoc in a semi-background fashion.


## Installation and dependencies

`here-this.py` is a simple Python script and requires:

- **Python 3.5** or higher. 
  The script just requires the Python standard library,
  so a vanilla Python environment should do the trick,
  no need to set up virtual envs of some sort.
- **`tmux`, the terminal multiplexer**, to do the real work.
  This tool is usually not available by default,
  so install it through the package manager of your OS.
  
Because it is a simple one-file Python script, you can just put
it in a location that is convenient for your workflow.
Use, as desired, some combination of the following tips:

- copy or symlink `here-this.py` to a destination folder
  of your liking
- drop the `.py` extension, if you don't like that cruft 
  in command line tools
- make sure its containing folder is in your `PATH` 
  to have `here-this` it at your fingertips at all time.


## Usage

### Direct usage

You can use `here-this` directly by passing it a command,
like this:

    here-this.py python3 -m http.server

which will respond with something like this:

    Starting new tmux session 'here-this-python3mhttpserv-pathtosomewhere' in background with command 'python3 -m http.server'
    Launched new tmux session with initial output:
    ----------------------------------------------------------------------
    Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
    
    ----------------------------------------------------------------------
    To re-attach:
        tmux attach -t here-this-python3mhttpserv-pathtosomewhere
    To dump latest output/logs:
        tmux capture-pane -p -t here-this-python3mhttpserv-pathtosomewhere

This example illustrates a couple of things that `here-this` provides:

- a descriptive tmux **session name** is automatically derived from the command
  and working directory
- the **initial output** of the command is shown 
- example commands are shown of how to **re-attach** or get a **dump the latest output**

You can also pass multiple commands as a single string snippet:

    here-this.py 'for i in 1 2 3; do echo $i hello; sleep $i; done'

### Reusable scripts and aliases

TODO

## Troubleshooting

TODO append sleep