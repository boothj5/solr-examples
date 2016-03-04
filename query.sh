#curl http://localhost:8983/solr/myshop/select?q=*:*&wt=json&indent=true

QUERY=q=$@

curl -G -v "http://localhost:8983/solr/myshop/select" \
    --data-urlencode "$QUERY" \
    --data-urlencode "wt=json" \
    --data-urlencode "indent=true"
