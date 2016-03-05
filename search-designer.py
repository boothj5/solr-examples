#!/usr/bin/python

import sys
import urllib2
import json
import solrqueries as solr

if len(sys.argv) < 3:
    print "You must specify a query and designer ID"
    raise SystemExit

query=sys.argv[1]
designer_id = sys.argv[2]

response = solr.search(query, "designer_id", designer_id)
numFound = response["response"]["numFound"]

if numFound == 0:
	print ""
	print "No results found."
	print ""
	raise SystemExit

designer_name = response["response"]["docs"][0]["designer"]

pad = 0
for document in response["response"]["docs"]:
	main_str = document["name"] + " by " + document["designer"] + " (" + document["sub_type"] + " " + document["product_type"] + ")"
	if len(main_str) + 1 > pad:
		pad = len(main_str) + 1

print ""
print str(numFound) + " results for \"" + query + "\" in " + designer_name + ":"
for document in response["response"]["docs"]:
	main_str = document["name"] + " by " + document["designer"] + " (" + document["sub_type"] + " " + document["product_type"] + ")"
	print (
		"    " + main_str.ljust(pad) + 
		": " + "./get-product.py " + str(document["id"])
	)
print ""


