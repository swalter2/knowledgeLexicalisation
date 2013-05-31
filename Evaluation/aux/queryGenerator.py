
import os
import pystache
from itertools import product


def instantiate_queries():

    # read map
    f_map     = open('config/lingonto_map','r')
    uris      = dict()
    hierarchy = []
    active_head = ''; active_list = []
    for line in f_map.readlines():
        if line.strip():
           words = line.split()
           if line.startswith('*'):
              uris[words[1]] = words[2:]
              active_list.append(words[1])
           else:
              uris[words[0]] = words[1:]
              if active_head: hierarchy.append( (active_head,active_list) )
              active_head = words[0]
              active_list = []
    if active_head: hierarchy.append( (active_head,active_list) )
    # result:
    # hierarchy = [ ('subject',[]), ('number',['singular','plural']), ... ]
    # uris      = { 'subject': [...], 'number': [...], 'singular': [...], ... }

    # build context for rendering
    context = dict() 
    for x,ys in hierarchy:
        if ys: 
           for y in ys: __shave2__(uris,x,y,context)
        else:           __shave1__(uris,x,context)


    # instantiate templates
    sparql = 'sparql/'
    meta   = sparql + 'meta/'
    for f in os.listdir(meta):
        if f.endswith('.mustache'):
           if '.' in f: 
                 filename = f[:f.rindex('.')]
           else: filename = f
           f_in  = open(meta+f,'r').read()
           f_out = open(sparql+filename + '.sparql','w')
           f_out.write(pystache.render(f_in,context))


def __shave1__(uris,x,context):
    context[x] = []
    for value in uris[x]:
        context[x].append( { x : '<'+value+'>' } )
    context[x][-1]['last'] = True

def __shave2__(uris,x,y,context):
    key = x+'_'+y
    context[key] = []
    for pair in product(uris[x],uris[y]):
        context[key].append( { key: '<'+pair[0]+'> <'+pair[1]+'>' } )
    context[key][-1]['last'] = True


## MAIN #########

if __name__ == "__main__":
   instantiate_queries()
