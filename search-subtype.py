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

sub_type_tree = sys.argv[1]
query=sys.argv[2]
query_param="&q=(" + query.replace(" ", "+") + ")" + "+AND+sub_type_tree:" + "\"" + sub_type_tree.replace(" ", "+") + "\""

path = base_url + query_param + params
res = urllib2.urlopen(path).read()
# print res

response = json.loads(res)
numFound = response["response"]["numFound"]

pad = 0
for document in response["response"]["docs"]:
	main_str = document["name"] + " by " + document["designer"]
	if len(main_str) + 1 > pad:
		pad = len(main_str) + 1

print ""
print "Found " + str(numFound) + " results:"
for document in response["response"]["docs"]:
	main_str = document["name"] + " by " + document["designer"]
	print (
		"    " + main_str.ljust(pad) + 
		": " + "./get-product.py " + str(document["id"])
	)
print ""


