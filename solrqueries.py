import urllib2
import json

def autosuggest(query, group_fields):
	host = "localhost"
	port = 8983
	core = "myshop"
	base_url = "http://" + host + ":" + str(port) + "/solr/" + core + "/select?wt=json&indent=true&defType=edismax"
	params = (
	    "&qf=name_search+designer_search+category_search+product_type_search+sub_type_search"
	    "&group=true"
	    "&group.limit=100"
	)
	for group_field in group_fields:
		params += "&group.field=" + group_field

	query_param="&q=" + query.replace(" ", "+")

	path = base_url + query_param + params
	res = urllib2.urlopen(path).read()
	response = json.loads(res)

	return response

def search(query, field, field_value):
	host = "localhost"
	port = 8983
	core = "myshop"
	base_url = "http://" + host + ":" + str(port) + "/solr/" + core + "/select?wt=json&indent=true&defType=edismax"
	params = (
	    "&qf=name_search+designer_search+category_search+product_type_search+sub_type_search"
	)

	query_param="&q=(" + query.replace(" ", "+") + ")" + "+AND+" + field + ":" + "\"" + field_value.replace(" ", "+") + "\""

	path = base_url + query_param + params
	res = urllib2.urlopen(path).read()
	response = json.loads(res)

	return response
