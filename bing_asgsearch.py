# -*- coding: utf-8 -*-

"""
This script modifies the script created by Autor et al. (2019)

Note that the input file should be in csv format and should contain the
firm ID in first column ("assignee_id" or just "id") and a search key (firm name)
in a second column. The program will insert quotation marks around the key and
search the key on Bing. Only N top results are retrieved from Bing (see API params
that are hard-coded in this script).

Usage from command line:

python bing_asgsearch.py <input.csv> <startRow> <endRow> <free|s2>

Where startRow and endRow indicate what rows of input.csv the script should use.


See original implementation at:
Autor, David, David Dorn, Gordon H. Hanson, Gary Pisano, and Pian Shu, 􏰄Foreign Competition and Domestic Innovation: Evidence from U.S. Patents,􏰅 NBER Working Paper No. 22879, December 2016.
"""

import urllib
import urllib2
import json
import time
import logging
import bing_searchweb
import csv, string, re, sys
import datetime
import time
from configparser import ConfigParser
parser = ConfigParser()
parser.read('config.cfg')

debug = False # display runtime messages?
resultsLimit = 10 # number of search results to retrieve with query
batch_size = 1000 # report progress to terminal every N records

start_index = int(sys.argv[2])
end_index = int(sys.argv[3])
cfg = sys.argv[4] or 'free'
input_names = open(str(sys.argv[1]), 'rU')
file_name = 'output' + '_' + str(start_index) + '_' + str(end_index) + '.csv'
output_file = open(file_name, 'w')
reader = csv.reader(input_names)
data = [row for row in reader]
input_names.close()
writer = csv.writer(output_file)

firstRow = ['id', 'key', 'count']
for item in range(1, resultsLimit + 1):
    firstRow.append('link' + str(item))
    firstRow.append('title' + str(item))

writer.writerow(firstRow)


def millis():
    return int(round(time.time() * 1000))


print "Start time: %s" % (datetime.datetime.utcnow().strftime("%H:%M:%S.%f"))
print "Using config version '%s'" % (cfg)


row_counter = start_index
report_counter = 0
batch_counter = 1

millis_start = 1590606347000 # any time in the past
millisBetweenCalls = parser.getint(cfg, 'millisBetweenCalls')
safety_margin = millisBetweenCalls * .3 # about 30%


for row in data[start_index : end_index]:

    # small ad-hoc routine to sleep online the necessary to avoid API's too many calls error
    s = 0
    millis_now = millis()
    diff = millis_now - millis_start
    if (diff < millisBetweenCalls):
        print "%s %s" % (millisBetweenCalls, diff)
        s = (millisBetweenCalls - diff + safety_margin) / float(1000)
        print "sleeping %s millisecs" % (s)
    time.sleep(s)

    new_row = []
    write = True
    counter = 0
    record_id = ''
    firm_name = ''

    if (row[0] == 'assignee_id' or row[0] == 'id'):
        continue
    for s in row:
        if counter == 0:
            record_id = s
            counter += 1
        elif counter == 1:
            firm_name = s
            counter += 1
        else:
            break

    search_str = '%s: %s' % (record_id, firm_name)

    if debug:
        print "Searching #%s %s (%s)..." % (row_counter + 1, firm_name, record_id)
    # else:
    #     sys.stdout.write('.')
    #     sys.stdout.flush()

    query = "\"" + firm_name + "\""

    millis_start = millis()
    links = bing_searchweb.get_all_links(query, resultsLimit, cfg)
    results_count = len(links) / 2 # 2 props: link, title
    report_counter += 1

    if debug:
        print "Got %s results" % (results_count)
    else:
        if (report_counter == batch_size):
            print "%s rows processed" % (batch_size * batch_counter)
            report_counter = 0
            batch_counter += 1

    row_counter += 1

    new_row = [record_id]
    new_row.append(firm_name)
    new_row.append(results_count)

    for link in links:
        new_row.append(link)
    writer.writerow(new_row)

output_file.close()

# Done.
if (report_counter > 0):
    print "%s rows processed" % ((batch_size * (batch_counter - 1)) + report_counter)
print "End time: %s" % (datetime.datetime.utcnow().strftime("%H:%M:%S.%f"))
print "\nDone."
print "Results are in %s" % (file_name)
