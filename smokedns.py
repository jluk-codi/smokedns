#!/usr/bin/python
from __future__ import print_function
import time
import calendar
from multiprocessing.dummy import Pool as ThreadPool
import subprocess
import yaml
import json
import socket

def probe_dns(data):
    while data['records']:
        for record in data['records']:
            tstamp = str(calendar.timegm(time.gmtime()))
            status = 'OK'
            try:
                result = subprocess.check_output(["host", record, data['ns']], stderr=subprocess.STDOUT)
                result = result.decode('utf8')
                result = result.splitlines()[5]
            except subprocess.CalledProcessError as cpe:
                ret = cpe.returncode
                result = cpe.output.decode('utf8').strip()
                status = 'ERROR'
            #print("DNS probe finished:", record, "@", data['ns'], result)
            log = {"status": status, "time": tstamp, "output": result, "ns": data['ns'], "query": record, "src": data['src']}
            print(json.dumps(log))
        time.sleep(data['sleep'])
    print("probe_dns exiting")
    return 

def calculateParallel(numbers, threads=2):
    return results

if __name__ == "__main__":
    threads = 2
    cfg = yaml.load(open('cfg.yaml', 'r'))
    threads = cfg.get("threads", 2)
    ns_list = cfg.get("ns_list", [])
    sleep = cfg.get("sleep", 2)
    src = cfg.get("src", socket.gethostname())
    records = cfg.get("records", [])
    data = [{"ns": ns, "sleep": sleep, "records": records, "src": src} for ns in ns_list]
    pool = ThreadPool(threads)
    results = pool.map(probe_dns, data)
    pool.close()
    pool.join()
