#!/usr/bin/env bash
nohup gunicorn -w 4 -b 0.0.0.0:5050 -k eventlet app:app &