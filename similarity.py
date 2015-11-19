#!/usr/bin/env python
import csv
from datetime import datetime
from time import sleep
import multiprocessing
import json
import sys
import urllib2

fields = {
    'CERT': 'certNumber',
    'NAME': 'name',
    'OFFNAME': 'branchName',
    'ZIP': None,
    'MAINOFF': None,
    'asset_size': 0
}

post_fields = [
    'post_date',
    'post_title',
    'post_name',
    'post_modified'
]

base_url = 'https://odata.fdic.gov/v1/financial-institution/Institution?$format=json&$filter=certNumber%20eq%20{0}'


def get_raw_api_data(branch_type):
    branches = []
    counter = 0
    previous = datetime.now()
    if branch_type == 'FDIC':
        try:
            reader = None
            with open("OFFICES2_ALL.CSV", "r") as myfile:
                reader = csv.DictReader(myfile)
                p = multiprocessing.Pool()
                branches = p.map_async(multi_call_api, reader, chunksize=1)
                p.close()
                while (True):
                    remaining = branches._number_left
                    print "{0} tasks left".format(remaining)
                    if branches.ready() or remaining == 0: break
                    sleep(1)
                # for row in reader:
                #     counter += 1
                #     if counter % 100 == 0:
                #         current = datetime.now()
                #         print str(counter) + ' in ' + str(current - previous)
                #         previous = current
                #     d = {k: val for k, val in row.iteritems() if (k in fields.keys() and row is not None)}
                #     response = urllib2.urlopen(base_url.format(d['CERT']))
                #     response_json = json.load(response)
                #     d['asset_size'] = response_json['d']['results'][0]['totalAssets']
                #     branches.append(d)
            return branches.get()
        except Exception as e:
            print 'error is: ' + e.message
            return branches.get()


def multi_call_api(row):
    d = {k: val for k, val in row.iteritems() if (k in fields.keys() and row is not None)}
    if d['MAINOFF'] == '0':
        return None
    response = urllib2.urlopen(base_url.format(d['CERT']))
    response_json = json.load(response)
    d['asset_size'] = response_json['d']['results'][0]['totalAssets']
    return d


def output_json_to_csv(raw_api_data):
    with open("asset_size.csv", "w") as myfile:
        myfile.write('"'+'","'.join(raw_api_data[0].keys())+'"')
        myfile.write("\n")
        for row in raw_api_data:
            try:
                myfile.write('"'+'","'.join(val for key, val in row.iteritems())+'"')
                myfile.write("\n")
            except:
                pass

# def get_post_data():
#     posts = []
#     with open("OFFICES2_ALL.CSV", "r") as myfile:
#         reader = csv.DictReader(myfile)
#         for row in reader:
#             posts.append({k: val for k, val in row.iteritems() if (k in post_fields and row is not None)})
#         return posts

if __name__ == "__main__":
    branch_type = 'FDIC'
    if len(sys.argv) == 2:
        branch_type = str(sys.argv[1])
    raw_api_data = get_raw_api_data(branch_type)
    data = [row for row in raw_api_data if row is not None]
    output_json_to_csv(data)
    # print json.dumps(raw_api_data)
    # print (len(raw_api_data))
