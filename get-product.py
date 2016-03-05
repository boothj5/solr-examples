#!/usr/bin/python

import sys
import urllib
import urllib2
import json

host = "localhost"
port = 8983
core = "myshop"
base_url = "http://" + host + ":" + str(port) + "/solr/" + core + "/select?wt=json&indent=true"

if len(sys.argv) < 2:
    print "You must specify a product ID"
    raise SystemExit

product_id = sys.argv[1]
query_params = { "q" : "id:" + product_id }
query_params_enc = urllib.urlencode(query_params)

path = base_url + "&" + query_params_enc
res = urllib2.urlopen(path).read()

response = json.loads(res)

product = response["response"]["docs"][0]
print ""
print "Product Info:"
print "    Product      : " + product["name"]
print "    By           : " + product["designer"]
print "    Category     : " + product["category"]
print "    Product Type : " + product["product_type"]
print "    Sub Type     : " + product["sub_type"]
print ""

