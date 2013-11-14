import Sparql, LexiconGenerator
from Util import  WordnetFunctions as wf

def start(uri):
    list_of_entries = []
    sparql = Sparql.Connection()
    label = sparql.getLabel(uri)[0]
    if "(" in label:
        label = label.split("(")[0]
    if label.endswith(" "):
        label = label[:-1]
        
    #one for classes
    if sparql.askClassProperty(uri) == True:
        label_list = [label]
        label_list.extend(wf.returnNoun(label))
        for entry in label_list:
            for x in LexiconGenerator.createClassEntry(uri,entry):
                list_of_entries.append(x)
    
    #one for properties
    else:
        #Noun
        label_list = [label]
        label_list.extend(wf.returnNoun(label))
        for entry in label_list:
            for x in LexiconGenerator.createClassEntry(entry,uri,{}):
                list_of_entries.append(x)
    
        #Verb
        label_list = [label]
        label_list.extend(wf.returnVerb(label))
        for entry in label_list:
            list_of_entries.append(LexiconGenerator.TransitiveFrame(entry,uri,{}))
    
    return list_of_entries