# -*- coding: utf-8 -*-

"""
This script modifies the script created by Autor et al. (2019)

Note that the input file should be in csv format and should contain the
firm ID in first column ("assignee_id" or just "id") and a search key (firm name)
in a second column. The program will insert quotation marks around the key and
search the key on Bing. Only N top results are retrieved from Bing (see API params
that are hard-coded in this script).

Usage from command line:

python bing_asgsearch.py <input.csv> <startRow> <endRow>

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


# Search API params
debug = False # display runtime messages?
resultsLimit = 5 # number of search results to retrieve with query
# sleepSecs = 1 # time to wait between queries
report_every_n_records = 1000 # report progress to terminal every N records

start_index = int(sys.argv[2])
end_index = int(sys.argv[3])
input_names = open(str(sys.argv[1]), 'rU')
file_name = 'output' + '_' + str(start_index) + '_' + str(end_index) + '.csv'
output_file = open(file_name, 'w')
reader = csv.reader(input_names)
data = [row for row in reader]
input_names.close()
writer = csv.writer(output_file)
writer.writerow(['id', 'key', 'count', 'link1', 'title1', 'description1', 'link2', 'title2', 'description2', 'link3', 'title3', 'description3', 'link4', 'title4', 'description4', 'link5', 'title5', 'description5'])

# @sleep_and_retry
# @limits(calls=1, period=2)
# def get_all_links(q, c):
#     print "Calling"
#     return bing_searchweb.get_all_links(q, c)


def millis():
    return int(round(time.time() * 1000))

print datetime.datetime.utcnow().strftime("%H:%M:%S.%f")

row_counter = start_index
report_counter = 0

millis_start = 1590606347000 # any time in the past
time_between_calls = 10 # 1000 # millisecs between calls
safety_margin = 3 # 300 # about 30%


for row in data[start_index : end_index]:

    s = 0
    millis_now = millis()
    diff = millis_now - millis_start
    if (diff < time_between_calls):
        print "%s %s" % (time_between_calls, diff)
        s = (time_between_calls - diff + safety_margin) / float(1000)
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
    links = bing_searchweb.get_all_links(query, resultsLimit)
    # links = get_all_links(query, resultsLimit)
    results_count = len(links) / 3 # 3 props: link, title, descr
    report_counter += 1

    if debug:
        print "Got %s results" % (results_count)
    else:
        if (report_counter == report_every_n_records):
            print "%s rows processed" % (report_counter)
            report_counter=0

    # time.sleep(# sleepSecs)
    row_counter+=1

    new_row = [record_id]
    new_row.append(firm_name)
    new_row.append(results_count)

    for link in links:
        new_row.append(link)
    writer.writerow(new_row)

output_file.close()

print datetime.datetime.utcnow().strftime("%H:%M:%S.%f")
print "\nDone."
print "Results are in %s" % (file_name)
