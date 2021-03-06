#!/usr/bin/python
import web
import json
from collections import OrderedDict

import solrqueries as solr

urls = (
    "/", "home",
    "/autosuggest", "autosuggest",
    "/autosuggest/product", "autosuggest_product",
    "/autosuggest/designer", "autosuggest_designer",
    "/autosuggest/category", "autosuggest_category",
    "/search/designer", "search_designer",
    "/search/subtype", "search_subtype",
    '/product/(.*)', 'get_product'
)

def parse_query_params():
    params = {}
    for param in web.ctx.query[1:].split("&"):
        tokens = param.split("=")
        params[tokens[0]] = tokens[1]

    return params

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

def solr_designer_to_designer(solr_designer):
    return OrderedDict([
        ("name",    solr_designer["groupValue"]),
        ("id",      solr_designer["doclist"]["docs"][0]["designer_id"]),
        ("count",   solr_designer["doclist"]["numFound"])
    ])

def solr_category_to_category(solr_category):
    return OrderedDict([
        ("name",    solr_category["groupValue"]),
        ("count",   solr_category["doclist"]["numFound"])
    ])

def solr_group_to_group(solr_group, identifier):
    return OrderedDict([
        ("name",        solr_group["groupValue"]),
        ("identifier",  solr_group["doclist"]["docs"][0][identifier]),
        ("count",       solr_group["doclist"]["numFound"])
    ])

def solr_search_result_to_result(solr_results):
    results = []
    for solr_product in solr_results:
        results.append(solr_product_to_product(solr_product))

    return results

def solr_group_result_to_group_result(solr_groups, identifier):
    results = []
    for solr_group in solr_groups:
        results.append(solr_group_to_group(solr_group, identifier))

    return results

def solr_product_results_to_product_results(solr_product_results):
    count = solr_product_results["numFound"]
    results = []
    for solr_product in solr_product_results["docs"]:
        results.append(solr_product_to_product(solr_product))

    return OrderedDict([
        ("count", count),
        ("products", results)
    ])

def solr_designer_results_to_designer_results(solr_designer_results):
    results = []
    for solr_designer in solr_designer_results:
        results.append(solr_designer_to_designer(solr_designer))

    return results

def solr_category_results_to_category_results(solr_category_results):
    results = []
    for solr_category in solr_category_results:
        results.append(solr_category_to_category(solr_category))

    return results

class home:
    def GET(self):
        with open('index.html', 'r') as myfile:
            res = myfile.read().replace('\n', '')
            return res

class get_product:
    def GET(self, product_id):
        solr_product = solr.product_by_id(product_id)        
        product = solr_product_to_product(solr_product)
        body = json.dumps(product, indent=4)

        return body + "\n"

class autosuggest:
    def GET(self):
        params = parse_query_params()

        query_fields = {
            "designer_search": 10,
            "name_search": 5,
            "sub_type_search": 3,
            "product_type_search": 2,
            "category_search": 1
        }

        solr_group_result = solr.autosuggest(
            query = params["query"], 
            query_fields = query_fields, 
            group_fields = ["designer", "sub_type_tree"],
            group_limit = None,
            fields = None
        )

        solr_designer_groups = solr_group_result["grouped"]["designer"]["groups"]
        solr_subtype_groups = solr_group_result["grouped"]["sub_type_tree"]["groups"]

        designer_group_result = solr_group_result_to_group_result(solr_designer_groups, "designer_id")
        subtype_group_result = solr_group_result_to_group_result(solr_subtype_groups, "sub_type_tree")

        group_result = OrderedDict([
            ("designer", designer_group_result),
            ("subtype", subtype_group_result)
        ])

        body = json.dumps(group_result, indent=4)

        return str(body) + "\n"

class autosuggest_product:
    def GET(self):
        params = parse_query_params()

        query_fields = {
            "name_search": 1
        }

        solr_product_results = solr.autosuggest(
            query = params["query"], 
            query_fields = query_fields, 
            group_fields = None,
            group_limit = None,
            fields = None
        )

        product_results = solr_product_results_to_product_results(solr_product_results["response"])
        body = json.dumps(product_results, indent=4)

        return str(body) + "\n"

class autosuggest_designer:
    def GET(self):
        params = parse_query_params()

        query_fields = {
            "designer_search": 10
        }

        solr_designer_results = solr.autosuggest(
            query = params["query"], 
            query_fields = query_fields, 
            group_fields = ["designer"],
            group_limit = 1,
            fields = ["designer_id"]
        )

        designer_results = solr_designer_results_to_designer_results(solr_designer_results["grouped"]["designer"]["groups"])
        body = json.dumps(designer_results, indent=4)

        return str(body) + "\n"

class autosuggest_category:
    def GET(self):
        params = parse_query_params()

        query_fields = {
            "sub_type_tree_search": 10
        }

        solr_category_results = solr.autosuggest(
            query = params["query"], 
            query_fields = query_fields, 
            group_fields = ["sub_type_tree"],
            group_limit = 1,
            fields = ["category", "product_type", "sub_type"]
        )

        category_results = solr_category_results_to_category_results(solr_category_results["grouped"]["sub_type_tree"]["groups"])
        body = json.dumps(category_results, indent=4)

        return str(body) + "\n"

class search_designer:
    def GET(self):
        params = parse_query_params()
        solr_result = solr.search(params["query"], "designer_id", params["designer_id"])
        result = solr_search_result_to_result(solr_result["response"]["docs"])
        body = json.dumps(result, indent=4)

        return str(body) + "\n"

class search_subtype:
    def GET(self):
        params = parse_query_params()
        solr_result = solr.search(params["query"], "sub_type_tree", params["sub_type_tree"])
        result = solr_search_result_to_result(solr_result["response"]["docs"])
        body = json.dumps(result, indent=4)

        return str(body) + "\n"

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
