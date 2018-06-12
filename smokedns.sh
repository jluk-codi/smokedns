#!/bin/sh
python smokedns.py | tee dns.log.$(date +%s)
