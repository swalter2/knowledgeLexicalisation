import ConfigParser, Sparql
import LexiconGenerator

 
def createLabel(label,en_target_lexicon):
    if "(" in label:
        label = label.split("(")[0]
    if label.endswith(" "):
        label = label[:-1]
    config = ConfigParser.ConfigParser()
    config.read('config.conf')
    if config.get('system_language', 'language') == "English":
        return [label]
    else:
        #Here "translate only single words, so do not look up "highest mountain" at once, but split up.
        #simple case only for a phrase with two words
        if " " in label:
            label = label.lower()
#             print label
            tmp = label.split(" ")
            array1 = []
            array2 = []
            if tmp[0] in en_target_lexicon and tmp[1] in en_target_lexicon:
                array1 = en_target_lexicon[tmp[0]]
                array2 = en_target_lexicon[tmp[1]]

                label_array = []
                for x in array1:
                    for y in array2:
                        if ";" not in x and ";" not in y:
                            label_array.append((x+" "+y).replace("  ",""))
                return label_array
            
            elif tmp[0] in en_target_lexicon and tmp[1] not in en_target_lexicon:
                return en_target_lexicon[tmp[0]]
            
            elif tmp[0] not in en_target_lexicon and tmp[1] in en_target_lexicon:
                return en_target_lexicon[tmp[1]]
            else:
                return [label]
                
        else:
            if label.lower() in en_target_lexicon:
                label_array = en_target_lexicon[label]
                return label_array
            else:
                return [label]
            
            
def getLabel(uri,en_target_lexicon):
    config = ConfigParser.ConfigParser()
    config.read('config.conf')
    sparql=Sparql.Connection()
    label = sparql.getLabel(uri)[0]
    if "(" in label:
        label = label.split("(")[0]
    if label.endswith(" "):
        label = label[:-1]
        
    if config.get('system_language', 'language') == "English":
        return [label]
    else:
        #Here "translate only single words, so do not look up "highest mountain" at once, but split up.
        #simple case only for a phrase with two words
        if " " in label:
            label = label.lower()
            print label
            tmp = label.split(" ")
            array1 = []
            array2 = []
            if tmp[0] in en_target_lexicon and tmp[1] in en_target_lexicon:
                array1 = en_target_lexicon[tmp[0]]
                array2 = en_target_lexicon[tmp[1]]

                label_array = []
                for x in array1:
                    for y in array2:
                        label_array.append((x+" "+y).replace("  ",""))
                return label_array
            
            elif tmp[0] in en_target_lexicon and tmp[1] not in en_target_lexicon:
                return en_target_lexicon[tmp[0]]
            
            elif tmp[0] not in en_target_lexicon and tmp[1] in en_target_lexicon:
                return en_target_lexicon[tmp[1]]
            else:
                return [label]
                
        else:
            if label.lower() in en_target_lexicon:
                label_array = en_target_lexicon[label]
                return label_array
            else:
                return [label]
        
def createEntries(uri,en_target_lexicon):
    label_array = getLabel(uri,en_target_lexicon)
    lemonEntries = []
    sparql=Sparql.Connection()
    try:
        for label in label_array:#
            if label.startswith(" "):
                label = label[1:]
            label = label.replace("  "," ")
            if label.endswith(" "):
                label = label[:-1]
            
            if len(label)>2:
                if label.endswith("ing"):
    #                 Do NOT use LexiconGenerator.verbEntry here!
                    entry_term = LexiconGenerator.checkForIngForm(label)
                    entry = LexiconGenerator.TransitiveFrame(entry_term, uri,"")
                    lemonEntries.append(entry)
                    
#                     new
                    entry = LexiconGenerator.AdjectivePPFrame(label, uri, {})
                    lemonEntries.append(entry)
                else:
                    entry = LexiconGenerator.NounPPFrame(label, uri, {})
                    lemonEntries.append(entry)
                    label = label.lower()
                    if label.endswith("ed"):
                        entry = LexiconGenerator.AdjectivePPFrame(label, uri, {})
                        lemonEntries.append(entry)
                        
#                         new
                        entry = LexiconGenerator.TransitiveFrame(entry_term, uri,"")
                        lemonEntries.append(entry)
                        
                    try:
    #                     print label
                        info = sparql.getWiktionaryInformations(label)
    #                     print ("info generated")
    #                     print ("info",info)
    #                     print("info[0][0]",info[0][0])
                        if "adjective" in info[0][0]:
                            entry = LexiconGenerator.AdjectivePPFrame(label, uri, {})
                            lemonEntries.append(entry)
                    except:
                        pass
                    
                    if label.endswith(" by"):
                        entry = LexiconGenerator.NounPPFrame("have "+label, uri, {})
                        lemonEntries.append(entry)
                        entry = LexiconGenerator.TransitiveFrame("have "+label, uri, "")
                        lemonEntries.append(entry)
                        entry = LexiconGenerator.NounPPFrame(label.replace(" by",""), uri, {})
                        lemonEntries.append(entry)
    
    # #             entry = LexiconGenerator.NounPossisiveFrameWithoutMarker(label, uri)
    # #             lemonEntries.append(entry)
    # #             entry = LexiconGenerator.AdjectivePPFrame(label, uri, {})
    # #             lemonEntries.append(entry)
    # #             entry = LexiconGenerator.TransitiveFrame(label, uri, {})
    # #             lemonEntries.append(entry)
    except:
        pass
    return lemonEntries

def createAllEntries(uri,en_target_lexicon):
    label_array = getLabel(uri,en_target_lexicon)
    lemonEntries = []
    try:
        for label in label_array:#
            if label.startswith(" "):
                label = label[1:]
            label = label.replace("  "," ")
            if label.endswith(" "):
                label = label[:-1]
            if label.endswith("ing"):
                entry_term = LexiconGenerator.checkForIngForm(label)
                entry = LexiconGenerator.TransitiveFrame(entry_term, uri,{})
                lemonEntries.append(entry)
            else:
                entry = LexiconGenerator.NounPPFrame(label, uri, {})
                lemonEntries.append(entry)
                entry = LexiconGenerator.NounPossisiveFrameWithoutMarker(label, uri)
                lemonEntries.append(entry)
                entry = LexiconGenerator.AdjectivePPFrame(label, uri, {})
                lemonEntries.append(entry)
                entry = LexiconGenerator.TransitiveFrame(label, uri, {})
                lemonEntries.append(entry)
    except:
        pass
    return lemonEntries