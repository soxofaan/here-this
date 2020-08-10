#!/bin/bash

# Always use port 8000 (risking collision) or just a random available one?
# python -m http.server 8000
python -m http.server 0

# Sleep a bit to allow capturing of initial failure messages.
sleep 3
