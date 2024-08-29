#!/bin/bash

# Activate the virtual environment
source .venv/bin/activate

# Run main.py with all arguments passed through
python main.py "$@"
