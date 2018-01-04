## DEMO
[Demo](https://madsholten.github.io/PySPARQL2D3/)

## USE
```sh
$ python PyS2D3.py -t fileA.ttl fileB.ttl -q query.rq
```

Arguments

Flag            | Required | Description
--------------- | -------- | -----------
-t --triple     | X        | Path to one or more triple files in ttl-format
-q --query      | X        | SPARQL query string or path to a file containing the SPARQL query
-p --prefixes   |          | Path to JSON-file with prefixes. Defaults to ./data/prefixes.json
-o --output     |          | Path to output file. Defaults to ./data.json

## TEST
```sh
$ python PyS2D3.py -t ./test/fileA.ttl ./test/fileB.ttl -q ./test/query.rq -o ./test/data.json
```

## D3 JSON file use
Based on the work by Rathachai, I have made some minor visual improvements and changed it so that it renders content from a JSON-file.
Simply run a simple http server from the root folder. It visualises the file 'data.json' located within the folder as default.

Run server with python 2.7
```sh
$ python -m SimpleHTTPServer 8000
```

Run server with python 3.6
```sh
$ python -m http.server 8000
```

Then visit localhost:8000 in the browser to see the result
