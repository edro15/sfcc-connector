default_query = {
    "query": {
        "filtered_query": {
            "query": {
                "match_all_query": {}
            },
            "filter": {
                "bool_filter": {
                    "operator": "or",
                    "filters": []
                }
            }
        }
    }
}
