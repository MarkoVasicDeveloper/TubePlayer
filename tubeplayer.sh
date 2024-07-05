#!/bin/bash

if [ ! -d "TubePlayer" ]; then
  python3 -m venv TubePlayer
fi

source TubePlayer/bin/activate

python3 setup/install.py

python3 yt.py
