#!/bin/sh
python smokedns.py | tee -a dns.log.$(hostname)
