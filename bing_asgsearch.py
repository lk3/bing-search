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
limit = 5 # number of search results to retrieve with query
sleepSecs = 1 # time to wait between queries


start_index = int(sys.argv[2])
end_index = int(sys.argv[3])
input_names = open(str(sys.argv[1]), 'rU')
file_name = 'output' + '_' + str(start_index) + '_' + str(end_index) + '.csv'
output_file = open(file_name, 'w')
reader = csv.reader(input_names)
data = [row for row in reader]
input_names.close()
writer = csv.writer(output_file)
writer.writerow(['id', 'key', 'link1', 'title1', 'description1', 'link2', 'title2', 'description2', 'link3', 'title3', 'description3', 'link4', 'title4', 'description4', 'link5', 'title5', 'description5'])

row_counter = start_index
for row in data[start_index : end_index]:
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

    start = 0
    ts = time.time()
    track_time = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    if debug:
        print "Searching #%s %s (%s)..." % (row_counter + 1, firm_name, record_id)
    else:
        sys.stdout.write('.')
        sys.stdout.flush()

    query = "\"" + firm_name + "\""

    links = bing_searchweb.get_all_links(query, limit)
    results_count = len(links) / 3 # 3 props: link, title, descr
    if debug:
        print "Got %s results" % (results_count)

    time.sleep(sleepSecs)
    row_counter += 1

    new_row = [record_id]
    new_row.append(firm_name)
    new_row.append(results_count)

    for link in links:
        new_row.append(link)
    writer.writerow(new_row)

output_file.close()

print "\nDone."
print "Results are in %s" % (file_name)

