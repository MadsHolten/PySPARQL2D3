#!/usr/bin/env python
# # -*- coding: utf-8 -*-

__author__      = "Mads Holten Rasmussen"
__copyright__   = "Copyright 2017, DTU|Niras"
__license__     = "GPL"
__version__     = "0.0.1"
__email__       = "mhoras@byg.dtu.dk"
__status__      = "Development"

import rdflib
import argparse
import json

class PySPARQL2D3(object):

    def __init__(self):
        self.graph = rdflib.Graph()  # holds graph
        self.prefixesPath = './data/prefixes.json'

    def establishGraph(self,data,**kwargs):
        # From string or file(s)?
        string = kwargs.pop('string', False)

        if not string:
            # if data is a string, append it to a list
            if type(data) is str:
                data = [data]
            # insert all data items to the graph and return the graph
            for item in data:
                self.graph.parse(item, format="turtle")
        else:
            self.graph.parse(data=data, format="turtle")

        return self.graph

    def queryGraph(self,query):

        if '{' in query:
            queryString = query
        else:
            # If query is in a file, read it into a string
            with open(query, 'r') as f:
                queryString = f.read()
        
        triples = self.graph.query(queryString)
        
        # If no triples in graph, return error
        if len(triples) == 0:
            return "ERR: The query returned no result"
        else:
            return triples

    def generateD3Triples(self, graph, **kwargs):
        # Get optional arguments
        prefixesPath = kwargs.pop('prefixesPath', self.prefixesPath)
        filePath = kwargs.pop('filePath', None)
        
        # Parse triples to D3 format
        triples = self._parse2D3(graph,prefixesPath)

        # Write to file
        with open(filePath, 'w') as outfile:
            json.dump(triples, outfile)
        outfile.close
        
        return triples
    
    def _parse2D3(self,triples,prefixesPath=None):
        triplesJSON = list()

        for s,p,o in triples:

            # If prefixes are defined, append these
            if prefixesPath:
                prefixes = json.load(open(prefixesPath))

                for item in prefixes:
                    pfx = str(item["prefix"]+":")
                    if item["uri"] in s:
                        s = s.replace(item["uri"], pfx)
                    if item["uri"] in p:
                        p = p.replace(item["uri"], pfx)
                    if item["uri"] in o:
                        o = o.replace(item["uri"], pfx)

            # Create JSON output
            triplesJSON.append({"subject": s, "predicate": p, "object": o})

        return triplesJSON

def main():
    # Get arguments from stdin
    parser = argparse.ArgumentParser(description='Generate D3 JSON file')
    parser.add_argument('-t', '--triples', nargs='+', required=True, help='Path to one or more triple files in ttl-format')
    parser.add_argument('-q', '--query', required=False, help='SPARQL query string or path to a file containing the SPARQL query')
    parser.add_argument('-p', '--prefixes', required=False, help='Path to JSON-file with prefixes. Defaults to ./data/prefixes.json')
    parser.add_argument('-o', '--output', required=False, help='Path to output file. Defaults to ./data.json')

    # Get arguments and set defaults
    args = parser.parse_args()
    paths = args.triples
    query = args.query
    filePath = args.output if args.output else './data.json'
    prefixesPath = args.prefixes if args.prefixes else './data/prefixes.json'

    # Initialize class
    pd3 = PySPARQL2D3()

    # Load data to in memory graph
    g = pd3.establishGraph(paths)

    # Do query if one is specified
    if query:
        g = pd3.queryGraph(query)

    # Do query and write to D3-json
    d3JSON = pd3.generateD3Triples(g,filePath=filePath,prefixesPath=prefixesPath)


if __name__ == "__main__":
    main()
