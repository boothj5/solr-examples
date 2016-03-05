def print_suggest_results(query, group_display, groups, search_script, search_field, quote_search_field):
    pad = 0
    for group in groups:
        main_str = query + " in " + group["groupValue"] + " (" + str(group["doclist"]["numFound"]) + ")"
        if len(main_str) + 1 > pad:
            pad = len(main_str) + 1

    print ""
    print "Suggested searches by " + group_display + ":"
    for group in groups:
        main_str = query + " in " + group["groupValue"] + " (" + str(group["doclist"]["numFound"]) + ")"
        if quote_search_field:
            search_str = search_script + " \"" + query + "\" " + "\"" + str(group["doclist"]["docs"][0][search_field]) + "\""
        else:
            search_str = search_script + " \"" + query + "\" " + str(group["doclist"]["docs"][0][search_field])
        print (
            "    " + main_str.ljust(pad) +
            ": " + search_str
        )