#!/usr/bin/python

import sys
import urllib
import urllib2
import json
import solrqueries as solr

if len(sys.argv) < 2:
    print "You must specify a product ID"
    raise SystemExit

product_id = sys.argv[1]

product = solr.product_by_id(product_id)
print ""
print "Product Info:"
print "    Product      : " + product["name"]
print "    By           : " + product["designer"]
print "    Category     : " + product["category"]
print "    Product Type : " + product["product_type"]
print "    Sub Type     : " + product["sub_type"]
print ""

