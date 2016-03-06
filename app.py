#!/usr/bin/python
import web
import json
from collections import OrderedDict

import solrqueries as solr

urls = (
    "/", "home",
    "/autosuggest/search/designer/(.*)", "autosuggest_search_designer",
    "/autosuggest/search/subtype/(.*)", "autosuggest_search_subtype",
    "/search/designer", "search_designer",
    "/search/subtype", "search_subtype",
    '/product/(.*)', 'get_product'
)

def solr_product_to_product(solr_product):
    return OrderedDict([
        ("id",                  solr_product["id"]),
        ("name",                solr_product["name"]),
        ("designer",            solr_product["designer"]),
        ("designer_id",         solr_product["designer_id"]),
        ("category",            solr_product["category"]),
        ("product_type",        solr_product["product_type"]),
        ("product_type_tree",   solr_product["product_type_tree"]),
        ("sub_type",            solr_product["sub_type"]),
        ("sub_type_tree",       solr_product["sub_type_tree"])
    ])

def solr_search_result_to_result(solr_results):
    results = []
    for solr_product in solr_results:
        results.append(solr_product_to_product(solr_product))

    return results

def solr_group_result_to_group_result(solr_group_result, group, identifier):
    groups = solr_group_result["grouped"][group]["groups"]
    results = []

    for group in groups:
        result = OrderedDict([
            ("name", group["groupValue"]),
            ("identifier", group["doclist"]["docs"][0][identifier]),
            ("count", group["doclist"]["numFound"])
        ])
        results.append(result)
    return results

class home:
    def GET(self):
        return "Solr Examples"

class get_product:
    def GET(self, product_id):
        solr_product = solr.product_by_id(product_id)        
        product = solr_product_to_product(solr_product)
        body = json.dumps(product, indent=4)

        return body + "\n"

class autosuggest_search_designer:
    def GET(self, query):
        solr_group_result = solr.autosuggest(query, ["designer"])
        group_result = solr_group_result_to_group_result(solr_group_result, "designer", "designer_id")
        body = json.dumps(group_result, indent=4)

        return str(body) + "\n"

class autosuggest_search_subtype:
    def GET(self, query):
        solr_group_result = solr.autosuggest(query, ["sub_type_tree"])
        group_result = solr_group_result_to_group_result(solr_group_result, "sub_type_tree", "sub_type_tree")
        body = json.dumps(group_result, indent=4)

        return str(body) + "\n"

class search_designer:
    def GET(self):
        params = web.ctx.query[1:].split("&")
        params_dict = {}
        for param in params:
            tokens = param.split("=")
            params_dict[tokens[0]] = tokens[1]
        solr_result = solr.search(params_dict["query"], "designer_id", params_dict["designer_id"])
        result = solr_search_result_to_result(solr_result["response"]["docs"])
        body = json.dumps(result, indent=4)

        return str(body) + "\n"

class search_subtype:
    def GET(self):
        params = web.ctx.query[1:].split("&")
        params_dict = {}
        for param in params:
            tokens = param.split("=")
            params_dict[tokens[0]] = tokens[1]
        solr_result = solr.search(params_dict["query"], "sub_type_tree", params_dict["sub_type_tree"])
        result = solr_search_result_to_result(solr_result["response"]["docs"])
        body = json.dumps(result, indent=4)

        return str(body) + "\n"

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
