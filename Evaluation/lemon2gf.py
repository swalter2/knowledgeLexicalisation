
import sys
import argparse
import logging

from ontology2abstract  import *
from lexicon2concrete   import *
from aux.queryGenerator import *
from aux.utils import print_signature


gf_libs   = dict()
signature = dict( domain = 'Domain',
                   classes    = [],
                   properties = [],
                   entities   = []
                 )


def run():

    p = argparse.ArgumentParser(description='lemon2gf')
    p.add_argument('-o', action='store',  dest='tbox', 
                   help='path to the ontology schema (an OWL/RDF file)')
    p.add_argument('-a', action='store',  dest='abox', 
                    help='path to the ontology instances (an OWL/RDF file)')
    p.add_argument('-l', action='append', dest='lexica', default=[],
                    help='path to the lexicon (a lemon RDF file)')

    args = p.parse_args()

    logging.basicConfig(filename='../test/out/lemon2gf.log',
                        filemode='w', 
                        level=logging.INFO,
                        format='%(levelname)-8s %(message)s')
    console = logging.StreamHandler()
    console.setLevel(logging.WARNING)
    console.setFormatter(logging.Formatter('%(levelname)-8s %(message)s'))
    logging.getLogger('').addHandler(console)

    __init__()

    __generateGF__(signature,args.tbox,args.abox,args.lexica)


def __init__():
    # generate SPARQL queries
    instantiate_queries()
    # language mappings
    for line in open('config/iso639','r').readlines():
        ls = line.split(':')
        if len(ls) == 5: 
           for l in ls[0:4]: gf_libs[l.strip()] = ls[4].strip()


def __generateGF__(signature,tbox,abox,lexica):

    if not tbox is None: convert_ontology(signature,tbox,abox)
    else: logging.warning('No T-Box specified. Resulting GF grammar will not compile.')

    if lexica: convert_lexica(signature,lexica,gf_libs)
    else: logging.warning('No lexicon specified.')
    
    logging.info('Signature:' + print_signature(signature))

    render_ontology(signature)
    
    logging.info('Done.')



## MAIN #########

if __name__ == "__main__":
   run()
