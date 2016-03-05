#!/usr/bin/python

import sys
import urllib2
import json
import solrqueries as solr

if len(sys.argv) < 3:
    print "You must specify a query and sub type"
    raise SystemExit

query=sys.argv[1]
sub_type_tree = sys.argv[2]
response = solr.search(query, "sub_type_tree", sub_type_tree)
numFound = response["response"]["numFound"]

if numFound == 0:
	print ""
	print "No results found."
	print ""
	raise SystemExit

sub_type_tree = response["response"]["docs"][0]["sub_type_tree"]

pad = 0
for document in response["response"]["docs"]:
	main_str = document["name"] + " by " + document["designer"]
	if len(main_str) + 1 > pad:
		pad = len(main_str) + 1

print ""
print str(numFound) + " results for \"" + query + "\" in " + sub_type_tree + ":"
for document in response["response"]["docs"]:
	main_str = document["name"] + " by " + document["designer"]
	print (
		"    " + main_str.ljust(pad) + 
		": " + "./get-product.py " + str(document["id"])
	)
print ""


