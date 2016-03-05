#!/usr/bin/python

import sys
import urllib2
import json
import solrqueries as solr

if len(sys.argv) < 2:
    print "You must specify a query"
    raise SystemExit

query=sys.argv[1]

response = solr.autosuggest(query, ["designer", "sub_type_tree"])

designer_groups = response["grouped"]["designer"]["groups"]

pad = 0
for group in designer_groups:
    main_str = query + " in " + group["groupValue"] + " (" + str(group["doclist"]["numFound"]) + ")"
    if len(main_str) + 1 > pad:
        pad = len(main_str) + 1

print ""
print "Suggested searches by designer:"
for group in designer_groups:
    main_str = query + " in " + group["groupValue"] + " (" + str(group["doclist"]["numFound"]) + ")"
    print (
        "    " + main_str.ljust(pad) +
        ": " + "./search-designer.py \"" + query + "\" " + str(group["doclist"]["docs"][0]["designer_id"])
    )

sub_type_tree_groups = response["grouped"]["sub_type_tree"]["groups"]

pad = 0
for group in sub_type_tree_groups:
    main_str = query + " in " + group["groupValue"] + " (" + str(group["doclist"]["numFound"]) + ")"
    if len(main_str) + 1 > pad:
        pad = len(main_str) + 1

print ""
print "Suggested searches by sub_type:"
for group in sub_type_tree_groups:
    main_str = query + " in " + group["groupValue"] + " (" + str(group["doclist"]["numFound"]) + ")"
    print (
        "    " + main_str.ljust(pad) +
        ": " + "./search-subtype.py \"" + query + "\" " + "\"" + str(group["doclist"]["docs"][0]["sub_type_tree"]) + "\""
	)
print ""
