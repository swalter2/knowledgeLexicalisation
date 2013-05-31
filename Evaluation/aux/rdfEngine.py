import json
import logging

import rdflib as rdf
from   rdflib import Namespace, RDFS, RDF, BNode
import pystache

from os.path import exists
from sys     import exit

from utils import isURI


OWL   = Namespace("http://www.w3.org/2002/07/owl#")
lemon = Namespace("http://www.monnet-project.eu/lemon#")


"""
 Loading an OWL/RDF graph
"""

def loadGraph(f):
     graph = rdf.Graph()
     if f.endswith('.owl') or f.endswith('.rdf'):
           graph.parse(f)
     elif f.endswith('.ttl') or f[:-3] in ('.n3','.nt'):
           graph.parse(f,format='n3') 
     else: 
           logging.error('Unknown format of: '+f)
           exit(0)
     logging.info('Graph in '+ f +' contains ' + str(len(graph)) + ' statements.')
     return graph


""" 
 Reading an ontology 
 based on ONTO_INSPECTOR (c) 2010 __Michele Pasin__ <michelepasin.org>
"""

def getClasses(graph):

    classes = []

    for s,p,o in graph.triples((None, RDF.type, OWL.Class)):
        classes.append(s)
    for s,p,o in graph.triples((None, RDF.type, RDFS.Class)):
        classes.append(s)

    # classes not declared explicitly
    # ...but only in subclass definitions
    for s,p,o in graph.triples((None, RDFS.subClassOf, None)):
        if s not in classes: classes.append(s)
        if o not in classes: classes.append(o)
    # ...but only in rdfs:domain and rdfs:range definitions
    for s,p,o in graph.triples((None, RDFS.domain, None)):
        if o not in classes: classes.append(o)
    for s,p,o in graph.triples((None, RDFS.range, None)):
        if o not in classes: classes.append(o)

    classes = [ x for x in classes if not __isBlankNode(x) ]
    
    return list(set(classes))


def getProperties(graph):

    properties = []
		
    for s,p,o in graph.triples((None, RDF.type, RDF.Property)):
        properties.append(s)
    for s,p,o in graph.triples((None, RDF.type, OWL.ObjectProperty)):
        properties.append(s)
    for s,p,o in graph.triples((None, RDF.type, OWL.DatatypeProperty)):
        properties.append(s)

    return list(set(properties))

def getPropertyDomain(graph,propertyURI):

    domains = []
    for _,_,o in graph.triples((propertyURI, RDFS.domain, None)):
        if o not in domains: domains.append(o)
    if not domains: domains.append(OWL.thing)
    return domains

def getPropertyRange(graph,propertyURI):

    ranges = []
    for _,_,o in graph.triples((propertyURI, RDFS.range, None)):
        if o not in ranges: ranges.append(o)
    if not ranges: ranges.append(OWL.thing)
    return ranges


def getInstances(graph,classURI):

    instances = []
    for s,p,o in graph.triples((None, RDF.type, classURI)):
        instances.append(s)
    return list(set(instances))


def __isBlankNode(node):
    if type(node) == BNode: return True
    return False


"""
  Support for OWL constructs
"""

# owl:propertyChain

def collectPropertyChains(graph):

    chains = dict() # { blankNodeIdentifier: [property] }

    for _,_,o1 in graph.triples((None, lemon.sense, None)):
        for _,_,o2 in graph.triples((o1, lemon.reference, None)):
            if not isURI(o2): 
               nodeList = []
               for _,_,o3 in graph.triples((o2, OWL.propertyChain, None)):
                   __readList(graph,o3,nodeList)
               """ domain and range would need to be extracted from tbox-graph
               chain['domain']    = getPropertyDomain(graph,nodeList[0])[0]
               chain['range']     = getPropertyRange(graph,nodeList[-1])[0]
               """
               chains[str(o2)] = nodeList

    return chains

def __readList(graph,node,nodeList):

     for _,_,first in graph.triples((node, RDF.first, None)):
         nodeList.append(first)
         for _,_,rest in graph.triples((node, RDF.rest, None)):
             if not rest == RDF.nil:
                if __isBlankNode(rest): 
                   __readList(graph,rest,nodeList)
                else:
                   nodeList.append(rest)

"""
  Querying
"""

def check(x):
     return exists('sparql/'+x+'.sparql')

def q(x,y):
    f = 'sparql/'+x+'.sparql'
    if (not exists(f)): 
       logging.error('File not found: '+f)
       exit(0)
    return pystache.render(open(f,'r').read(),{'uri':y})

def getResults(graph,name,uri):
    try:
        return graph.query(q(name,uri)).result
    except: 
        logging.error('Querying for '+name+' failed.')
        return []

def getResultsFrom(graph,f):
    if (not exists(f)): 
       logging.error('File not found: '+f)
       exit(0)
    try: 
        return graph.query(open(f,'r').read()).result
    except: 
        logging.error('Querying '+f+' failed.')
        return []

def getBindings(graph,name,uri):
    try:
        j = graph.query(q(name,uri)).serialize(format='json')
        return json.loads(j)['results']['bindings']
    except: 
        logging.error('Querying for '+name+' failed.')
        return []
    
def getBindingsAsDict(graph,name,uri,postprocessing):
    # build [ { key:value } ]
    bindings = []
    for b in getBindings(graph,name,uri):
        d = dict()
        for key in b.keys():
            d[key] = postprocessing(b[key]['value'])
        bindings.append(d)
    # aggregate blank node
    new_bindings = []
    for b in bindings:
        if not new_bindings: new_bindings.append(b)
        else:
           if 'blank' in b.keys():
              for nb in new_bindings:
                  if 'blank' in nb.keys() and nb['blank'] == b['blank']:
                      listupdate(nb,b)
           else: new_bindings.append(b)
    # remove blank nodes and singletons
    for nb in new_bindings: 
        if nb.has_key('blank'): del nb['blank']
        for (k,v) in nb.items():
            if type(v) == set and len(v) == 1: nb[k] = next(iter(v))
    # return result
    return new_bindings

def updateDict(graph,dic,name,uri,postprocessing):
     for b in getBindingsAsDict(graph,name,uri,postprocessing): dic.update(b)
