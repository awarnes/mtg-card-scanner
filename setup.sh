#!/bin/bash

python3 -m venv scanner-venv &&
source scanner-venv/bin/activate &&
pip install -r requirements.txt