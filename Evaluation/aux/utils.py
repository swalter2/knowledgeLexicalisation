import re
import sys


# string utilities

def capitalize1(string):
    if string.startswith('xsd'):  return 'xsd'+capitalize1(string[3:])
    if string.startswith('owl'):  return 'owl'+capitalize1(string[3:])
    if string.startswith('rdfs'): return 'rdfs'+capitalize1(string[3:])
    if string.startswith('rdf'):  return 'rdf'+capitalize1(string[3:])
    return string[:1].upper() + string[1:]

def snakecase(string):
    return re.sub('\B([A-Z])','_\g<1>',string).lower()

def frag_uri(string):
    if string.startswith('http://www.w3.org/2001/XMLSchema#'):
       return 'xsd'+string.split('#')[1]
    if string.startswith('http://www.w3.org/2002/07/owl#'):
       return 'owl'+string.split('#')[1]
    if string.startswith('http://www.w3.org/1999/02/22-rdf-syntax-ns#'):
       return 'rdf'+string.split('#')[1]
    if string.startswith('http://www.w3.org/2000/01/rdf-schema#'):
       return 'rdfs'+string.split('#')[1]
    return re.match('.*/([^/]+\#)?([^/]+)$',string).group(2)

def frag_file(string):
    if '/' in string: string = string[string.rindex('/')+1:]
    return string[:string.rindex('.')].replace('.','_')

def toGF(string):
    if not '/' in string: return string
    else: return frag_uri(string)


# print 

def print_signature(signature):
       sig  = '\n----------------------------\n'
       sig += '\nDomain: ' + signature['domain'] + '\n'
       sig += '\nClasses:\n'
       for c in signature['classes']:    sig += str(c) + '\n'
       sig += '\nProperties:\n '
       for f in signature['properties']: sig += str(f) + '\n'
       sig += '\nEntities:\n '
       for f in signature['entities']:   sig += str(f) + '\n'
       sig += '----------------------------\n'
       return sig

def print_records(records):
       rec = '\n----------------------------\n'
       for r in records: rec += '\n' + str(r) +'\n'
       rec += '----------------------------\n'
       return rec

# list and dict utilities

def intersect(a,b):
     return list(set(a) & set(b))

def listupdate(d1,d2):
    for k in intersect(d1.keys(),d2.keys()):
        if type(d1[k]) == set: d1[k].add(d2[k])
        else: d1[k] = set( [d1[k],d2[k]] )

# tests

def isClass(s,signature):
    if s in signature['classes']: return True
    return False

def isRelation(s,signature):
    for p in signature['properties']:
        if p['name'] == s : return True
    return False

def isURI(string):
    return '://' in string
