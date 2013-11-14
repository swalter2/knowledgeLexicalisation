from nltk.corpus import wordnet as wn
from nltk.stem.porter import *

#import sys, Wiktionary
import sys
def simple_path(path):
    return [s.lemmas[0].name for s in path]
  
  

    
def return_hypernyms(syn):
    paths = syn.hypernym_paths()
    hm = {}
    for path in paths:
        for s in simple_path(path):
            hm[s]=""
    result_array = []
    for key in hm:
        result_array.append(key)
    return result_array
        
def return_synsets(label):
    
    hm = {}
    result = []
    if "(" in label:
        label = label.split("(")[0]
        
    hm[label]=""
    
    label = label.replace(" ","_")
    try:
        dog = wn.synset(label+'.n.01')
        array = []
        for item in dog.hypernyms():
            array.append(item)
        
        for item in dog.hyponyms():
            array.append(item)
        
        for item in dog.member_holonyms():
            array.append(item)
        
        for item in dog.root_hypernyms():
            array.append(item)
        
        hm = {}
        for item in array:
            for x in item.lemma_names:
                hm[x]=""
        
    except:
        pass
    
    try:
        try:
            for s in wn.synsets(label,pos=wn.VERB):
                for item in s.lemma_names:
                    hm[item]=""
        except:
            
            print "Unexpected error:", sys.exc_info()[0]
            pass
        
        
        try:
            for s in wn.synsets(label,pos=wn.ADJ):
                for item in s.lemma_names:
                    hm[item]=""
        except:
            
            print "Unexpected error:", sys.exc_info()[0]
            pass
        
        
        try:
            for s in wn.synsets(label,pos=wn.ADV):
                for item in s.lemma_names:
                    hm[item]=""
        except:
            
            print "Unexpected error:", sys.exc_info()[0]
            pass
        
            
        try:
            for s in wn.synsets(label,pos=wn.NOUN):
                for item in s.lemma_names:
                    hm[item]=""
        except:
            
            print "Unexpected error:", sys.exc_info()[0]
            pass
        
        
    except:
        print "Unexpected error:", sys.exc_info()[0]
        print "error in returning synonyms \n\n"
    for key in hm:
        result.append(key.replace("_"," "))
        
    return result

def return_Noun(label):
    hm = {}
    for s in wn.synsets(label,pos=wn.NOUN):
        for item in s.lemma_names:
            hm[item]=""
    for key in hm:
        result.append(key.replace("_"," "))
    
    return result


def return_synsetsNoun(label):
    
    hm = {}
    #print "label: "+label
    result = []
    #print "label before: "+label+"Done"
    if "(" in label:
        label = label.split("(")[0]
        
    
    if label.endswith(" "):
        label = label[:-1]
    hm[label]=""
    
    label = label.replace(" ","_")
    try:
    
        try:
            for s in wn.synsets(label,pos=wn.NOUN):
                for item in s.lemma_names:
                    hm[item]=""
        except:
            
            print "Unexpected error:", sys.exc_info()[0]
            pass
        
    except:
        print "Unexpected error:", sys.exc_info()[0]
        pass
    
    for key in hm:
        result.append(key.replace("_"," "))
    
    return result

def return_Informations(word):
    """
    tries to determine, if a word is a verb etc.
    TODO: Fix functions
    """
    stem = PorterStemmer().stem_word(word)
    nouns = []
    verb = []
    adj = []
    if len(wn.synsets(word, wn.VERB))>0:
        #print "its a verb"
        for i in wn.synsets(word, wn.VERB):
            for j in i.lemmas:
                for k in j.derivationally_related_forms():
                    if (k.name.count(stem) > 0) and (k.name not in verb):
                        verb.append(k.name)

        if word.endswith("ed"):
            new_word = word[:-2]
            if new_word not in verb:
                verb.append(new_word)
        if word.endswith("ing"):
            new_word = word[:-3]
            if new_word[-1:] == new_word[-2:-1]:
                new_word = new_word[:-1]
            if new_word not in verb:
                verb.append(new_word)
        if word.endswith("es"):
            new_word = word[:-2]
            if new_word[-1:] == new_word[-2:-1]:
                new_word = new_word[:-1]
            if new_word not in verb:
                verb.append(new_word)
                

        if len(verb)>0:
            return "VERB",verb

    if len(wn.synsets(word, wn.NOUN))>0:
        for i in wn.synsets(word, wn.NOUN):
            for j in i.lemmas:
                for k in j.derivationally_related_forms():
                    if (k.name.count(stem) > 0) and (k.name not in nouns):
                        nouns.append(k.name)

        nouns.append(word)
        return "NOUN",nouns

    if len(wn.synsets(word, wn.ADJ))>0:
        #print "its a adj"
        for i in wn.synsets(word, wn.ADJ):
            for j in i.lemmas:
                for k in j.derivationally_related_forms():
                    if (k.name.count(stem) > 0) and (k.name not in adj):
                        adj.append(k.name)

        adj.append(word)
        return "ADJ",adj
    
        
    return "NONE",[word]
                            
