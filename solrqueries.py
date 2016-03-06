import urllib
import urllib2
import json

host = "localhost"
port = 8983
core = "myshop"
base_url = "http://" + host + ":" + str(port) + "/solr/" + core + "/select?wt=json&indent=true&defType=edismax"

def autosuggest(query, query_fields=None, group_fields=None):
	params = ""

	if query_fields:
		params += "&qf="
		field_strs = []
		for k,v in query_fields.items():
			field_strs.append(k + "^" + str(v))
		params += "+".join(field_strs)

	if group_fields:
		params += (
		    "&group=true"
		    "&group.limit=100"
		)

	if group_fields:
		for group_field in group_fields:
			params += "&group.field=" + group_field

	query_param="&q=" + query.replace(" ", "+")

	path = base_url + query_param + params
	print path

	res = urllib2.urlopen(path).read()
	response = json.loads(res)

	return response

def search(query, field=None, field_value=None):
	params = (
	    "&qf=name_search+designer_search+category_search+product_type_search+sub_type_search"
	)

	query_param = "&q=(" + query.replace(" ", "+") + ")"
	if field and field_value:
		query_param += "+AND+" + field + ":" + "\"" + field_value.replace(" ", "+") + "\""

	path = base_url + query_param + params
	res = urllib2.urlopen(path).read()
	response = json.loads(res)

	return response

def product_by_id(product_id):
    query_params = { "q" : "id:" + product_id }
    query_params_enc = urllib.urlencode(query_params)

    path = base_url + "&" + query_params_enc
    res = urllib2.urlopen(path).read()
    response = json.loads(res)
    product = response["response"]["docs"][0]

    return product
