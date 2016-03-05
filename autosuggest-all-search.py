#!/usr/bin/python

import sys
import urllib2
import json
import solrqueries as solr
import common

if len(sys.argv) < 2:
    print "You must specify a query"
    raise SystemExit

query=sys.argv[1]
response = solr.autosuggest(query, ["designer", "sub_type_tree"])

common.print_suggest_results(
    query,
    "designer",
    response["grouped"]["designer"]["groups"],
    "./search-designer.py",
    "designer_id",
    False
)

common.print_suggest_results(
    query,
    "sub_type",
    response["grouped"]["sub_type_tree"]["groups"],
    "./search-subtype.py",
    "sub_type_tree",
    True
)