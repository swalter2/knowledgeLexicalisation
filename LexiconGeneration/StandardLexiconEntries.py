import ConfigParser, Sparql
import LexiconGenerator

def getLabel(uri,en_de_lexicon):
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
    elif config.get('system_language', 'language') == "German":
        #Here "translate only single words, so do not look up "highest mountain" at once, but split up.
        #simple case only for a phrase with two words
        if " " in label:
            label = label.lower()
            print label
            tmp = label.split(" ")
            array1 = []
            array2 = []
            if tmp[0] in en_de_lexicon and tmp[1] in en_de_lexicon:
                array1 = en_de_lexicon[tmp[0]]
                array2 = en_de_lexicon[tmp[1]]

                label_array = []
                for x in array1:
                    for y in array2:
                        label_array.append((x+" "+y).replace("  ",""))
                return label_array
            
            elif tmp[0] in en_de_lexicon and tmp[1] not in en_de_lexicon:
                return en_de_lexicon[tmp[0]]
            
            elif tmp[0] not in en_de_lexicon and tmp[1] in en_de_lexicon:
                return en_de_lexicon[tmp[1]]
            else:
                return [label]
                
        else:
            if label.lower() in en_de_lexicon:
                label_array = en_de_lexicon[label]
                return label_array
            else:
                return [label]
        
def createEntries(uri,en_de_lexicon):
    label_array = getLabel(uri,en_de_lexicon)
    lemonEntries = []
    try:
        for label in label_array:#
            if label.startswith(" "):
                label = label[1:]
            label = label.replace("  "," ")
            if label.endswith(" "):
                label = label[:-1]
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