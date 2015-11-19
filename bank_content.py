#!/usr/bin/env python
import csv


def parseContent():
    data = []
    with open("ContentPosted2015.CSV", "rU") as myfile:
        reader = csv.DictReader(myfile)
        for row in reader:
            d = {k: val for k, val in row.iteritems() if row is not None}
            parser = d['Account Charter Number']
            letter = parser.find('-')
            d['certNumber'] = parser[0:letter]
            d['type'] = parser[letter+1:len(parser)]
            # print d
            data.append(d)
    return data


def printData(data):
    with open("ContentPostedParsed.csv", "w") as myfile:
        myfile.write(','.join(data[0].keys()))
        myfile.write("\n")
        for row in data:
            myfile.write(','.join(val for key, val in row.iteritems()))
            myfile.write("\n")
if __name__ == "__main__":
    data = parseContent()
    printData(data)
