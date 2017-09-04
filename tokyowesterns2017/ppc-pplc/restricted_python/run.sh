#!/bin/bash
cd $(dirname "$0")
/usr/bin/python2 $1.py 2> /dev/null | head --bytes=512 # Ubuntu 16.04(64bit) python-minimal package
