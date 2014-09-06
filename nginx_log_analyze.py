#!/bin/env python
# vim:fileencoding=utf-8
import sys
import re
import ltsv

filename = sys.argv[1]
if len(sys.argv) > 2:
    sortkey = sys.argv[2]
else:
    sortkey = "avg"

logs = [log for log in ltsv.DictReader(open(filename))]
total_count = len(logs)

"""
 {'apptime': '0.051',
  'cache': '-',
  'forwardedfor': '-',
  'host': '127.0.0.1',
  'method': 'GET',
  'protocol': 'HTTP/1.1',
  'referer': '-',
  'reqsize': '89',
  'reqtime': '0.051',
  'runtime': '-',
  'size': '4650',
  'status': '200',
  'time': '27/Aug/2014:16:50:34 +0000',
  'ua': 'ISUCON Agent 2013',
  'uri': '/',
  'vhost': 'localhost'}
"""

reqtimes_of = {}
for log in logs:
    uri = re.sub(r'\d+', '', log["uri"])

    if not reqtimes_of.has_key(uri):
        reqtimes_of[uri] = []
    reqtimes_of[uri].append(log["reqtime"])

print "=== count ==="
print "%d (total)" % total_count
for uri, reqtimes in sorted(reqtimes_of.items(), key=lambda x:len(x[1]), reverse=True):
    count = len(reqtimes)
    print "%d (%3d%% ) %s" % (count, float(count)/total_count*100, uri)

print "=== reqtime ==="
result_of = {}
for uri, reqtimes in reqtimes_of.items():
    reqtimes = [float(x) for x in reqtimes]
    result_of[uri] = {
        "sum": sum(reqtimes),
        "avg": sum(reqtimes)/len(reqtimes),
        "max": max(reqtimes),
        "min": min(reqtimes),
        "med": (max(reqtimes)+min(reqtimes))/2,
    }

for uri, result in sorted(result_of.items(), key=lambda x:x[1][sortkey], reverse=True):
    print "{uri:<10}  avg:{avg:.3f}\tsum:{sum:.3f}\tmax:{max:.3f}\tmed:{med:.3f}\tmin:{min:.3f}".format(uri=uri, **result) 

