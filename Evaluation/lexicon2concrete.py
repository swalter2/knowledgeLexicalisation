
import logging
import re

import pystache

from aux.rdfEngine import *
from aux.utils     import *


identity = lambda x: x

# Warning and error messages
language_error   = lambda x: "Lexicon "+x+" specifies either no language or more than one (but needs to specify exactly one)."
language_warning = lambda x: "There is no resource grammar for language "+x+". Resulting GF grammar will not compile."
too_many_pos_warning = lambda x: "The lexical entry "+x+" has more than one part of speech."
pos_or_frame_not_found_warning = lambda x: "No template for part of speech or frame (or both) in entry "+x+" found."
pos_not_found_warning = lambda x: "Unknown part of speech: "+x
complex_class_sense_warning = lambda x,y: "Found a complex class sense ("+x+") but cannot determine its argument; I use arg0 instead. This happened in entries: "+y
complex_property_sense_warning = lambda x,y: "Found a complex property sense ("+x+") with more than one subject argument. This will not work! I use arg1 instead. This happened in entries: "+y



def convert_lexica(signature,lexica,gf_libs):

  lexicalizations = dict()

  ## FOR ALL LEXICON FILES
  for lexicon_file in lexica:
    logging.info('Converting: ' + lexicon_file)

    # load RDF file
    logging.info('Loading graph...')
    graph = loadGraph(lexicon_file)
    logging.info('OK.')

    for lexicon in getResultsFrom(graph,'sparql/lexicon.sparql'):
        
        # determine language
        langs = getResults(graph,'language',str(lexicon))
        if len(langs) == 1:
           l = langs[0]
           if l in gf_libs.keys(): 
               language = gf_libs[l]
           else: 
               language = l 
               logging.warning(language_warning(l))
        else: 
               logging.error(language_error) 
               system.exit()

        # build sense record from lexicon entries
        records = __construct_records__(graph,lexicon,signature,dict())
        logging.info('Records:' + print_records(records))

  ## END FOR ALL LEXICON FILES

  ## FOR ALL COLLECTED LEXICALIZATIONS
  # render concrete template as $domain_name$language.gf


def __construct_records__(graph,lexicon,signature,renaming):

    senses = __collect_senses__(graph,lexicon,signature,renaming)
    __add_lexical_information__(graph,senses,renaming)

    return senses

def __collect_senses__(graph,lexicon,signature,renaming):

    senses = []
    chains = collectPropertyChains(graph)

    for entry in getResults(graph,'entry',str(lexicon)):

        # collect simple senses
        for b in getBindings(graph,'sense',str(entry)):
            sense = dict(entries=str(entry))
            ref = b['reference']['value']
            if not isURI(ref) and chains.has_key(ref):
               sense.update( __constructReferenceChain__(chains[ref],signature) )
            else:
               for var in b.keys(): 
                   sense[var] = toGF(b[var]['value'])
            senses.append(sense)
        # collect complex senses
        sense = dict(entries=str(entry),subsenses=[])
        for b in getBindings(graph,'subsense',str(entry)):
            subsense = dict()
            for var in b.keys(): 
                if not var == 'sense': subsense[var] = toGF(b[var]['value'])
            sense['subsenses'].append(subsense)
        """ TODO: complex sense
        if  sense['subsenses']: 
            new_sense = __construct_reference_chain__(sense,signature)
            senses.append(new_sense)
        """

    # group entries with the same sense(s)
    new_senses = []
    for s in senses:
        s['entries'] = [s.pop('entries',None)]
        if not new_senses: new_senses.append(s)
        else: 
           new = True
           for e in new_senses:
               e_entry = e.pop('entries',None)
               s_entry = s.pop('entries',None)
               if e['reference'] == s['reference']: 
                  e['entries'] = e_entry + s_entry; 
                  if __sense_args_differ__(e,s):
                      r = dict()
                      r[s['subjOfProp']] = e['subjOfProp']
                      r[s['objOfProp']]  = e['objOfProp']
                      renaming[s_entry[0]] = r
                  new = False; break
               else: 
                  e['entries'] = e_entry
                  s['entries'] = s_entry
           if new: new_senses.append(s)

    for s in senses: 
        # process domain and range restrictions
        domain_res = s.has_key('propertyDomain')
        range_res  = s.has_key('propertyRange')
        if domain_res or range_res:
           for p in signature['properties']:
               if p['reference'] == s['reference']:
                  new_p = dict()
                  new_p['reference'] = s['reference'] = p['reference']+'_restr'
                  if domain_res: new_p['domain'] = s['propertyDomain']
                  if range_res:  new_p['range']  = s['propertyRange'] 
                  signature['properties'].append(new_p)
                  break

    return new_senses

