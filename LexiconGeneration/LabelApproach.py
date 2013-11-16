import Sparql, LexiconGenerator
from Util import  WordnetFunctions as wf


#http://en.wikipedia.org/wiki/Levenshtein_distance
def nld(s1, s2):
    """
    Calculates the normalized Levenshtein distance for two given terms
    """
    if len(s1) < len(s2):
        return nld(s2, s1)
    if not s1:
        return len(s2)
 
    previous_row = xrange(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
 
    return (1-(previous_row[-1] / (max(len(s1),len(s2))+0.0)) if previous_row[-1]!=0 else 1.0)



def load_keystore():
    f = open("/home/swalter/Dropbox/Public/keystore","r")
    hm = {}
    for line in f:
        line = line.replace("\n","")
        tmp = line.split("\t")
        hm[tmp[1]] = tmp[0]
    f.close()
    return hm

def generateTextClass(sparql,uri,keystore,index):
    print "generate text"
    sentence_list = []
    sentence_hm = {}
    tmp = sparql.getClassEntity(uri)
    print "returned entity"
    for x in tmp:
        try:
            list = index.searchKey(keystore[x])
            for x in list:
                sentence_hm[x] = ""

        except:
            pass
        
    for key in sentence_hm:
        sentence_list.append(key)
    #Filter POS tags out and return only list of words and make sure, each word occurs only once!!
    return sentence_list

def generateTextProperty(sparql,uri,keystore,index):
    print "generate text"
    word_list = []
    word_hm = {}
    tmp = sparql.getPropertyEntity(uri)
    for x in tmp:
        try:
            list = index.searchKey(keystore[x])
            for x in list:
                for i in x:
                    word_hm[i[0]] = ""

        except:
            pass
        
    for key in word_hm:
        word_list.append(key)
    return word_list
    
def start(uri,keystore,index):
#     keystore = load_keystore()
#     print "load keystore"
    list_of_entries = []
    sparql = Sparql.Connection()
    label = sparql.getLabel(uri)[0]
    if "(" in label:
        label = label.split("(")[0]
    if label.endswith(" "):
        label = label[:-1]
        
    #one for classes
    if sparql.askClassProperty(uri) == True:
        words = generateTextClass(sparql,uri,keystore,index)
        list_of_entries.append(LexiconGenerator.NounPPFrame(label,uri,{}))
        label_list = [label]
        label_list.extend(wf.return_Noun(label))
        nld_list = {}
        for entry in label_list:
            value = 0
            for word in words:
                try:
                    value += nld(entry,word)
                except:
                    pass
            if value == 0:
                pass
            else:
                value = (value+0.0)/len(words)
            nld_list[entry] = value
            
        counter = 0
        for key, value in sorted(nld_list.iteritems(), key=lambda x:x[1], reverse = True):
            counter +=1
            if counter <=3:
                list_of_entries.append(LexiconGenerator.createClassEntry(uri,entry))
    
    #one for properties
    else:
        words = generateTextProperty(sparql,uri,keystore,index)

        #Noun
        list_of_entries.append(LexiconGenerator.NounPPFrame(label,uri,{}))
        label_list = [label]
        label_list.extend(wf.return_Noun(label))
        nld_list = {}
        for entry in label_list:
            value = 0
            for word in words:
                try:
                    value += nld(entry,word)
                except:
                    pass
            if value == 0:
                pass
            else:
                value = (value+0.0)/len(words)
            nld_list[entry] = value
            
        counter = 0
        for key, value in sorted(nld_list.iteritems(), key=lambda x:x[1], reverse = True):
            counter +=1
            if counter <=3:
                list_of_entries.append(LexiconGenerator.NounPPFrame(key,uri,{}))
                
                
        label_list = [label]
        label_list.extend(wf.return_Verb(label))
        nld_list = {}
        for entry in label_list:
            value = 0
            for word in words:
                try:
                    value += nld(entry,word)
                except:
                    pass
            if value == 0:
                pass
            else:
                value = (value+0.0)/len(words)
            nld_list[entry] = value
            
        counter = 0
        for key, value in sorted(nld_list.iteritems(), key=lambda x:x[1], reverse = True):
            counter +=1
            if counter <=3:
                list_of_entries.append(LexiconGenerator.TransitiveFrame(key,uri,{}))
                
    
    hm = {}
    for x in list_of_entries:
        hm[x] = ""
    list_of_entries = []
    for key in hm:
        list_of_entries.append(key)
    
    return list_of_entries