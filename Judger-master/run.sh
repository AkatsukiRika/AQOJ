#!/bin/bash
while [ true ]; do
/bin/sleep 1
PYTHONIOENCODING=utf-8 python3 daemon.py
done