def __sense_args_differ__(s1,s2):
     if s1.has_key('subjOfProp') and s2.has_key('subjOfProp'):
        if not s1['subjOfProp'] == s2['subjOfProp']: return True
     if s1.has_key('objOfProp') and s2.has_key('objOfProp'):
        if not s1['objOfProp'] == s2['objOfProp']: return True
     return False

def __constructReferenceChain__(chain,signature):

    new_sense = dict()

    name = 'composition'
    for p in chain:
        name += '_' + frag_uri(p)
    new_sense['reference'] = name

    # get domain and range from signature
    for p in signature['properties']: 
        if p['reference'] == frag_uri(chain[0]):
           new_sense['domain'] = p['domain'] 
        if p['reference'] == frag_uri(chain[-1]):
           new_sense['range']  = p['range']
    # fallback (should not be necessary)
    if not new_sense.has_key('domain'): new_sense['domain'] = 'owlThing'
    if not new_sense.has_key('range'):  new_sense['range']  = 'owlThing'

    signature['properties'].append(new_sense)
    return new_sense


def __add_lexical_information__(graph,senses,renaming):

    pos_map = __read_pos_map__()

    for sense in senses:
        extended_entries = []
        for e in sense['entries']: 
            extended_e = dict()

            # canonical form
            updateDict(graph,extended_e,'canonicalForm',str(e),toGF)
            
            # part of speech
            for b in getBindingsAsDict(graph,'pos',str(e),identity):
                if len(b.keys()) > 1: logging.warning(too_many_pos_warning(str(e)))              
                for k in b.keys(): 
                    if pos_map.has_key(b[k]):
                       pos = pos_map[b[k]]
                       extended_e['pos'] = pos
                       # and part-of-speech-specific information (if available)
                       if (check(pos)): updateDict(graph,extended_e,pos,str(e),toGF)
                    else: logging.warning(pos_not_found_warning(b[k]))
            # syntactic behaviors
            extended_e['synBehaviors'] = []
            for b in getBindingsAsDict(graph,'synBehavior',str(e),identity):
                b['frame'] = toGF(b['frame'])
                # query for argument-specific information (e.g. markers)
                for k in b.keys():
                    if k != 'frame':
                       if type(b[k]) == set: 
                          args = []
                          for arg in b[k]: 
                              a = dict(name=toGF(arg))
                              updateDict(graph,a,'synArg',str(arg),toGF)
                              if not a in args: args.append(a)
                          b[k] = args
                       else: 
                          a = dict(name=toGF(b[k]))
                          updateDict(graph,a,'synArg',str(b[k]),toGF)
                          b[k] = a 
                # renaming args
                if e in renaming.keys(): 
                   for v in b.values():
                       if type(v) == dict and v.has_key('name') and v['name'] in renaming[e].keys():
                          v['name'] = renaming[e][v['name']]
                # add syn behavior
                extended_e['synBehaviors'].append(b)              

            # put everything together again
            extended_entries.append(extended_e)

        sense['entries'] = extended_entries


def __read_pos_map__():
    pos_map = dict()
    f_pos_map = open('config/lingonto_pos_map','r')
    for line in f_pos_map.readlines():
        words = line.split()
        for w in words[1:]:
            pos_map[w] = words[0]
    return pos_map

