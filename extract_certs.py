#!/usr/bin/env python
import csv
import re
from datetime import datetime
from time import sleep
import multiprocessing
import json
import sys
import urllib2


def parse_cert():
    data = []
    content = []
    with open("banking_click_data.csv", "rU") as myfile:
        for line in myfile:
            content.append(line)
    # reader = csv.DictReader(content)
    count = 0
    for row in content:
        count += 1
        items = row.split(',')
        d = {'src_url_tx': items[0].strip(), 'src_prod_nm': items[1].strip()}
        begin = 0
        end = 0
        s0 = d['src_url_tx']
        if not s0:
            continue
        if s0.find('/blog') > -1:
            d['isBlog'] = '1'
        else:
            d['isBlog'] = '0'
        s1 = d['src_prod_nm']
        if re.search("\d", s1) is None:
            continue
        begin = re.search("\d", s1).start(0)
        for i in xrange(begin, len(s1)):
            if not s1[i].isdigit():
                end = i
                break
        d['name'] = s1[0:begin]
        d['certNumber'] = s1[begin:end]
        d['type'] = s1[end:end+2]
        data.append(d)
    return data


def output_json_to_csv(data):
    with open("banking_click_certs.csv", "w") as myfile:
        myfile.write(','.join(data[0].keys()))
        myfile.write("\n")
        for row in data:
            myfile.write(','.join(val for key, val in row.iteritems()))
            myfile.write("\n")

if __name__ == "__main__":
    data = parse_cert()
    output_json_to_csv(data)
