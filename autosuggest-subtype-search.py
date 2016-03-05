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
    "&group=true"
    "&group.limit=100"
    "&group.field=sub_type_tree"
)

if len(sys.argv) < 2:
    print "You must specify a query"
    raise SystemExit

query=sys.argv[1]
query_param="&q=" + query.replace(" ", "+")

path = base_url + query_param + params
res = urllib2.urlopen(path).read()
# print res

response = json.loads(res)
groups = response["grouped"]["sub_type_tree"]["groups"]

pad = 0
for group in groups:
	main_str = query + " in " + group["groupValue"] + " (" + str(group["doclist"]["numFound"]) + ")"
	if len(main_str) + 1 > pad:
		pad = len(main_str) + 1

print ""
print "Suggested searches:"
for group in groups:
	main_str = query + " in " + group["groupValue"] + " (" + str(group["doclist"]["numFound"]) + ")"
	print (
		"    " + main_str.ljust(pad) + 
		": " + "./search-subtype.py " + "\"" + str(group["doclist"]["docs"][0]["sub_type_tree"]) + "\" \"" + query + "\""
	)
print ""
