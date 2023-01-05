#!/bin/bash 

set -eux 

gunicorn -w 4 -b 0.0.0.0:10000 "main:create_app()"

