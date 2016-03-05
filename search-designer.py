#!/usr/bin/python

import sys
import urllib2
import json

host = "localhost"
port = 8983
core = "myshop"
base_url = "http://" + host + ":" + str(port) + "/solr/" + core + "/select?wt=json&indent=true&defType=edismax"
params = (
    "&qf=name_search+designer_search+category_search+product_type_search+sub_type_search"
)

if len(sys.argv) < 3:
    print "You must specify a query"
    raise SystemExit

designer_id = sys.argv[1]
query=sys.argv[2]
query_param="&q=(" + query.replace(" ", "+") + ")" + "+AND+designer_id:" + designer_id

path = base_url + query_param + params
res = urllib2.urlopen(path).read()

response = json.loads(res)
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


