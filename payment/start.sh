#!/bin/sh
uvicorn main:app --host 127.0.0.1 --port 8001 & # need to change to 0.0.0.0 
python consumer.py