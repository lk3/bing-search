# -*- coding: utf-8 -*-

"""
This script modifies the script created by Autor et al. (2019)
Update the config.py file before running the script.

See original implementation at:
Autor, David, David Dorn, Gordon H. Hanson, Gary Pisano, and Pian Shu, 􏰄Foreign Competition and Domestic Innovation: Evidence from U.S. Patents,􏰅 NBER Working Paper No. 22879, December 2016.
"""

import urllib
import urllib2
import json
from configparser import ConfigParser
parser = ConfigParser()


def get_all_links(query, limit, cfg):

    parser.read('config.cfg')

    if limit is None:
        limit = 1

    key = parser.get(cfg, 'cognitiveServicesKey')
    endPoint = parser.get(cfg, 'endPoint')
    customConfig = parser.get(cfg, 'customConfig')
    query = urllib.quote(query)
    url = endPoint+'/search?customconfig='+customConfig+'&q=%27'+query+'%27&count='+str(limit)
    try:
        request = urllib2.Request(url)
        request.add_header('Ocp-Apim-Subscription-Key', key)
        request_opener = urllib2.build_opener()
        response = request_opener.open(request)
        response_data = response.read()
        json_result = json.loads(response_data)
        result_list = []
        if json_result.has_key('webPages'):
            if json_result['webPages'].has_key('value'):
                result_list = json_result['webPages']['value']
        links = []
        for result in result_list:
            # link field
            if u'url' in result.viewkeys():
                 links.append(result[u'url'].encode('utf-8'))
            # title field
            if u'name' in result.viewkeys():
                links.append(result[u'name'].encode('utf-8'))
            # description field
            # if u'snippet' in result.viewkeys():
            #    links.append(result[u'snippet'].encode('utf-8'))
    except urllib2.HTTPError as e:
        links=["ERROR", e]

    return links